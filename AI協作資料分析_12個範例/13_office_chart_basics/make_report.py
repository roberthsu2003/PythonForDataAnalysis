"""
13｜辦公室資料：部門全年支出自動化腳本
"""
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "辦公室圖表練習資料.xlsx"
OUTPUT_FILE = BASE_DIR / "output" / "部門全年支出.xlsx"


def load_monthly(xlsx_path: Path) -> pd.DataFrame:
    if not xlsx_path.exists():
        raise FileNotFoundError(f"找不到資料檔案：{xlsx_path}（請先執行 lesson.ipynb 第 0 步下載）")
    return pd.read_excel(xlsx_path, sheet_name="部門月報")


def summarize_departments(monthly: pd.DataFrame) -> pd.DataFrame:
    """金額依部門加總；人數是分母，每月相同，只取一個月的值"""
    if (monthly.groupby("部門")["人數"].nunique() != 1).any():
        raise ValueError("有部門各月人數不同，請先確認每人支出的分母。")
    dept = monthly.groupby("部門").agg(人數=("人數", "first"), 全年預算=("預算（元）", "sum"),
                                     全年實際支出=("實際支出（元）", "sum"))
    dept["差異"] = dept["全年實際支出"] - dept["全年預算"]
    dept["預算執行率"] = dept["全年實際支出"] / dept["全年預算"]
    dept["每人全年支出"] = (dept["全年實際支出"] / dept["人數"]).round(0)
    return dept.sort_values("全年實際支出", ascending=False).reset_index()


def export_excel(dept: pd.DataFrame, monthly: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dept.to_excel(output_path, index=False)
    if pd.read_excel(output_path)["全年實際支出"].sum() != monthly["實際支出（元）"].sum():
        raise ValueError("匯出後全年實際支出合計與部門月報不一致。")


def main():
    print("=" * 50)
    print("🚀 開始執行部門全年支出腳本...")
    print("=" * 50)

    monthly = load_monthly(DATA_PATH)
    dept = summarize_departments(monthly)
    export_excel(dept, monthly, OUTPUT_FILE)

    print(f"\n🏢 【部門全年實際支出】部門月報 {len(monthly)} 列 → {len(dept)} 個部門")
    for _, row in dept.iterrows():
        print(f"  - {row['部門']}：{row['全年實際支出']:>10,.0f} 元（執行率 {row['預算執行率']:.1%}，每人 {row['每人全年支出']:,.0f} 元）")
    per_head = dept.loc[dept["每人全年支出"].idxmax()]
    print(f"\n👤 每人全年支出最高：{per_head['部門']}（{per_head['每人全年支出']:,.0f} 元）")
    print(f"\n✅ 成果已成功匯出至：{OUTPUT_FILE.relative_to(BASE_DIR)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
