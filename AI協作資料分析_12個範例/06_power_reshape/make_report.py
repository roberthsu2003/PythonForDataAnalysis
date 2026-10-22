"""
06｜縣市用電：寬表轉長表與核對自動化腳本
"""
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "power_wide.csv"
OUTPUT_FILE = BASE_DIR / "output" / "縣市用電_長表.xlsx"
ID_COLS = ["縣市", "區域"]


def load_wide(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"找不到資料檔案：{csv_path}")
    return pd.read_csv(csv_path)


def to_long(wide: pd.DataFrame) -> pd.DataFrame:
    """把月份欄位轉成「年月、用電量」兩欄"""
    long_df = wide.melt(id_vars=ID_COLS, var_name="年月", value_name="用電量_百萬度")
    long_df["日期"] = pd.to_datetime(long_df["年月"], format="%Y-%m")
    long_df["年"] = long_df["日期"].dt.year
    long_df["月"] = long_df["日期"].dt.month
    return long_df.sort_values(["縣市", "日期"]).reset_index(drop=True)


def validate(wide: pd.DataFrame, long_df: pd.DataFrame) -> tuple:
    month_cols = [c for c in wide.columns if c not in ID_COLS]
    expected_rows = wide["縣市"].nunique() * len(month_cols)
    wide_total = wide[month_cols].sum().sum()
    long_total = long_df["用電量_百萬度"].sum()
    if len(long_df) != expected_rows or abs(wide_total - long_total) > 1e-6:
        raise ValueError("寬表轉長表後列數或總量不一致，請停止檢查。")
    return expected_rows, wide_total


def export_excel(long_df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    long_df[["縣市", "區域", "年", "月", "年月", "用電量_百萬度"]].to_excel(output_path, index=False)


def main():
    print("=" * 50)
    print("🚀 開始執行縣市用電寬表轉長表腳本...")
    print("=" * 50)

    wide = load_wide(DATA_PATH)
    long_df = to_long(wide)
    rows, total = validate(wide, long_df)
    export_excel(long_df, OUTPUT_FILE)

    taipei = long_df[long_df["縣市"] == "臺北市"]
    peak = taipei.loc[taipei["用電量_百萬度"].idxmax()]
    low = taipei.loc[taipei["用電量_百萬度"].idxmin()]
    print(f"\n🔄 【轉換核對】寬表 {wide.shape[0]} 列 × {wide.shape[1]} 欄 → 長表 {len(long_df)} 列（應為 {rows}）")
    print(f"  - 總用電量一致：{total:,.1f} 百萬度")
    print("\n📈 【臺北市季節型態】")
    print(f"  - 最高：{peak['年月']}（{peak['用電量_百萬度']:.1f} 百萬度）")
    print(f"  - 最低：{low['年月']}（{low['用電量_百萬度']:.1f} 百萬度）")
    print(f"\n✅ 成果已成功匯出至：{OUTPUT_FILE.relative_to(BASE_DIR)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
