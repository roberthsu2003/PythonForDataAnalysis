"""
02｜便利商店一週銷售：類別營收報表自動化腳本
"""
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "store_sales.csv"
OUTPUT_FILE = BASE_DIR / "output" / "類別營收報表.xlsx"


def load_data(csv_path: Path) -> pd.DataFrame:
    """讀取原始銷售資料（不修改原檔）"""
    if not csv_path.exists():
        raise FileNotFoundError(f"找不到資料檔案：{csv_path}")
    return pd.read_csv(csv_path)


def add_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """逐列衍生營收；單價不能直接加總"""
    result = df.copy()
    result["營收"] = result["單價"] * result["數量"]
    return result


def summarize_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """依類別加總數量與營收，並附上兩種排名"""
    summary = df.groupby("類別").agg(銷售數量=("數量", "sum"), 整週營收=("營收", "sum"))
    summary["數量排名"] = summary["銷售數量"].rank(ascending=False).astype(int)
    summary["營收排名"] = summary["整週營收"].rank(ascending=False).astype(int)
    return summary.sort_values("整週營收", ascending=False).reset_index()


def export_excel(summary: pd.DataFrame, detail: pd.DataFrame, output_path: Path) -> None:
    """匯出兩個工作表，並重新讀檔核對營收合計"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path) as writer:
        summary.to_excel(writer, sheet_name="類別營收", index=False)
        detail.to_excel(writer, sheet_name="品項明細", index=False)
    check = pd.read_excel(output_path, sheet_name="類別營收")
    if check["整週營收"].sum() != detail["營收"].sum():
        raise ValueError("匯出後營收合計與原始資料不一致，請停止並檢查。")


def main():
    print("=" * 50)
    print("🚀 開始執行便利商店類別營收報表腳本...")
    print("=" * 50)

    detail = add_revenue(load_data(DATA_PATH))
    summary = summarize_by_category(detail)
    export_excel(summary, detail, OUTPUT_FILE)

    top, bottom = summary.iloc[0], summary.iloc[-1]
    swapped = summary[summary["數量排名"] != summary["營收排名"]]
    print(f"\n📊 【整週營收比較】資料 {len(detail)} 列，總營收 {detail['營收'].sum():,} 元")
    print(f"  - 營收最高類別：{top['類別']}（{top['整週營收']:,} 元）")
    print(f"  - 營收最低類別：{bottom['類別']}（{bottom['整週營收']:,} 元）")
    print("\n🔁 【數量排名 ≠ 營收排名】")
    for _, row in swapped.iterrows():
        print(f"  - {row['類別']}：數量第 {row['數量排名']} 名，營收第 {row['營收排名']} 名")
    print(f"\n✅ 成果已成功匯出並核對：{OUTPUT_FILE.relative_to(BASE_DIR)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
