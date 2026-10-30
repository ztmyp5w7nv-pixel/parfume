/* =========================================================
   AURA PARFUM - INTERACTIVE LOGIC & STORE COMPARISON
   Full Vanilla JS with Fetch API & Localhost Support
   ========================================================= */

let allPerfumes = [];
let currentCategory = "tümü";
let currentSort = "default";
let searchQuery = "";

// DOM Elements
const perfumesGrid = document.getElementById("perfumesGrid");
const searchInput = document.getElementById("searchInput");
const categoryPills = document.querySelectorAll(".cat-pill");
const sortSelect = document.getElementById("sortSelect");
const modalBackdrop = document.getElementById("modalBackdrop");
const modalContent = document.getElementById("modalContent");
const matrixTableBody = document.getElementById("matrixTableBody");

// View Tab Buttons
const tabGridBtn = document.getElementById("tabGridBtn");
const tabMatrixBtn = document.getElementById("tabMatrixBtn");
const tabPromptBtn = document.getElementById("tabPromptBtn");

const viewGrid = document.getElementById("viewGrid");
const viewMatrix = document.getElementById("viewMatrix");
const viewPrompt = document.getElementById("viewPrompt");

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  fetchPerfumes();
  setupEventListeners();
});

// Fetch Data from Localhost API (or fallback if opened via file://)
async function fetchPerfumes() {
  try {
    const res = await fetch("/api/perfumes");
    if (!res.ok) throw new Error("API hatası");
    allPerfumes = await res.json();
  } catch (err) {
    console.warn("API'den çekilemedi, yerleşik veri kümesi kullanılıyor:", err);
    // In case static HTML is opened directly without server.py
    if (window.__PERFUMES_DATA) {
      allPerfumes = window.__PERFUMES_DATA;
    }
  }
  renderAllViews();
}

function setupEventListeners() {
  // Live Search
  searchInput.addEventListener("input", (e) => {
    searchQuery = e.target.value.toLowerCase().trim();
    renderPerfumesGrid();
    renderMatrixTable();
  });

  // Keyboard shortcut: CMD+K or Ctrl+K or / to focus search
  window.addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "k") {
      e.preventDefault();
      searchInput.focus();
    } else if (e.key === "/" && document.activeElement !== searchInput) {
      e.preventDefault();
      searchInput.focus();
    }
  });

  // Category Filtering
  categoryPills.forEach((pill) => {
    pill.addEventListener("click", () => {
      categoryPills.forEach((p) => p.classList.remove("active"));
      pill.classList.add("active");
      currentCategory = pill.dataset.category;
      renderPerfumesGrid();
      renderMatrixTable();
    });
  });

  // Sorting
  sortSelect.addEventListener("change", (e) => {
    currentSort = e.target.value;
    renderPerfumesGrid();
    renderMatrixTable();
  });

  // Tab Switching
  tabGridBtn.addEventListener("click", () => switchView("grid"));
  tabMatrixBtn.addEventListener("click", () => switchView("matrix"));
  tabPromptBtn.addEventListener("click", () => switchView("prompt"));

  // Modal Close on backdrop click
  modalBackdrop.addEventListener("click", (e) => {
    if (e.target === modalBackdrop) {
      closeModal();
    }
  });

  // Close on Escape key
  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modalBackdrop.classList.contains("active")) {
      closeModal();
    }
  });
}

function switchView(viewName) {
  [tabGridBtn, tabMatrixBtn, tabPromptBtn].forEach((btn) => btn.classList.remove("active"));
  [viewGrid, viewMatrix, viewPrompt].forEach((view) => (view.style.display = "none"));

  if (viewName === "grid") {
    tabGridBtn.classList.add("active");
    viewGrid.style.display = "block";
  } else if (viewName === "matrix") {
    tabMatrixBtn.classList.add("active");
    viewMatrix.style.display = "block";
    renderMatrixTable();
  } else if (viewName === "prompt") {
    tabPromptBtn.classList.add("active");
    viewPrompt.style.display = "block";
  }
}

function getFilteredPerfumes() {
  return allPerfumes.filter((p) => {
    const matchesCat =
      currentCategory === "tümü" ||
      p.category.toLowerCase().includes(currentCategory.toLowerCase()) ||
      p.family.toLowerCase().includes(currentCategory.toLowerCase());

    const allNotes = [...p.notes.top, ...p.notes.heart, ...p.notes.base].join(" ").toLowerCase();
    const matchesSearch =
      !searchQuery ||
      p.name.toLowerCase().includes(searchQuery) ||
      p.brand.toLowerCase().includes(searchQuery) ||
      p.vibe.summary.toLowerCase().includes(searchQuery) ||
      p.trivia.text.toLowerCase().includes(searchQuery) ||
      allNotes.includes(searchQuery);

    return matchesCat && matchesSearch;
  });
}

