"""
04｜社區活動問卷：清理規則與清理紀錄自動化腳本
"""
import re
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "survey_raw.csv"
OUTPUT_FILE = BASE_DIR / "output" / "問卷清理結果.xlsx"

SATISFACTION_TEXT = {"非常滿意": "5", "滿意": "4"}   # 對照規則：可在課堂討論後修改
GENDER_MAP = {"男": "男", "M": "男", "male": "男", "男生": "男",
              "女": "女", "F": "女", "female": "女", "女生": "女"}


def load_raw(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"找不到資料檔案：{csv_path}")
    return pd.read_csv(csv_path, dtype=str)


def drop_duplicates(raw: pd.DataFrame, log: list) -> pd.DataFrame:
    survey = raw.drop_duplicates().copy()
    log.append(("全部", "刪除完全重複的列", len(raw) - len(survey)))
    return survey


def clean_satisfaction(survey: pd.DataFrame, log: list) -> pd.DataFrame:
    raw_score = survey["滿意度"]
    text = raw_score.str.strip().str.replace("分", "", regex=False).replace(SATISFACTION_TEXT)
    score = pd.to_numeric(text, errors="coerce")
    invalid = score.notna() & ~score.between(1, 5)
    survey["滿意度"] = score.where(~invalid)
    log.append(("滿意度", "同義寫法對應 1～5；不在 1～5 設為缺值", count_changed(raw_score, survey["滿意度"])))
    return survey


def count_changed(before: pd.Series, after: pd.Series) -> int:
    """原本有填、但清理後被改寫或設為缺值的筆數"""
    had_value = before.notna()
    if pd.api.types.is_numeric_dtype(after):
        before = pd.to_numeric(before, errors="coerce")
    return int((had_value & (before != after)).sum())


def fix_phone(text: str) -> str:
    digits = re.sub(r"\D", "", str(text))
    if digits.startswith("886"):
        digits = "0" + digits[3:]
    if len(digits) == 9 and digits.startswith("9"):
        digits = "0" + digits
    return digits


def clean_other_fields(survey: pd.DataFrame, log: list) -> pd.DataFrame:
    clean = survey.copy()
    clean["姓名"] = survey["姓名"].str.strip()
    clean["性別"] = survey["性別"].str.strip().map(GENDER_MAP)
    area = survey["居住區"].str.strip()
    clean["居住區"] = area.where(area.str.endswith("區"), area + "區")
    age = pd.to_numeric(survey["年齡"].str.extract(r"(\d+)")[0], errors="coerce")
    clean["年齡"] = age.where(age.between(10, 100))
    clean["電話"] = survey["電話"].map(fix_phone)
    for col, rule in [("姓名", "去除前後空白"), ("性別", "統一為男／女"), ("居住區", "去空白、補上「區」字"),
                      ("年齡", "只取數字；不在 10～100 歲設為缺值"), ("電話", "只留數字、+886 改 0、補前導 0")]:
        log.append((col, rule, count_changed(survey[col], clean[col])))
    return clean


def export_excel(clean: pd.DataFrame, log: list, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path) as writer:
        clean.to_excel(writer, sheet_name="乾淨問卷", index=False)
        pd.DataFrame(log, columns=["欄位", "清理規則", "受影響筆數"]).to_excel(writer, sheet_name="清理紀錄", index=False)


def main():
    print("=" * 50)
    print("🚀 開始執行社區活動問卷清理腳本...")
    print("=" * 50)

    log = []
    raw = load_raw(DATA_PATH)
    survey = clean_satisfaction(drop_duplicates(raw, log), log)
    clean = clean_other_fields(survey, log)
    export_excel(clean, log, OUTPUT_FILE)

    counts = clean["滿意度"].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0)
    print(f"\n🧹 【清理結果】原始 {len(raw)} 列 → 去重複後 {len(clean)} 份")
    print(f"  - 滿意度有效 {counts.sum()} 份、缺值 {clean['滿意度'].isna().sum()} 份")
    print("  - 1～5 分人數：" + "、".join(f"{int(s)} 分 {c} 人" for s, c in counts.items()))
    print(f"  - 電話全部為 09 開頭 10 碼：{clean['電話'].str.fullmatch(r'09\d{8}').all()}")
    print("\n📝 【清理紀錄】")
    for col, rule, n in log:
        print(f"  - {col}：{rule}（{n} 筆）")
    print(f"\n✅ 成果已成功匯出至：{OUTPUT_FILE.relative_to(BASE_DIR)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
