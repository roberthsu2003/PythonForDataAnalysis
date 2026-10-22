"""
09｜六城市氣象：城市 × 月份對照表自動化腳本
"""
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "weather_monthly.csv"
OUTPUT_FILE = BASE_DIR / "output" / "六城市氣象對照表.xlsx"
METRIC_UNITS = {"平均氣溫": "°C", "降雨量": "毫米", "日照時數": "小時", "降雨日數": "天"}


def load_data(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"找不到資料檔案：{csv_path}")
    return pd.read_csv(csv_path)


def check_complete(df: pd.DataFrame) -> None:
    """每個城市都要有 1～12 月各一列"""
    ok = df.groupby("城市")["月份"].apply(lambda m: sorted(m) == list(range(1, 13)))
    if not ok.all():
        raise ValueError(f"月份不完整的城市：{list(ok[~ok].index)}")


def build_tables(df: pd.DataFrame) -> dict:
    tables = {}
    for metric, unit in METRIC_UNITS.items():
        table = df.pivot(index="城市", columns="月份", values=metric)
        table.columns = [f"{m}月" for m in table.columns]
        if metric == "平均氣溫":
            table["全年平均"] = table.mean(axis=1).round(1)
        else:
            table["全年合計"] = table.sum(axis=1).round(1)
        tables[f"{metric}({unit})"] = table
    return tables


def export_excel(tables: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path) as writer:
        for name, table in tables.items():
            table.to_excel(writer, sheet_name=name)


def main():
    print("=" * 50)
    print("🚀 開始執行六城市氣象對照表腳本...")
    print("=" * 50)

    df = load_data(DATA_PATH)
    check_complete(df)
    tables = build_tables(df)
    export_excel(tables, OUTPUT_FILE)

    taipei = df[df["城市"] == "臺北"]
    hot = taipei.loc[taipei["平均氣溫"].idxmax()]
    cold = taipei.loc[taipei["平均氣溫"].idxmin()]
    rain = tables["降雨量(毫米)"]["全年合計"].sort_values(ascending=False)
    print(f"\n✅ 【資料完整】{df['城市'].nunique()} 個城市 × 12 個月 = {len(df)} 列")
    print("\n🌡️ 【臺北氣溫】")
    print(f"  - 最熱：{hot['月份']} 月（{hot['平均氣溫']} °C）；最冷：{cold['月份']} 月（{cold['平均氣溫']} °C）")
    print("\n🌧️ 【全年降雨量】")
    print(f"  - 最多：{rain.index[0]}（{rain.iloc[0]:,.0f} 毫米）；最少：{rain.index[-1]}（{rain.iloc[-1]:,.0f} 毫米）")
    print(f"\n✅ 成果已成功匯出至：{OUTPUT_FILE.relative_to(BASE_DIR)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
