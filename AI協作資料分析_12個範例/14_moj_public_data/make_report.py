"""
14｜法務部公開統計：官方資料下載與核心結果自動化腳本
"""
from datetime import date
from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_FILE = BASE_DIR / "output" / "公開資料分析.xlsx"

CHOICE = "B"   # A：每日收容動態；B：勒戒新入所人數；C：決定補償金額
SOURCES = {
    "A": {"名稱": "矯正機關每日收容動態", "頁面": "https://data.gov.tw/dataset/101185",
          "下載": "https://prisonmuseum.moj.gov.tw/jqw_pub/today.xml", "檔名": "moj_daily_custody.xml",
          "欄位": ["日期", "實際收容", "男", "女", "核定容額", "超收率"]},
    "B": {"名稱": "成年勒戒處所新入所收容人人數按毒品種類及性別分", "頁面": "https://data.gov.tw/dataset/39440",
          "下載": "https://www.rjsd.moj.gov.tw/rjsdweb/OpenData.ashx?code=G08102", "檔名": "moj_rehab_new_admissions.csv",
          "欄位": ["毒品種類", "觀勒次數", "性別", "民國年", "月份", "人"]},
    "C": {"名稱": "地方檢察署犯罪被害補償金決定補償金額（按補償金類別分）", "頁面": "https://data.gov.tw/dataset/15128",
          "下載": "https://www.rjsd.moj.gov.tw/rjsdweb/OpenData.ashx?code=QC1004", "檔名": "moj_victim_compensation.csv",
          "欄位": ["被害補償金類別", "民國年", "月份", "新臺幣元"]},
}


def download(source: dict) -> tuple:
    """重新下載官方資料；失敗時改用既有檔案"""
    path = DATA_DIR / source["檔名"]
    DATA_DIR.mkdir(exist_ok=True)
    try:
        urlretrieve(source["下載"], path)
        return path, date.today().isoformat()
    except Exception as error:
        if not path.exists():
            raise FileNotFoundError(f"下載失敗且 data/ 沒有既有檔案：{error}") from error
        print(f"⚠️ 下載失敗（{type(error).__name__}），改用既有檔案：{path.name}")
        return path, "（使用既有檔案，下載日期不明）"


def load_data(path: Path) -> pd.DataFrame:
    if path.suffix == ".xml":
        return pd.read_xml(path, parser="etree")
    return pd.read_csv(path, encoding="utf-8-sig", dtype={"月份": str})


def check_columns(df: pd.DataFrame, expected: list) -> None:
    missing = [c for c in expected if c not in df.columns]
    if missing:
        raise ValueError(f"官方欄位可能已改版，缺少：{missing}；實際欄位：{list(df.columns)}")


def build_result(df: pd.DataFrame) -> tuple:
    """回傳（核心結果, 資料期間, 提示訊息）"""
    notes = []
    if CHOICE == "A":
        row = df.iloc[0]
        result = pd.DataFrame({"項目": ["核定容額", "實際收容"], "人數": [int(row["核定容額"]), int(row["實際收容"])]})
        notes.append("只有單日快照，不能畫時間趨勢")
        return result, str(row["日期"]), notes
    df = df.copy()
    df["年月"] = pd.to_datetime((df["民國年"].astype(int) + 1911).astype(str) + "-" + df["月份"].str.zfill(2) + "-01")
    months = df.groupby("民國年")["月份"].nunique()
    if (months < 12).any():
        notes.append(f"民國 {list(months[months < 12].index)} 年不滿 12 個月，不能和完整年度比較全年總量")
    period = f"{df['年月'].min():%Y-%m}～{df['年月'].max():%Y-%m}"
    if CHOICE == "B":
        result = df.groupby("年月", as_index=False)["人"].sum().rename(columns={"人": "新入所人數"})
        result["年月"] = result["年月"].dt.strftime("%Y-%m")
    else:
        latest = months[months == 12].index.max()
        result = (df[df["民國年"] == latest].groupby("被害補償金類別", as_index=False)["新臺幣元"].sum()
                  .sort_values("新臺幣元", ascending=False))
        notes.append(f"比較年度：民國 {latest} 年（最近一個完整年度）")
    return result, period, notes


def export_excel(result: pd.DataFrame, card: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path) as writer:
        result.to_excel(writer, sheet_name="核心結果", index=False)
        card.to_excel(writer, sheet_name="來源卡", index=False)


def main():
    print("=" * 50)
    print("🚀 開始執行法務部公開統計自動化腳本...")
    print("=" * 50)

    source = SOURCES[CHOICE]
    path, downloaded = download(source)
    df = load_data(path)
    check_columns(df, source["欄位"])
    result, period, notes = build_result(df)
    card = pd.DataFrame({"項目": ["資料名稱", "資料頁網址", "下載網址", "下載日期", "資料期間", "不能推論的事"],
                         "內容": [source["名稱"], source["頁面"], source["下載"], downloaded, period,
                                "不能回推個人；人數、金額不能互換；同期變化不能直接說成政策成效"]})
    export_excel(result, card, OUTPUT_FILE)

    print(f"\n🗂️ 【來源卡】{source['名稱']}")
    print(f"  - 資料頁：{source['頁面']}")
    print(f"  - 下載日期：{downloaded}；資料期間：{period}；原始資料 {len(df)} 列")
    for note in notes:
        print(f"  ⚠️ {note}")
    print("\n📊 【核心結果（最後 5 列）】")
    print(result.tail(5).to_string(index=False))
    print(f"\n✅ 成果已成功匯出至：{OUTPUT_FILE.relative_to(BASE_DIR)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
