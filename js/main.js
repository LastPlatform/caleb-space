/**
 * Caleb's Space — Main JS
 * Features: sticky header, hamburger menu, scroll reveal,
 *           active nav highlight, smooth scroll,
 *           i18n (zh/en) language toggle
 */

(function () {
  "use strict";

  /* ================================================================
   * 1. STICKY HEADER SHADOW
   * ================================================================ */
  const header = document.getElementById("site-header");
  if (header) {
    window.addEventListener("scroll", () => {
      header.classList.toggle("scrolled", window.scrollY > 20);
    }, { passive: true });
  }

  /* ================================================================
   * 2. MOBILE HAMBURGER
   * ================================================================ */
  const hamburger = document.getElementById("hamburger");
  const mainNav   = document.getElementById("main-nav");
  if (hamburger && mainNav) {
    hamburger.addEventListener("click", () => {
      const open = mainNav.classList.toggle("open");
      hamburger.setAttribute("aria-expanded", open);
      const bars = hamburger.querySelectorAll("span");
      if (open) {
        bars[0].style.transform = "translateY(7px) rotate(45deg)";
        bars[1].style.opacity   = "0";
        bars[2].style.transform = "translateY(-7px) rotate(-45deg)";
      } else {
        bars[0].style.transform = "";
        bars[1].style.opacity   = "";
        bars[2].style.transform = "";
      }
    });
    document.addEventListener("click", (e) => {
      if (!header.contains(e.target)) {
        mainNav.classList.remove("open");
        hamburger.removeAttribute("aria-expanded");
        hamburger.querySelectorAll("span").forEach(s => {
          s.style.transform = "";
          s.style.opacity   = "";
        });
      }
    });
  }

  /* ================================================================
   * 3. SCROLL REVEAL
   * ================================================================ */
  const revealEls = document.querySelectorAll(".reveal");
  if (revealEls.length && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("visible"));
  }

  /* ================================================================
   * 4. ACTIVE NAV HIGHLIGHT
   * ================================================================ */
  const path = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav-link").forEach((link) => {
    const href = link.getAttribute("href") || "";
    if (href === path || (path === "index.html" && href === "index.html")) {
      link.style.fontWeight = "700";
      link.style.color = "var(--text-primary)";
    }
  });

  /* ================================================================
   * 5. SMOOTH ANCHOR SCROLL
   * ================================================================ */
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (e) => {
      const target = document.querySelector(a.getAttribute("href"));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });

  /* ================================================================
   * 6. I18N — LANGUAGE TOGGLE (ZH / EN)
   * ================================================================
   * How it works:
   *   - Every translatable element has data-zh="中文" data-en="English"
   *   - On toggle, we walk all [data-zh] elements and swap .textContent
   *   - The <html lang> attribute is also updated for accessibility
   *   - Current language is persisted in localStorage("lang")
   * ================================================================ */
  const LANG_KEY = "caleb-lang";

  function applyLang(lang) {
    document.documentElement.setAttribute("lang", lang === "en" ? "en" : "zh-CN");

    // swap all translatable text nodes
    document.querySelectorAll("[data-zh]").forEach((el) => {
      const txt = lang === "en" ? el.getAttribute("data-en") : el.getAttribute("data-zh");
      if (txt !== null) el.textContent = txt;
    });

    // swap translatable placeholders / aria-labels
    document.querySelectorAll("[data-zh-label]").forEach((el) => {
      const lbl = lang === "en"
        ? el.getAttribute("data-en-label")
        : el.getAttribute("data-zh-label");
      if (lbl !== null) el.setAttribute("aria-label", lbl);
    });

    // update toggle button appearance
    const btn = document.getElementById("lang-toggle");
    if (btn) {
      btn.textContent = lang === "en" ? "中文" : "EN";
      btn.setAttribute("title", lang === "en" ? "切换到中文" : "Switch to English");
    }

    // persist
    localStorage.setItem(LANG_KEY, lang);
  }

  function initLang() {
    // read saved preference, default to zh
    const saved = localStorage.getItem(LANG_KEY) || "zh";
    applyLang(saved);

    const btn = document.getElementById("lang-toggle");
    if (btn) {
      btn.addEventListener("click", () => {
        const current = localStorage.getItem(LANG_KEY) || "zh";
        applyLang(current === "zh" ? "en" : "zh");
      });
    }
  }

  // run after DOM is ready (script is at bottom of body so DOM is ready)
  initLang();

})();
