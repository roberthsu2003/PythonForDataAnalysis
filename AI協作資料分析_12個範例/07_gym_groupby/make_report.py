"""
07｜健身房會員：分店入場人次與會員人數自動化腳本
"""
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "gym_visits.csv"
OUTPUT_FILE = BASE_DIR / "output" / "分店摘要.xlsx"


def load_data(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"找不到資料檔案：{csv_path}")
    return pd.read_csv(csv_path)


def summarize_branches(df: pd.DataFrame) -> pd.DataFrame:
    """count 數人次、nunique 數人數"""
    summary = df.groupby("分店").agg(入場人次=("紀錄編號", "count"), 會員人數=("會員編號", "nunique"))
    summary["平均每人入場次數"] = (summary["入場人次"] / summary["會員人數"]).round(1)
    return summary.sort_values("入場人次", ascending=False)


def add_total_row(summary: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
    total = pd.DataFrame({"入場人次": [len(df)], "會員人數": [df["會員編號"].nunique()]}, index=["全部"])
    total["平均每人入場次數"] = (total["入場人次"] / total["會員人數"]).round(1)
    return pd.concat([summary, total]).rename_axis("分店").reset_index()


def export_excel(report: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report.to_excel(output_path, index=False)


def main():
    print("=" * 50)
    print("🚀 開始執行健身房分店摘要腳本...")
    print("=" * 50)

    df = load_data(DATA_PATH)
    branches = summarize_branches(df)
    report = add_total_row(branches, df)
    export_excel(report, OUTPUT_FILE)

    top, bottom = branches.iloc[0], branches.iloc[-1]
    print(f"\n🏋️ 【人次 vs 人數】入場 {len(df):,} 人次，不重複會員 {df['會員編號'].nunique()} 人")
    print(f"  - 入場人次最多：{branches.index[0]}（{int(top['入場人次'])} 人次，會員 {int(top['會員人數'])} 人）")
    print(f"  - 入場人次最少：{branches.index[-1]}（{int(bottom['入場人次'])} 人次，會員 {int(bottom['會員人數'])} 人）")
    print(f"\n✅ 成果已成功匯出至：{OUTPUT_FILE.relative_to(BASE_DIR)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
