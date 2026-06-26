from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from pathlib import Path
import pandas as pd

def export_to_pdf(df: pd.DataFrame, output_path: Path) -> None:
    
    # 註冊可顯示中文的字型（macOS / Linux 常可直接使用）
    font_name = "STSong-Light"
    pdfmetrics.registerFont(UnicodeCIDFont(font_name))

    # 挑選適合放進報表的欄位，避免欄位太多導致版面混亂
    preferred_columns = ["sno", "sna", "sarea", "ar", "tot", "sbi", "bemp", "mday"]
    columns = [col for col in preferred_columns if col in df.columns]

    if not columns:
        print("找不到可輸出的欄位，無法建立 PDF。")
        return

    table_rows = df[columns].fillna("").astype(str).values.tolist()
    rows_per_page = 35

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=landscape(A4),
        rightMargin=18,
        leftMargin=18,
        topMargin=18,
        bottomMargin=18,
    )

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    title_style.fontName = font_name

    story = [
        Paragraph("YouBike 即時資料報表", title_style),
        Spacer(1, 12),
    ]

    for index in range(0, len(table_rows), rows_per_page):
        chunk = table_rows[index:index + rows_per_page]
        table_data = [columns] + chunk

        col_widths = []
        for col in columns:
            if col in ("sna", "ar"):
                col_widths.append(135)
            elif col == "mday":
                col_widths.append(120)
            else:
                col_widths.append(62)

        table = Table(table_data, repeatRows=1, colWidths=col_widths)
        table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (-1, -1), font_name),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )

        story.append(table)

        if index + rows_per_page < len(table_rows):
            story.append(PageBreak())

    doc.build(story)
    print(f"PDF 已產生：{output_path}")