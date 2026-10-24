// 程式碼上色＋「複製」按鈕
document.querySelectorAll('.md pre > code').forEach((code) => {
  if (code.classList.contains('language-text')) return;   // 示意圖不需要上色與複製
  if (window.hljs) hljs.highlightElement(code);
  const btn = document.createElement('button');
  btn.className = 'copy-btn';
  btn.type = 'button';
  btn.textContent = '複製';
  btn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(code.innerText);
      btn.textContent = '已複製 ✓';
    } catch (e) {
      btn.textContent = '請手動選取';
    }
    setTimeout(() => { btn.textContent = '複製'; }, 1600);
  });
  code.parentElement.appendChild(btn);
});

// 手機版：展開／收合章節清單
const side = document.getElementById('sidebar');
const toggle = side && side.querySelector('.side-toggle');
if (toggle) {
  toggle.addEventListener('click', () => {
    const open = side.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });
}

// 自我檢查清單：勾選狀態記在這台瀏覽器
document.querySelectorAll('.task-list-item input[type=checkbox]').forEach((box, i) => {
  const key = 'pfda:' + location.pathname + ':' + i;
  box.disabled = false;
  try { box.checked = localStorage.getItem(key) === '1'; } catch (e) { /* 無法使用儲存空間時就不記錄 */ }
  box.addEventListener('change', () => {
    try { localStorage.setItem(key, box.checked ? '1' : '0'); } catch (e) { /* 同上 */ }
  });
});