function getSortedPerfumes(list) {
  const sorted = [...list];
  if (currentSort === "price-asc") {
    sorted.sort((a, b) => getLowestPrice(a) - getLowestPrice(b));
  } else if (currentSort === "price-desc") {
    sorted.sort((a, b) => getLowestPrice(b) - getLowestPrice(a));
  } else if (currentSort === "savings-desc") {
    sorted.sort((a, b) => getSavings(b) - getSavings(a));
  }
  return sorted;
}

function getLowestPrice(perfume) {
  const inStock = perfume.prices.filter((p) => p.in_stock);
  if (!inStock.length) return 0;
  return Math.min(...inStock.map((p) => p.price));
}

function getHighestPrice(perfume) {
  const inStock = perfume.prices.filter((p) => p.in_stock);
  if (!inStock.length) return 0;
  return Math.max(...inStock.map((p) => p.price));
}

function getSavings(perfume) {
  const low = getLowestPrice(perfume);
  const high = getHighestPrice(perfume);
  return high > low ? high - low : 0;
}

function getBestStore(perfume) {
  const lowest = getLowestPrice(perfume);
  return perfume.prices.find((p) => p.price === lowest && p.in_stock) || perfume.prices[0];
}

function renderAllViews() {
  renderPerfumesGrid();
  renderMatrixTable();
}

