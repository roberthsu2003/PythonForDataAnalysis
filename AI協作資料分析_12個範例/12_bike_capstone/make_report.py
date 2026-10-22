"""
12｜共享單車綜合專題：清理決策表與借車時段自動化腳本
"""
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_FILE = BASE_DIR / "output" / "共享單車專題.xlsx"
LONG_RIDE_MINUTES = 2 * 24 * 60


def load_data(data_dir: Path) -> pd.DataFrame:
    path = data_dir / "bike_trips.csv"
    if not path.exists():
        raise FileNotFoundError(f"找不到資料檔案：{path}")
    return pd.read_csv(path)


def clean_rides(trips: pd.DataFrame) -> pd.DataFrame:
    """刪重複、時間填反對調；超長騎乘與還車站空白只標記不刪除"""
    rides = trips.drop_duplicates().copy()
    rides["借車時間"] = pd.to_datetime(rides["借車時間"])
    rides["還車時間"] = pd.to_datetime(rides["還車時間"])
    swapped = rides["還車時間"] < rides["借車時間"]
    rides.loc[swapped, ["借車時間", "還車時間"]] = rides.loc[swapped, ["還車時間", "借車時間"]].to_numpy()
    rides["時間已對調"] = swapped
    rides["騎乘分鐘"] = (rides["還車時間"] - rides["借車時間"]).dt.total_seconds() / 60
    rides["超長騎乘"] = rides["騎乘分鐘"] > LONG_RIDE_MINUTES
    rides["借車小時"] = rides["借車時間"].dt.hour
    return rides


def build_decisions(trips: pd.DataFrame, rides: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame([
        ("完全重複的紀錄", len(trips) - len(rides), "刪除", "所有分析", "—"),
        ("還車時間早於借車時間", int(rides["時間已對調"].sum()), "判斷為填反，對調並標記", "騎乘時間、借車時段", "—"),
        ("騎乘超過 2 天", int(rides["超長騎乘"].sum()), "保留並標記", "騎乘時間（需排除）", "借車時段、借車次數"),
        ("還車站空白", int(rides["還車站"].isna().sum()), "保留缺值", "還車站相關分析（需排除）", "借車時段、借車次數"),
    ], columns=["資料問題", "筆數", "處理方式", "影響的分析", "不影響的分析"])


def hourly_counts(rides: pd.DataFrame) -> pd.Series:
    return rides["借車小時"].value_counts().reindex(range(24), fill_value=0)


def export_excel(decisions: pd.DataFrame, hourly: pd.Series, rides: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path) as writer:
        decisions.to_excel(writer, sheet_name="清理決策表", index=False)
        hourly.rename_axis("借車小時").rename("借車次數").reset_index().to_excel(writer, sheet_name="各小時借車數", index=False)
        rides.to_excel(writer, sheet_name="清理後騎乘", index=False)


def main():
    print("=" * 50)
    print("🚀 開始執行共享單車綜合專題腳本...")
    print("=" * 50)

    trips = load_data(DATA_DIR)
    rides = clean_rides(trips)
    decisions = build_decisions(trips, rides)
    hourly = hourly_counts(rides)
    export_excel(decisions, hourly, rides, OUTPUT_FILE)

    print(f"\n🧹 【清理決策表】原始 {len(trips):,} 筆 → 清理後 {len(rides):,} 筆")
    for _, row in decisions.iterrows():
        print(f"  - {row['資料問題']}：{row['筆數']} 筆 → {row['處理方式']}")
    am, pm = hourly[:12].idxmax(), hourly[12:].idxmax()
    print("\n🚲 【借車尖峰】")
    print(f"  - 早上：{am} 點（{hourly[am]} 次）；傍晚：{pm} 點（{hourly[pm]} 次）")
    print(f"\n✅ 成果已成功匯出至：{OUTPUT_FILE.relative_to(BASE_DIR)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
