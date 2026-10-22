"""
05｜連鎖書店季報：多表合併與未匹配清單自動化腳本
"""
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_FILE = BASE_DIR / "output" / "第一季門市營收.xlsx"


def load_orders(data_dir: Path) -> pd.DataFrame:
    """讀取所有月份訂單，統一欄名後上下合併"""
    files = sorted(data_dir.glob("orders_2025_*.csv"))
    if not files:
        raise FileNotFoundError(f"找不到訂單檔：{data_dir}")
    return pd.concat([pd.read_csv(f).rename(columns={"購買數量": "數量"}) for f in files], ignore_index=True)


def clean_keys(orders: pd.DataFrame) -> pd.DataFrame:
    orders = orders.copy()
    orders["門市代碼"] = orders["門市代碼"].str.strip().str.upper()
    return orders


def merge_master(orders: pd.DataFrame, products: pd.DataFrame, stores: pd.DataFrame) -> pd.DataFrame:
    """left join 主檔；筆數改變就停止；無售價營收保持缺值"""
    sales = (orders.merge(products, on="商品編號", how="left", indicator="商品比對")
                   .merge(stores, on="門市代碼", how="left", indicator="門市比對"))
    if len(sales) != len(orders):
        raise ValueError("合併後筆數改變，主檔可能有重複代碼，請檢查。")
    sales["營收"] = sales["數量"] * sales["售價"]
    sales["門市"] = sales["門市"].fillna(sales["門市代碼"] + "（門市資料缺）")
    return sales


def summarize_stores(sales: pd.DataFrame) -> pd.DataFrame:
    summary = sales.groupby("門市").agg(可計價營收=("營收", "sum"), 訂單筆數=("訂單編號", "count"),
                                      無法計價筆數=("售價", lambda s: s.isna().sum()))
    return summary.sort_values("可計價營收", ascending=False).reset_index()


def list_unmatched(sales: pd.DataFrame, stores: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for code, g in sales[sales["門市比對"] == "left_only"].groupby("門市代碼"):
        rows.append(("訂單缺門市主檔", code, len(g), int(g["數量"].sum())))
    for code, g in sales[sales["商品比對"] == "left_only"].groupby("商品編號"):
        rows.append(("訂單缺商品主檔", code, len(g), int(g["數量"].sum())))
    for code in sorted(set(stores["門市代碼"]) - set(sales["門市代碼"])):
        rows.append(("主檔門市無訂單", code, 0, 0))
    return pd.DataFrame(rows, columns=["問題類型", "代碼", "影響訂單筆數", "影響本數"])


def export_excel(summary: pd.DataFrame, issues: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path) as writer:
        summary.to_excel(writer, sheet_name="門市營收", index=False)
        issues.to_excel(writer, sheet_name="未匹配清單", index=False)


def main():
    print("=" * 50)
    print("🚀 開始執行連鎖書店第一季季報腳本...")
    print("=" * 50)

    products = pd.read_csv(DATA_DIR / "products.csv")
    stores = pd.read_csv(DATA_DIR / "stores.csv")
    orders = clean_keys(load_orders(DATA_DIR))
    sales = merge_master(orders, products, stores)
    summary = summarize_stores(sales)
    issues = list_unmatched(sales, stores)
    export_excel(summary, issues, OUTPUT_FILE)

    inner_revenue = (orders.merge(products, on="商品編號").merge(stores, on="門市代碼")
                     .eval("數量 * 售價").sum())
    top = summary.iloc[0]
    print(f"\n📦 【合併結果】訂單 {len(orders):,} 筆，合併後 {len(sales):,} 筆")
    print(f"  - 營收最高門市：{top['門市']}（{top['可計價營收']:,.0f} 元）")
    print("\n⚠️ 【未匹配清單】")
    for _, row in issues.iterrows():
        print(f"  - {row['問題類型']}：{row['代碼']}（{row['影響訂單筆數']} 筆，{row['影響本數']} 本）")
    print(f"\n💡 left join 可計價營收 {sales['營收'].sum():,.0f} 元；inner join 會少算 {sales['營收'].sum() - inner_revenue:,.0f} 元")
    print(f"\n✅ 成果已成功匯出至：{OUTPUT_FILE.relative_to(BASE_DIR)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
