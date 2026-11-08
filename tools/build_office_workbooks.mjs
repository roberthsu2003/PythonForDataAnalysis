// 使用 @oai/artifact-tool，搭配 build_office_materials.py 產生的固定資料。
import fs from 'node:fs/promises';
import path from 'node:path';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const manifest = JSON.parse(await fs.readFile(process.argv[2] ?? '/tmp/office-materials.json', 'utf8'));
const previews = '/tmp/office-excel-previews';
await fs.mkdir(previews, {recursive:true});
for (const c of manifest.cases) {
  const wb = Workbook.create();
  for (const source of c.sheets) {
    const sheet = wb.worksheets.add(source.name);
    const count = source.rows.length + 1;
    const last = String.fromCharCode(64 + source.headers.length);
    sheet.getRange(`A1:${last}${count}`).values = [source.headers, ...source.rows];
    sheet.showGridLines = false;
    sheet.getRange(`A1:${last}${count}`).format.font = {name:'Arial',size:11};
    sheet.getRange(`A1:${last}${count}`).format.rowHeight = 25;
    sheet.getRange(`A1:${last}1`).format = {fill:'#243B53',font:{bold:true,color:'#FFFFFF'},horizontalAlignment:'center'};
    for (let col=0; col<source.headers.length; col++) {
      const letter = String.fromCharCode(65+col);
      sheet.getRange(`${letter}1:${letter}${count}`).format.columnWidth = Math.max(17, source.headers[col].length*2+3);
      if (source.rows.some(r => typeof r[col] === 'number')) {
        sheet.getRange(`${letter}2:${letter}${count}`).setNumberFormat('#,##0');
      }
    }
    sheet.freezePanes.freezeRows(1);
    sheet.tables.add(`A1:${last}${count}`,true,`Office${c.name.slice(0,2)}${source.name === '資料' ? 'Data' : 'Receipts'}`);
  }
  wb.recalculate();
  for (const source of c.sheets) {
    const last = String.fromCharCode(64+source.headers.length);
    const inspected = await wb.inspect({kind:'table',range:`'${source.name}'!A1:${last}${source.rows.length+1}`,include:'values',maxChars:700});
    if (!inspected.ndjson) throw new Error(`Cannot inspect ${c.name}`);
    const image = await wb.render({sheetName:source.name,range:`A1:${last}${source.rows.length+1}`,scale:1.5,format:'png'});
    await fs.writeFile(path.join(previews,`${c.name}_${source.name}.png`), new Uint8Array(await image.arrayBuffer()));
  }
  // 匯出器會附帶檢查紀錄，先在暫存區匯出，只交付 Excel 本體。
  const exported = path.join(previews, `${c.name}.xlsx`);
  await (await SpreadsheetFile.exportXlsx(wb)).save(exported);
  await fs.copyFile(exported, path.join(manifest.destination,`${c.name}.xlsx`));
  console.log(`已匯出 ${c.name}`);
}
