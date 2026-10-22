/**
 * 【看懂資料與選對圖表】章節專用導航模組
 */
(function() {
  const navItems = [
    { title: "章節大廳", url: "./index.html" },
    { title: "🎯 五大問題與圖表動畫", url: "./question-types.html" },
    { title: "📐 圖表名稱與坐標軸", url: "./chart-vocabulary.html" },
    { title: "📊 資料條件挑圖指南", url: "./chart-matrix.html" },
    { title: "⚡ 欄位組合速查", url: "./field-combinations.html" }
  ];

  function renderNavbar() {
    const currentPath = window.location.pathname.split("/").pop() || "index.html";

    const header = document.createElement("header");
    header.style.cssText = "background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(12px); border-bottom: 1px solid #E2E8F0; position: sticky; top: 0; z-index: 100;";
    header.innerHTML = `
      <div style="max-width: 1200px; margin: 0 auto; padding: 12px 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <a href="../index.html" style="font-size: 0.82rem; font-weight: 700; color: #64748B; text-decoration: none; padding: 4px 8px; border-radius: 6px; background: #F1F5F9; display: flex; align-items: center; gap: 4px;">
            <span>🏠 全課程總首頁</span>
          </a>
          <span style="color: #CBD5E1;">/</span>
          <a href="./index.html" style="display: flex; align-items: center; gap: 6px; font-weight: 800; font-size: 1.05rem; color: #0F172A; text-decoration: none;">
            <span>📊 看懂資料與選對圖表</span>
          </a>
        </div>
        <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
          ${navItems.map(item => {
            const isActive = currentPath === item.url.replace("./", "") || (currentPath === "" && item.url === "./index.html");
            return `
              <a href="${item.url}" style="
                text-decoration: none;
                font-size: 0.85rem;
                font-weight: 700;
                padding: 6px 12px;
                border-radius: 6px;
                transition: all 0.2s ease;
                color: ${isActive ? '#FFFFFF' : '#475569'};
                background: ${isActive ? '#2563EB' : 'transparent'};
                border: 1px solid ${isActive ? '#2563EB' : 'transparent'};
              ">${item.title}</a>
            `;
          }).join("")}
          <a href="https://github.com/roberthsu2003/PythonForDataAnalysis" target="_blank" style="
            text-decoration: none;
            font-size: 0.85rem;
            font-weight: 600;
            padding: 5px 10px;
            color: #64748B;
            border-left: 1px solid #CBD5E1;
            margin-left: 4px;
          ">GitHub ↗</a>
        </div>
      </div>
    `;

    const oldHeader = document.querySelector("header");
    if (oldHeader) {
      oldHeader.replaceWith(header);
    } else {
      document.body.insertBefore(header, document.body.firstChild);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderNavbar);
  } else {
    renderNavbar();
  }
})();
