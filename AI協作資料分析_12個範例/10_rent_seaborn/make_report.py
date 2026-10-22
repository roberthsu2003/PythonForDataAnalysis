"""
10｜台北租屋：異常值排除與每坪租金自動化腳本
"""
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "rent_listings.csv"
OUTPUT_FILE = BASE_DIR / "output" / "租屋清理結果.xlsx"
MIN_RENT, MAX_RENT = 1_000, 500_000


def load_data(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"找不到資料檔案：{csv_path}")
    return pd.read_csv(csv_path)


def flag_invalid(df: pd.DataFrame) -> pd.Series:
    """回傳每筆物件的排除原因；空字串代表保留"""
    reasons = pd.Series("", index=df.index)
    reasons[df["坪數"] <= 0] += "坪數為 0；"
    reasons[df["月租金"] < MIN_RENT] += f"月租金低於 {MIN_RENT:,} 元；"
    reasons[df["月租金"] > MAX_RENT] += f"月租金超過 {MAX_RENT:,} 元；"
    return reasons


def add_price_per_ping(clean: pd.DataFrame) -> pd.DataFrame:
    clean = clean.copy()
    clean["每坪租金"] = (clean["月租金"] / clean["坪數"]).round(0)
    return clean


def export_excel(clean: pd.DataFrame, excluded: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path) as writer:
        clean.to_excel(writer, sheet_name="清理後物件", index=False)
        excluded.to_excel(writer, sheet_name="排除清單", index=False)


def main():
    print("=" * 50)
    print("🚀 開始執行台北租屋清理腳本...")
    print("=" * 50)

    df = load_data(DATA_PATH)
    reasons = flag_invalid(df)
    excluded = df[reasons != ""].assign(排除原因=reasons[reasons != ""])
    clean = add_price_per_ping(df[reasons == ""])
    if len(clean) + len(excluded) != len(df):
        raise ValueError("清理後與排除筆數相加不等於原始筆數。")
    export_excel(clean, excluded, OUTPUT_FILE)

    print(f"\n🧹 【異常值排除】{len(df)} 筆 → {len(clean)} 筆")
    for _, row in excluded.iterrows():
        print(f"  - {row['物件編號']}：{row['排除原因']}")
    print(f"  - 月租金平均：{df['月租金'].mean():,.0f} → {clean['月租金'].mean():,.0f} 元")
    print(f"\n🏠 【每坪租金】中位數 {clean['每坪租金'].median():,.0f} 元／坪")
    for area, value in clean.groupby("行政區")["每坪租金"].median().sort_values(ascending=False).items():
        print(f"  - {area}：{value:,.0f} 元／坪")
    print(f"\n✅ 成果已成功匯出至：{OUTPUT_FILE.relative_to(BASE_DIR)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
