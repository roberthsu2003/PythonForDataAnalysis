"""
01｜班級段考成績分析與報表自動化生成腳本
"""
from pathlib import Path
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "scores.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "成績報表.xlsx"

def load_and_validate_data(csv_path: Path) -> pd.DataFrame:
    """讀取資料並驗證欄位角色與缺考防呆"""
    if not csv_path.exists():
        raise FileNotFoundError(f"找不到資料檔案：{csv_path}")
    df = pd.read_csv(csv_path)
    return df

def calculate_subject_stats(df: pd.DataFrame, subjects: list) -> pd.DataFrame:
    """計算各科統計數據（排除缺考 NaN，不可當 0 分）"""
    stats = pd.DataFrame({
        "科目": subjects,
        "全班平均": df[subjects].mean().round(1).values,
        "最高分": df[subjects].max().values,
        "最低分": df[subjects].min().values,
        "標準差": df[subjects].std().round(1).values,
        "缺考人數": df[subjects].isna().sum().values
    })
    return stats

def calculate_student_rankings(df: pd.DataFrame, subjects: list) -> pd.DataFrame:
    """計算已考科目總分；只有五科完整者參與班級排名。"""
    result = df.copy()
    result["應考科數"] = result[subjects].notna().sum(axis=1)
    result["總分"] = result[subjects].sum(axis=1)
    result["平均"] = result[subjects].mean(axis=1).round(1)
    complete = result["應考科數"].eq(len(subjects))
    result["排名"] = result["總分"].where(complete).rank(ascending=False, method="min").astype("Int64")
    result["成績狀態"] = complete.map({True: "完整", False: "缺考，暫不排名"})
    
    result = result.sort_values(["排名", "座號"], na_position="last").reset_index(drop=True)
    cols = ["排名", "座號", "姓名"] + subjects + ["應考科數", "總分", "平均", "成績狀態"]
    return result[cols]

def export_to_styled_excel(stats_df: pd.DataFrame, ranked_df: pd.DataFrame, output_path: Path):
    """將分析結果匯出為格式化 Excel 報表（不及格紅字高亮、凍結窗格）"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        ranked_df.to_excel(writer, sheet_name="學生名次與成績", index=False)
        stats_df.to_excel(writer, sheet_name="各科統計摘要", index=False)
        
    wb = openpyxl.load_workbook(output_path)
    
    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    header_font = Font(name="微軟正黑體", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="微軟正黑體", size=10)
    fail_font = Font(name="微軟正黑體", size=10, bold=True, color="C00000")
    fail_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
    center_align = Alignment(horizontal="center", vertical="center")
    
    for ws in wb.worksheets:
        ws.views.sheetView[0].showGridLines = True
        ws.freeze_panes = "A2"
        score_columns = {cell.column for cell in ws[1] if cell.value in ["國文", "英文", "數學", "自然", "社會", "平均"]}
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = center_align
        
        for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            for cell in row:
                cell.font = data_font
                cell.alignment = center_align
                if cell.column in score_columns and isinstance(cell.value, (int, float)) and cell.value < 60:
                    cell.font = fail_font
                    cell.fill = fail_fill
        
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = max(max_len * 2, 12)
            
    wb.save(output_path)

def main():
    print("=" * 50)
    print("🚀 開始執行班級段考成績自動化分析腳本...")
    print("=" * 50)
    
    df = load_and_validate_data(DATA_PATH)
    subjects = ["國文", "英文", "數學", "自然", "社會"]
    
    stats_df = calculate_subject_stats(df, subjects)
    ranked_df = calculate_student_rankings(df, subjects)
    
    export_to_styled_excel(stats_df, ranked_df, OUTPUT_FILE)
    
    min_sub = stats_df.loc[stats_df["全班平均"].idxmin()]
    max_sub = stats_df.loc[stats_df["全班平均"].idxmax()]
    complete = ranked_df["成績狀態"].eq("完整")
    top3 = ranked_df[complete].head(3)
    needs_help = ranked_df[complete & ((ranked_df["平均"] < 60) | (ranked_df[subjects].min(axis=1) < 50))]
    absent = ranked_df[~complete]
    
    print(f"\n📊 【各科平均分比較】")
    print(f"  - 全班平均最低科目：{min_sub['科目']}（平均 {min_sub['全班平均']} 分）")
    print(f"  - 全班最高科目：{max_sub['科目']}（平均達 {max_sub['全班平均']} 分）")
    
    print(f"\n🏆 【全班前 3 名優等生】")
    for _, row in top3.iterrows():
        print(f"  - 第 {row['排名']} 名：{row['姓名']}（總分 {row['總分']:.0f}，平均 {row['平均']} 分）")
        
    print(f"\n⚠️ 【需重點輔導與補救學生】共 {len(needs_help)} 位")
    print(f"📝 【缺考，暫不排名】共 {len(absent)} 位；總分僅採計已考科目")
    print(f"\n✅ 成果已成功匯出至：{OUTPUT_FILE.relative_to(BASE_DIR)}")
    print("=" * 50)

if __name__ == "__main__":
    main()
