/**
 * Caleb's Space — Novel Gate
 * 访问码门禁：未验证时显示遮罩，验证通过后显示小说正文
 *
 * 工作原理：
 *   - 进入 novel.html 时，检查 localStorage 是否有有效访问码
 *   - 没有 → 显示 #novel-gate 遮罩，隐藏 #novel-content
 *   - 输入正确访问码 → 写入 localStorage，显示正文
 *   - 改访问码后，老设备的 localStorage 值不再匹配，自动失效
 *
 * 安全性说明：
 *   纯前端访问码不是真正安全——任何人查看 JS 源码都能看到访问码。
 *   这适合"礼貌性拦截"，挡住随意访问的陌生人，挡不住技术破解。
 *   如需真正安全，需要后端验证（不在当前架构内）。
 */

(function () {
  "use strict";

  /* ============================================================
   * ⚠️ 访问码 — 改这里即可更换
   *    改后所有已验证设备会自动失效（需重新输入新码）
   * ============================================================ */
  const NOVEL_ACCESS_CODE = "caleb-novel-2026";
  const STORAGE_KEY = "novel-access-code";

  const gate    = document.getElementById("novel-gate");
  const content = document.getElementById("novel-content");
  const form    = document.getElementById("novel-gate-form");
  const input   = document.getElementById("novel-gate-input");
  const error   = document.getElementById("novel-gate-error");

  // 不在小说页（没有 gate / content 元素），跳过初始化
  if (!gate || !content) return;

  /* ---- 状态检查 ---- */
  function isGranted() {
    return localStorage.getItem(STORAGE_KEY) === NOVEL_ACCESS_CODE;
  }

  function grant() {
    localStorage.setItem(STORAGE_KEY, NOVEL_ACCESS_CODE);
  }

  /* ---- 显示控制 ---- */
  function showContent() {
    gate.classList.add("hidden");
    content.classList.add("unlocked");
    document.body.classList.remove("gate-active");
  }

  function showGate() {
    gate.classList.remove("hidden");
    content.classList.remove("unlocked");
    document.body.classList.add("gate-active");
    if (input) setTimeout(() => input.focus(), 100);
  }

  /* ---- 验证逻辑 ---- */
  function tryAccess() {
    if (!input) return;
    const value = input.value.trim();
    if (value === NOVEL_ACCESS_CODE) {
      grant();
      showContent();
    } else {
      if (error) {
        error.classList.add("show");
        setTimeout(() => error.classList.remove("show"), 3000);
      }
      input.value = "";
      input.focus();
    }
  }

  /* ---- Placeholder 翻译 ----
   * main.js 的 applyLang 不处理 placeholder 属性，
   * 这里单独监听 langRefresh 事件来切换中英文 placeholder。
   */
  function translatePlaceholder() {
    if (!input) return;
    const lang = localStorage.getItem("caleb-lang") || "zh";
    const txt = lang === "en"
      ? input.getAttribute("data-en-placeholder")
      : input.getAttribute("data-zh-placeholder");
    if (txt) input.placeholder = txt;
  }

  /* ---- 初始化 ---- */
  if (isGranted()) {
    showContent();
  } else {
    showGate();
  }
  translatePlaceholder();

  /* ---- 事件绑定 ---- */
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      tryAccess();
    });
  }

  // 监听语言切换（main.js 切换语言后会 dispatch langRefresh）
  document.addEventListener("langRefresh", translatePlaceholder);

  /* ---- 全局方法（调试/扩展用）----
   * 在浏览器控制台可以：
   *   __novelGate.lock()  — 强制锁定（清除验证状态）
   *   __novelGate.check() — 查看当前是否已验证
   */
  window.__novelGate = {
    lock:  () => { localStorage.removeItem(STORAGE_KEY); showGate(); },
    check: () => isGranted()
  };

})();
