/**
 * Caleb's Space — Article Detail Page Logic (post.js)
 * Handles: URL parameter routing, article data injection,
 *         category-specific styling, breadcrumb updates
 */

(function () {
  "use strict";

  /* ================================================================
   * ARTICLE DATABASE
   * Add new articles here. Fields:
   *   cat      : 'life' | 'travel' | 'pro' | 'think'
   *   slug     : unique URL-safe identifier
   *   title_zh / title_en
   *   excerpt_zh / excerpt_en
   *   date     : ISO date string e.g. '2026-04-22'
   *   date_zh  / date_en
   *   tags     : array of tag objects { label_zh, label_en, cat }
   *   cover_icon : emoji shown in placeholder cover
   *   author   : always 'Caleb'
   *   read_time: string e.g. '约 5 分钟'
   * ================================================================ */
  const ARTICLES = [
    {
      cat: "pro",
      slug: "day-one-gmp-mindset",
      title_zh: "细胞培养工程师的第一天：从实验室到 GMP 车间的心态切换",
      title_en: "Day One as a Cell Culture Engineer: From Lab Bench to GMP Manufacturing",
      excerpt_zh: "从科研实验室进入工业化生产车间，不只是环境的变化，更是思维框架的重构……",
      excerpt_en: "Moving from a research lab to an industrial GMP facility is not just a change of environment, but a reconstruction of mental frameworks…",
      date: "2026-04-22",
      date_zh: "2026年4月22日",
      date_en: "April 22, 2026",
      read_time: "约 5 分钟",
      read_time_en: "5 min read",
      cover_icon: "🔬",
      tags: [
        { label_zh: "细胞培养", label_en: "Cell Culture", cat: "pro" },
        { label_zh: "GMP", label_en: "GMP", cat: "pro" },
        { label_zh: "职场", label_en: "Career", cat: "pro" },
      ],
      // Which section page to link back to
      section_page: "professional.html",
      section_label_zh: "专业思考",
      section_label_en: "Professional",
      section_color: "pro",
    },
    {
      cat: "think",
      slug: "first-principles-biopharma",
      title_zh: "为什么「第一性原理」在生物制药里格外难用",
      title_en: "Why 'First Principles' Are Especially Hard to Apply in Biopharma",
      excerpt_zh: "物理世界有确定的公理，生物系统却充满随机性与涌现性，从底层重新思考这个问题……",
      excerpt_en: "The physical world has definite axioms, but biological systems are full of randomness and emergence…",
      date: "2026-04-20",
      date_zh: "2026年4月20日",
      date_en: "April 20, 2026",
      read_time: "约 6 分钟",
      read_time_en: "6 min read",
      cover_icon: "🧠",
      tags: [
        { label_zh: "思维", label_en: "Thinking", cat: "think" },
        { label_zh: "生物制药", label_en: "Biopharma", cat: "pro" },
      ],
      section_page: "thinking.html",
      section_label_zh: "思维提升",
      section_label_en: "Deep Thinking",
      section_color: "think",
    },
    {
      cat: "life",
      slug: "last-holiday-before-work",
      title_zh: "入职前的最后一个假期：我做了什么",
      title_en: "My Last Holiday Before Work: What I Did",
      excerpt_zh: "在进入职场之前，给自己留下一段真正属于自己的时间……",
      excerpt_en: "Before entering the workforce, I gave myself a stretch of time that truly belonged to me…",
      date: "2026-04-18",
      date_zh: "2026年4月18日",
      date_en: "April 18, 2026",
      read_time: "约 3 分钟",
      read_time_en: "3 min read",
      cover_icon: "☀️",
      tags: [
        { label_zh: "日常", label_en: "Daily", cat: "life" },
        { label_zh: "旅行", label_en: "Travel", cat: "travel" },
      ],
      section_page: "life.html",
      section_label_zh: "日常生活",
      section_label_en: "Daily Life",
      section_color: "life",
    },
    {
      cat: "travel",
      slug: "qinghai-lake-solo",
      title_zh: "一个人的青海湖：当科学思维遭遇自然震撼",
      title_en: "Qinghai Lake Solo: When Scientific Thinking Meets Awe of Nature",
      excerpt_zh: "站在湖边的那一刻，我突然理解了为什么科学家也需要「无用的感动」……",
      excerpt_en: "Standing by the lake, I suddenly understood why scientists also need 'useless wonder'…",
      date: "2026-04-15",
      date_zh: "2026年4月15日",
      date_en: "April 15, 2026",
      read_time: "约 4 分钟",
      read_time_en: "4 min read",
      cover_icon: "🏔️",
      tags: [
        { label_zh: "旅行", label_en: "Travel", cat: "travel" },
        { label_zh: "青海湖", label_en: "Qinghai Lake", cat: "travel" },
      ],
      section_page: "travel.html",
      section_label_zh: "旅行探索",
      section_label_en: "Travel",
      section_color: "travel",
    },
  ];

  /* ================================================================
   * ROUTING: parse URL params
   *   ?cat=pro&slug=day-one-gmp-mindset
   * Fallback: show demo article (first in ARTICLES array)
   * ================================================================ */
  function getParams() {
    const p = new URLSearchParams(window.location.search);
    return {
      cat:  p.get("cat")  || "pro",
      slug: p.get("slug") || "day-one-gmp-mindset",
    };
  }

  function findArticle(cat, slug) {
    return ARTICLES.find(
      (a) => a.cat === cat && a.slug === slug
    ) || ARTICLES[0]; // fallback to first
  }

  /* ================================================================
   * HELPERS
   * ================================================================ */
  function qs(sel) { return document.querySelector(sel); }

  function tagHTML(tag) {
    return `<span class="tag tag-${tag.cat}">${tag.label_zh}</span>`;
  }

  function tagHTMLForLang(tag, lang) {
    const label = lang === "en" ? tag.label_en : tag.label_zh;
    return `<span class="tag tag-${tag.cat}">${label}</span>`;
  }

  /* ================================================================
   * INJECT ARTICLE DATA
   * ================================================================ */
  function applyArticleData(article) {
    const lang = localStorage.getItem("caleb-lang") || "zh";

    // --- Title + lang attribute ---
    document.title = `${lang === "en" ? article.title_en : article.title_zh} — Caleb's Space`;

    // --- Top accent bar ---
    const topBar = qs("#post-top-bar");
    if (topBar) topBar.className = `post-top-bar post-top-bar-${article.cat}`;

    // --- Breadcrumb ---
    const catLink = qs("#breadcrumb-cat");
    if (catLink) {
      catLink.href = article.section_page;
      catLink.textContent = lang === "en" ? article.section_label_en : article.section_label_zh;
    }
    const breadcrumbTitle = qs("#breadcrumb-title");
    if (breadcrumbTitle) {
      breadcrumbTitle.textContent = lang === "en" ? article.title_en : article.title_zh;
    }

    // --- Tags (header) ---
    const tagsEl = qs("#post-tags");
    if (tagsEl) {
      tagsEl.innerHTML = article.tags.map((t) => tagHTMLForLang(t, lang)).join("");
    }

    // --- Title (data attributes for i18n) ---
    const titleEl = qs("#post-title");
    if (titleEl) {
      titleEl.setAttribute("data-zh", article.title_zh);
      titleEl.setAttribute("data-en", article.title_en);
      titleEl.textContent = lang === "en" ? article.title_en : article.title_zh;
    }

    // --- Date ---
    const dateEl = qs("#post-date");
    if (dateEl) {
      dateEl.textContent = lang === "en" ? article.date_en : article.date_zh;
      dateEl.setAttribute("datetime", article.date);
    }

    // --- Read time ---
    const readTimeEl = qs("#post-read-time");
    if (readTimeEl) {
      readTimeEl.setAttribute("data-zh", article.read_time + "阅读");
      readTimeEl.setAttribute("data-en", article.read_time_en);
      readTimeEl.textContent = lang === "en" ? article.read_time_en : article.read_time;
    }

    // --- Cover ---
    const coverPlaceholder = qs(".post-cover-placeholder");
    if (coverPlaceholder) {
      coverPlaceholder.innerHTML = `<span>${article.cover_icon}</span>`;
      coverPlaceholder.className = `post-cover-placeholder cover-${article.cat}`;
    }

    // --- End tags ---
    const endTagsEl = qs("#post-end-tags");
    if (endTagsEl) {
      endTagsEl.innerHTML = article.tags.map((t) => tagHTMLForLang(t, lang)).join("");
    }

    // --- Back button ---
    const backBtn = qs("#post-back-btn");
    if (backBtn) backBtn.href = article.section_page;

    // --- Prev / Next (placeholder: show article list order) ---
    const idx = ARTICLES.findIndex(
      (a) => a.cat === article.cat && a.slug === article.slug
    );
    const prevArticle = idx > 0 ? ARTICLES[idx - 1] : null;
    const nextArticle = idx < ARTICLES.length - 1 ? ARTICLES[idx + 1] : null;

    const prevBtn = qs("#post-nav-prev");
    const nextBtn = qs("#post-nav-next");

    if (prevBtn) {
      if (prevArticle) {
        prevBtn.href = `post.html?cat=${prevArticle.cat}&slug=${prevArticle.slug}`;
        const prevTitleEl = qs("#post-nav-prev-title");
        if (prevTitleEl) {
          prevTitleEl.setAttribute("data-zh", prevArticle.title_zh);
          prevTitleEl.setAttribute("data-en", prevArticle.title_en);
          prevTitleEl.textContent = lang === "en" ? prevArticle.title_en : prevArticle.title_zh;
        }
      } else {
        prevBtn.style.visibility = "hidden";
      }
    }

    if (nextBtn) {
      if (nextArticle) {
        nextBtn.href = `post.html?cat=${nextArticle.cat}&slug=${nextArticle.slug}`;
        const nextTitleEl = qs("#post-nav-next-title");
        if (nextTitleEl) {
          nextTitleEl.setAttribute("data-zh", nextArticle.title_zh);
          nextTitleEl.setAttribute("data-en", nextArticle.title_en);
          nextTitleEl.textContent = lang === "en" ? nextArticle.title_en : nextArticle.title_zh;
        }
      } else {
        nextBtn.style.visibility = "hidden";
      }
    }
  }

  /* ================================================================
   * I18N REFRESH on language toggle
   * main.js fires a custom event 'langRefresh' when language changes
   * ================================================================ */
  document.addEventListener("langRefresh", function () {
    const { cat, slug } = getParams();
    const article = findArticle(cat, slug);
    applyArticleData(article);
  });

  /* ================================================================
   * INIT
   * ================================================================ */
  function init() {
    const { cat, slug } = getParams();
    const article = findArticle(cat, slug);
    applyArticleData(article);
  }

  // Run after DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
