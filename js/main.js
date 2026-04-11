/**
 * Caleb's Space — Main JS
 */

(function () {
  "use strict";

  /* ---- Sticky header shadow ---- */
  const header = document.getElementById("site-header");
  if (header) {
    window.addEventListener("scroll", () => {
      header.classList.toggle("scrolled", window.scrollY > 20);
    }, { passive: true });
  }

  /* ---- Mobile hamburger ---- */
  const hamburger = document.getElementById("hamburger");
  const mainNav   = document.getElementById("main-nav");
  if (hamburger && mainNav) {
    hamburger.addEventListener("click", () => {
      const open = mainNav.classList.toggle("open");
      hamburger.setAttribute("aria-expanded", open);
      // animate bars → X
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

    // close on outside click
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

  /* ---- Scroll reveal ---- */
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
    // fallback: show all immediately
    revealEls.forEach((el) => el.classList.add("visible"));
  }

  /* ---- Active nav highlight based on current page ---- */
  const path = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav-link").forEach((link) => {
    const href = link.getAttribute("href") || "";
    if (href === path || (path === "index.html" && href === "index.html")) {
      link.style.fontWeight = "700";
      link.style.color = "var(--text-primary)";
    }
  });

  /* ---- Smooth anchor scroll for # links ---- */
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (e) => {
      const target = document.querySelector(a.getAttribute("href"));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });

})();
