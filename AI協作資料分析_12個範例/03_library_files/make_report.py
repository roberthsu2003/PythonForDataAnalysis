"""
03｜圖書館借閱：多格式讀檔與分類借閱統計自動化腳本
"""
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_FILE = BASE_DIR / "output" / "分類借閱統計.xlsx"


def load_sources(data_dir: Path) -> dict:
    """依各檔格式正確讀取：Big5 CSV、兩個 Excel 工作表、JSON"""
    sheets = pd.read_excel(data_dir / "books.xlsx", sheet_name=None, dtype={"分類號": str})
    return {
        "loans": pd.read_csv(data_dir / "loans_big5.csv", encoding="cp950"),
        "books": sheets["書目"],
        "categories": sheets["分類代碼"],
        "members": pd.read_json(data_dir / "members.json"),
    }


def attach_category(loans: pd.DataFrame, books: pd.DataFrame, categories: pd.DataFrame) -> pd.DataFrame:
    """書號 → 分類號 → 分類名稱；筆數改變或對不到就停止"""
    detail = loans.merge(books[["書號", "分類號"]], on="書號", how="left").merge(categories, on="分類號", how="left")
    if len(detail) != len(loans):
        raise ValueError("合併後借閱筆數改變，請檢查書號是否重複。")
    missing = detail["分類名稱"].isna().sum()
    if missing:
        raise ValueError(f"有 {missing} 筆借閱對不到分類名稱，請檢查分類號格式。")
    return detail


def summarize_categories(detail: pd.DataFrame, books: pd.DataFrame, categories: pd.DataFrame) -> pd.DataFrame:
    """借閱次數、館藏冊數與每冊平均借閱次數"""
    counts = detail.groupby("分類名稱").size().rename("借閱次數")
    holdings = books.merge(categories, on="分類號").groupby("分類名稱").size().rename("館藏冊數")
    report = pd.concat([counts, holdings], axis=1).sort_values("借閱次數", ascending=False)
    report["每冊平均借閱次數"] = (report["借閱次數"] / report["館藏冊數"]).round(1)
    return report.reset_index()


def export_excel(report: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report.to_excel(output_path, index=False)


def main():
    print("=" * 50)
    print("🚀 開始執行圖書館分類借閱統計腳本...")
    print("=" * 50)

    src = load_sources(DATA_DIR)
    detail = attach_category(src["loans"], src["books"], src["categories"])
    report = summarize_categories(detail, src["books"], src["categories"])
    export_excel(report, OUTPUT_FILE)

    print("\n📂 【讀檔結果】")
    print(f"  - 借閱 {len(src['loans'])} 筆、書目 {len(src['books'])} 本、分類 {len(src['categories'])} 類、會員 {len(src['members'])} 位")
    top, bottom = report.iloc[0], report.iloc[-1]
    best = report.loc[report["每冊平均借閱次數"].idxmax()]
    print("\n📊 【分類借閱比較】")
    print(f"  - 借閱最多：{top['分類名稱']}（{top['借閱次數']} 次，館藏 {top['館藏冊數']} 本）")
    print(f"  - 借閱最少：{bottom['分類名稱']}（{bottom['借閱次數']} 次，館藏 {bottom['館藏冊數']} 本）")
    print(f"  - 每冊平均借閱最高：{best['分類名稱']}（{best['每冊平均借閱次數']} 次／本）")
    print(f"\n✅ 成果已成功匯出至：{OUTPUT_FILE.relative_to(BASE_DIR)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
