/**
 * 共用頂部導覽列模組
 * 未來若新增獨立網頁，只需在此處 links 陣列加入一筆，所有頁面導覽列自動同步！
 */
(function() {
  const navItems = [
    { title: "🏠 互動首頁", url: "./index.html" },
    { title: "🎯 五大問題與圖表動畫", url: "./question-types.html" },
    { title: "⚡ 欄位組合速查工具", url: "./field-combinations.html" }
  ];

  function renderNavbar() {
    const currentPath = window.location.pathname.split("/").pop() || "index.html";

    const header = document.createElement("header");
    header.innerHTML = `
      <div class="nav-container" style="max-width: 1200px; margin: 0 auto; padding: 12px 24px; display: flex; justify-content: space-between; align-items: center;">
        <a href="./index.html" class="logo" style="display: flex; align-items: center; gap: 8px; font-weight: 800; font-size: 1.15rem; color: #0F172A; text-decoration: none;">
          <span>📊 Python 資料分析</span>
          <span style="font-size: 0.75rem; background: #2563EB; color: #FFF; padding: 3px 8px; border-radius: 999px; font-weight: 700;">互動教材</span>
        </a>
        <div class="nav-tabs" style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
          ${navItems.map(item => {
            const isActive = currentPath === item.url.replace("./", "") || (currentPath === "" && item.url === "./index.html");
            return `
              <a href="${item.url}" class="nav-tab-link ${isActive ? 'active' : ''}" style="
                text-decoration: none;
                font-size: 0.88rem;
                font-weight: 700;
                padding: 6px 14px;
                border-radius: 8px;
                transition: all 0.2s ease;
                color: ${isActive ? '#FFFFFF' : '#475569'};
                background: ${isActive ? '#2563EB' : 'transparent'};
              ">${item.title}</a>
            `;
          }).join("")}
          <a href="https://github.com/roberthsu2003/PythonForDataAnalysis" target="_blank" style="
            text-decoration: none;
            font-size: 0.88rem;
            font-weight: 600;
            padding: 6px 12px;
            color: #64748B;
            border-left: 1px solid #CBD5E1;
            margin-left: 4px;
          ">GitHub ↗</a>
        </div>
      </div>
    `;

    // 插入至 body 開頭
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
