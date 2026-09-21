/**
 * Caleb's Space — Novel / Love board
 *
 * 设计变更（2026-09-22）：
 *   - 整板块（小说）已取消访问码，用户直接进入，无需密码。
 *   - 仅「恋爱」分栏需要密码（Aleen）。
 *   - 每次切换到「恋爱」分栏都会重新要求输入密码（不写入 localStorage，
 *     刷新或切走再切回都需重新验证）。
 *
 * 安全说明：
 *   纯前端密码，源码可见，仅作"礼貌性拦截"——挡住随意访问的陌生人，
 *   挡不住技术破解。如需真正安全，需要后端验证（不在当前架构内）。
 */

(function () {
  "use strict";

  /* ============================================================
   * 栏目切换（小说 / 恋爱）
   * ============================================================ */
  const tabs = document.querySelectorAll(".novel-tab");
  const panels = {
    fiction: document.getElementById("panel-fiction"),
    love:    document.getElementById("panel-love")
  };

  /* ============================================================
   * 恋爱栏密码 — Aleen
   *   每次进入恋爱分栏都需重新验证；不持久化，关闭即失效。
   * ============================================================ */
  const LOVE_PASSWORD = "Aleen";
  const loveGate    = document.getElementById("love-gate");
  const loveContent = document.getElementById("love-content");
  const loveForm    = document.getElementById("love-gate-form");
  const loveInput   = document.getElementById("love-gate-input");
  const loveError   = document.getElementById("love-gate-error");

  function showLoveContent() {
    if (loveGate)    loveGate.classList.add("hidden");
    if (loveContent) loveContent.classList.add("is-unlocked");
  }
  function showLoveGate() {
    if (loveGate)    loveGate.classList.remove("hidden");
    if (loveContent) loveContent.classList.remove("is-unlocked");
    if (loveInput) { loveInput.value = ""; setTimeout(() => loveInput.focus(), 100); }
    if (loveError)   loveError.classList.remove("show");
  }
  function tryLoveAccess() {
    if (!loveInput) return;
    if (loveInput.value.trim() === LOVE_PASSWORD) {
      showLoveContent();
    } else {
      if (loveError) {
        loveError.classList.add("show");
        setTimeout(() => loveError.classList.remove("show"), 3000);
      }
      loveInput.value = "";
      loveInput.focus();
    }
  }

  function switchTab(name) {
    tabs.forEach(t => t.classList.toggle("is-active", t.dataset.tab === name));
    Object.keys(panels).forEach(k => {
      if (panels[k]) panels[k].classList.toggle("is-active", k === name);
    });
    // 每次进入恋爱板块都重新验证密码
    if (name === "love") showLoveGate();
  }

  /* ---- Placeholder 翻译（复用主站 langRefresh）----
   * main.js 的 applyLang 不处理 placeholder 属性，
   * 这里单独监听 langRefresh 事件来切换中英文 placeholder。
   */
  function translateLovePlaceholder() {
    if (!loveInput) return;
    const lang = localStorage.getItem("caleb-lang") || "zh";
    const txt = lang === "en"
      ? loveInput.getAttribute("data-en-placeholder")
      : loveInput.getAttribute("data-zh-placeholder");
    if (txt) loveInput.placeholder = txt;
  }

  /* ---- 初始化 ---- */
  if (loveGate && loveContent) {
    showLoveGate(); // 默认即门禁状态，等待输入
    if (loveForm) {
      loveForm.addEventListener("submit", (e) => {
        e.preventDefault();
        tryLoveAccess();
      });
    }
    translateLovePlaceholder();
    document.addEventListener("langRefresh", translateLovePlaceholder);
  }
  tabs.forEach(t => t.addEventListener("click", () => switchTab(t.dataset.tab)));

})();