// Render Main Product Cards
function renderPerfumesGrid() {
  const filtered = getFilteredPerfumes();
  const sorted = getSortedPerfumes(filtered);

  if (!sorted.length) {
    perfumesGrid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; background: rgba(255,255,255,0.6); border-radius: 24px; border: var(--glass-border);">
        <p style="font-size: 32px; margin-bottom: 12px;">🔍</p>
        <h3 style="font-family: var(--font-serif); font-size: 20px; margin-bottom: 8px;">Aradığınız Kriterde Parfüm Bulunamadı</h3>
        <p style="color: var(--text-muted); font-size: 14px;">Arama teriminizi veya kategori filtrenizi değiştirerek tekrar deneyebilirsiniz.</p>
      </div>
    `;
    return;
  }

  perfumesGrid.innerHTML = sorted
    .map((perfume) => {
      const lowestPrice = getLowestPrice(perfume);
      const savings = getSavings(perfume);
      const bestStore = getBestStore(perfume);
      const storeCount = perfume.prices.length;

      return `
      <article class="perfume-card">
        <div class="card-top-meta">
          <span class="card-brand">${escapeHtml(perfume.brand)}</span>
          <span class="card-concentration">${escapeHtml(perfume.concentration)}</span>
        </div>

        <div class="card-image-box" onclick="openModal('${perfume.id}')" title="Detayları ve Tarihçeyi Gör">
          <img 
            class="card-bottle-img" 
            src="${escapeHtml(perfume.image)}" 
            alt="${escapeHtml(perfume.name)}"
            loading="lazy"
            onerror="this.src='https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?auto=format&fit=crop&w=600&q=80'"
          />
          <div class="card-trivia-badge">
            ✨ ${escapeHtml(perfume.trivia.title)}
          </div>
        </div>

        <h3 class="card-title" onclick="openModal('${perfume.id}')">${escapeHtml(perfume.name)}</h3>
        <p class="card-vibe-quote">"${escapeHtml(perfume.vibe.summary)}"</p>

        <div class="card-price-section">
          <div class="card-price-row">
            <div>
              <span style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 600; display: block;">En Uygun Fiyat</span>
              <span class="card-lowest-price">${lowestPrice.toLocaleString("tr-TR")} ₺</span>
            </div>
            ${
              savings > 0
                ? `<span class="card-savings-pill">${savings.toLocaleString("tr-TR")} ₺ Tasarruf</span>`
                : ""
            }
          </div>
          <div class="card-store-presence">
            <span>En iyi teklif: <strong class="card-best-store-name">${escapeHtml(bestStore.store)}</strong></span>
            <span>${storeCount} Türk Mağazasında</span>
          </div>
        </div>

        <button class="card-action-btn" onclick="openModal('${perfume.id}')">
          <span>Detaylar & Canlı Fiyatlar</span>
          <span>→</span>
        </button>
      </article>
    `;
    })
    .join("");
}

// Render Price Matrix View (All stores side-by-side)
function renderMatrixTable() {
  const filtered = getFilteredPerfumes();
  const sorted = getSortedPerfumes(filtered);

  matrixTableBody.innerHTML = sorted
    .map((perfume) => {
      const getStorePriceInfo = (storeName) => {
        const item = perfume.prices.find((p) => p.store.toLowerCase().includes(storeName.toLowerCase()));
        if (!item || !item.in_stock) {
          return `<span style="color: var(--text-muted); font-size: 12px;">Stokta Yok</span>`;
        }
        const isBest = item.price === getLowestPrice(perfume);
        return `
          <div class="matrix-price-cell ${isBest ? "best" : ""}">
            ${item.price.toLocaleString("tr-TR")} ₺
            ${isBest ? ' <span style="font-size: 10px;">★</span>' : ""}
          </div>
        `;
      };

      const savings = getSavings(perfume);

      return `
      <tr class="matrix-row">
        <td>
          <div class="matrix-perfume-col">
            <img class="matrix-thumb" src="${escapeHtml(perfume.image)}" alt="${escapeHtml(perfume.name)}" onerror="this.src='https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?auto=format&fit=crop&w=150&q=80'" />
            <div>
              <div style="font-weight: 700; font-family: var(--font-serif); cursor: pointer;" onclick="openModal('${perfume.id}')">${escapeHtml(perfume.name)}</div>
              <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">${escapeHtml(perfume.brand)} • ${escapeHtml(perfume.concentration)}</div>
            </div>
          </div>
        </td>
        <td>${getStorePriceInfo("Parfüm Noktası")}</td>
        <td>${getStorePriceInfo("Sephora")}</td>
        <td>${getStorePriceInfo("Boyner")}</td>
        <td>${getStorePriceInfo("Beymen")}</td>
        <td>${getStorePriceInfo("Sevil")}</td>
        <td>
          <span style="font-weight: 700; color: var(--success-text); font-size: 13px;">
            ${savings > 0 ? `+${savings.toLocaleString("tr-TR")} ₺` : "Aynı"}
          </span>
        </td>
        <td>
          <button class="glass-btn secondary" style="padding: 6px 12px; font-size: 12px;" onclick="openModal('${perfume.id}')">İncele</button>
        </td>
      </tr>
    `;
    })
    .join("");
}

// Open Detailed Liquid Glass Modal
function openModal(perfumeId) {
  const perfume = allPerfumes.find((p) => p.id === perfumeId);
  if (!perfume) return;

  const lowestPrice = getLowestPrice(perfume);

  modalContent.innerHTML = `
    <button class="modal-close-btn" onclick="closeModal()">✕</button>

    <div class="modal-grid">
      <!-- Left Visual Column -->
      <div class="modal-visual-side">
        <div class="modal-img-frame">
          <img class="modal-img" src="${escapeHtml(perfume.image)}" alt="${escapeHtml(perfume.name)}" onerror="this.src='https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?auto=format&fit=crop&w=600&q=80'" />
        </div>

        <!-- Sensory Vibe Radar -->
        <div style="background: rgba(255,255,255,0.7); border-radius: 20px; padding: 20px; border: var(--glass-border);">
          <h4 style="font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--accent-gold-dark); letter-spacing: 0.08em; margin-bottom: 12px;">
            ✨ Aura & Performans Radarı
          </h4>
          <div style="display: flex; flex-direction: column; gap: 10px; font-size: 13px;">
            <div style="display: flex; justify-content: space-between;">
              <span style="color: var(--text-muted);">Kalıcılık:</span>
              <strong style="color: var(--text-primary);">${escapeHtml(perfume.vibe.longevity)}</strong>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <span style="color: var(--text-muted);">Yayılım (Silaj):</span>
              <strong style="color: var(--text-primary);">${escapeHtml(perfume.vibe.sillage)}</strong>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <span style="color: var(--text-muted);">İdeal Mevsim:</span>
              <strong style="color: var(--text-primary);">${escapeHtml(perfume.vibe.season)}</strong>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <span style="color: var(--text-muted);">Uygun Ortam:</span>
              <strong style="color: var(--text-primary);">${escapeHtml(perfume.vibe.occasion)}</strong>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Details & Price Column -->
      <div class="modal-details">
        <div class="modal-header-info">
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
            <span class="gold-badge">${escapeHtml(perfume.category)}</span>
            <span class="card-concentration">${escapeHtml(perfume.concentration)}</span>
          </div>
          <h2>${escapeHtml(perfume.name)}</h2>
          <div class="brand">${escapeHtml(perfume.brand)} • Parfümör: ${escapeHtml(perfume.perfumer)} (${perfume.year})</div>
        </div>

        <!-- Trivia & Lore Card -->
        <div class="trivia-callout">
          <div class="trivia-header">
            <span>📜</span>
            <span>Şişe Tasarımı ve Tarihçe Anekdotu</span>
          </div>
          <p class="trivia-text">${escapeHtml(perfume.trivia.text)}</p>
          <div class="trivia-highlight">💡 ${escapeHtml(perfume.trivia.highlight)}</div>
        </div>

        <!-- Vibe Summary -->
        <div style="background: rgba(255, 255, 255, 0.6); border-radius: 16px; padding: 14px 18px; border: 1px solid rgba(215, 200, 180, 0.3);">
          <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: var(--accent-gold-dark); margin-bottom: 4px;">
            🌟 Koku Hissiyatı & Vibe
          </div>
          <p style="font-size: 13.5px; color: var(--text-secondary); font-style: italic; line-height: 1.5;">
            "${escapeHtml(perfume.vibe.summary)}"
          </p>
        </div>

        <!-- Notes Pyramid -->
        <div class="notes-pyramid">
          <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--accent-gold-dark); margin-bottom: 12px;">
            🌿 Koku Piramidi
          </div>
          <div class="pyramid-level">
            <span class="pyramid-tag">Üst Nota</span>
            <div class="pyramid-notes">
              ${perfume.notes.top.map((n) => `<span class="note-chip">${escapeHtml(n)}</span>`).join("")}
            </div>
          </div>
          <div class="pyramid-level">
            <span class="pyramid-tag">Kalp Nota</span>
            <div class="pyramid-notes">
              ${perfume.notes.heart.map((n) => `<span class="note-chip">${escapeHtml(n)}</span>`).join("")}
            </div>
          </div>
          <div class="pyramid-level">
            <span class="pyramid-tag">Dip Nota</span>
            <div class="pyramid-notes">
              ${perfume.notes.base.map((n) => `<span class="note-chip">${escapeHtml(n)}</span>`).join("")}
            </div>
          </div>
        </div>

        <!-- Turkey Stores Live Price Comparison -->
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <h4 style="font-size: 14px; font-weight: 700; text-transform: uppercase; color: var(--text-primary); letter-spacing: 0.05em;">
              🇹🇷 Türkiye Mağazaları Canlı Fiyat Karşılaştırması
            </h4>
            <span style="font-size: 12px; color: var(--success-text); font-weight: 700;">
              En iyi: ${lowestPrice.toLocaleString("tr-TR")} ₺
            </span>
          </div>

          <div class="store-price-list">
            ${perfume.prices
              .map((store) => {
                const isBest = store.price === lowestPrice && store.in_stock;
                return `
                <div class="store-row-card ${isBest ? "highlight" : ""}">
                  <div class="store-main-info">
                    <div class="store-logo-bullet">
                      ${store.store.includes("Sephora") ? "🖤" : store.store.includes("Beymen") ? "🛍️" : store.store.includes("Boyner") ? "🟡" : store.store.includes("Sevil") ? "✨" : "💎"}
                    </div>
                    <div>
                      <div class="store-name-text">
                        ${escapeHtml(store.store)}
                        ${isBest ? '<span class="card-savings-pill" style="margin-left: 8px;">En Uygun Teklif</span>' : ""}
                      </div>
                      <div class="store-sub-text">
                        ${escapeHtml(store.installment)} • ${escapeHtml(store.shipping)}
                      </div>
                    </div>
                  </div>

                  <div class="store-price-action">
                    <div class="store-val-box">
                      <div class="store-price-val">${store.price.toLocaleString("tr-TR")} ₺</div>
                      ${store.old_price > store.price ? `<div class="store-old-val">${store.old_price.toLocaleString("tr-TR")} ₺</div>` : ""}
                    </div>
                    <a href="${escapeHtml(store.link)}" target="_blank" rel="noopener noreferrer" class="store-buy-btn">
                      ${store.in_stock ? "Mağazada Gör ↗" : "Tükendi"}
                    </a>
                  </div>
                </div>
              `;
              })
              .join("")}
          </div>
        </div>
      </div>
    </div>
  `;

  modalBackdrop.classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeModal() {
  modalBackdrop.classList.remove("active");
  document.body.style.overflow = "";
}

// Copy Xcode Prompt to Clipboard
window.copyXcodePrompt = function () {
  const promptText = document.getElementById("promptCodeBox").innerText;
  navigator.clipboard.writeText(promptText).then(() => {
    const copyBtn = document.getElementById("copyPromptBtn");
    const originalText = copyBtn.innerHTML;
    copyBtn.innerHTML = "✓ Kopyalandı!";
    copyBtn.style.background = "#15803D";
    copyBtn.style.color = "#FFFFFF";
    setTimeout(() => {
      copyBtn.innerHTML = originalText;
      copyBtn.style.background = "";
      copyBtn.style.color = "";
    }, 2500);
  });
};

// Security helper
function escapeHtml(text) {
  if (!text) return "";
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
