"""
08｜外送訂單：UTC 轉台灣時間與時段報表自動化腳本
"""
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "delivery_orders.csv"
OUTPUT_FILE = BASE_DIR / "output" / "外送時段報表.xlsx"
LOCAL_TZ = "Asia/Taipei"


def load_data(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"找不到資料檔案：{csv_path}")
    return pd.read_csv(csv_path)


def convert_timezone(df: pd.DataFrame) -> pd.DataFrame:
    """以 UTC 解析後轉為台灣時間，並拆出小時、日期與送達分鐘"""
    df = df.copy()
    df["下單時間_台灣"] = pd.to_datetime(df["下單時間_utc"], utc=True).dt.tz_convert(LOCAL_TZ)
    df["送達時間_台灣"] = pd.to_datetime(df["送達時間_utc"], utc=True).dt.tz_convert(LOCAL_TZ)
    df["小時"] = df["下單時間_台灣"].dt.hour
    df["日期"] = df["下單時間_台灣"].dt.date
    df["送達分鐘"] = (df["送達時間_台灣"] - df["下單時間_台灣"]).dt.total_seconds() / 60
    return df


def hourly_orders(df: pd.DataFrame) -> pd.DataFrame:
    table = df["小時"].value_counts().reindex(range(24), fill_value=0).rename("訂單數").to_frame()
    table["占比(%)"] = (table["訂單數"] / table["訂單數"].sum() * 100).round(1)
    return table.rename_axis("小時（台灣時間）").reset_index()


def export_excel(table: pd.DataFrame, df: pd.DataFrame, output_path: Path) -> None:
    detail = df[["訂單編號", "下單時間_台灣", "送達時間_台灣", "區域", "訂單金額", "送達分鐘"]].copy()
    for col in ["下單時間_台灣", "送達時間_台灣"]:
        detail[col] = detail[col].dt.strftime("%Y-%m-%d %H:%M:%S")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path) as writer:
        table.to_excel(writer, sheet_name="各小時訂單", index=False)
        detail.to_excel(writer, sheet_name="訂單明細", index=False)


def main():
    print("=" * 50)
    print("🚀 開始執行外送時段報表腳本...")
    print("=" * 50)

    df = convert_timezone(load_data(DATA_PATH))
    table = hourly_orders(df)
    export_excel(table, df, OUTPUT_FILE)

    top3 = table.nlargest(3, "訂單數")
    changed = (df["下單時間_utc"].str[:10] != df["日期"].astype(str)).sum()
    print(f"\n🕒 【時段分析】訂單 {len(df):,} 筆（已轉為台灣時間）")
    for _, row in top3.iterrows():
        print(f"  - {int(row['小時（台灣時間）']):>2} 點：{int(row['訂單數'])} 筆（{row['占比(%)']}%）")
    print(f"\n📅 因時區轉換而改變日期：{changed} 筆")
    print(f"\n✅ 成果已成功匯出至：{OUTPUT_FILE.relative_to(BASE_DIR)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
