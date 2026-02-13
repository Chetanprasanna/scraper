// AI Articles Dashboard - Main Application
// Handles carousel, data loading, rendering, filtering, and save functionality

const STORAGE_KEY = 'glaido_saved_articles';
const DATA_URL = 'aggregated_articles.json';

let allArticles = [];
let savedArticleIds = new Set();
let currentFilter = 'all';
let currentCarouselIndex = 0;
let carouselInterval = null;

// Initialize app
async function init() {
    console.log('🚀 Initializing AI Articles Dashboard...');

    // Load saved articles from localStorage
    loadSavedArticles();

    // Load articles data
    await loadArticles();

    // Setup event listeners
    setupEventListeners();

    // Start carousel autoplay
    startCarouselAutoplay();
}

// Load saved articles from localStorage
function loadSavedArticles() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
        savedArticleIds = new Set(JSON.parse(saved));
        console.log(`📌 Loaded ${savedArticleIds.size} saved articles`);
    }
}

// Save articles to localStorage
function saveSavedArticles() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify([...savedArticleIds]));
}

// Load articles from JSON
async function loadArticles() {
    try {
        const response = await fetch(DATA_URL);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        allArticles = data.articles || [];

        // Update UI
        updateSourceStatus(data.sources);
        updateLastUpdated(data.last_updated);
        initCarousel();
        renderArticles();

        console.log(`✅ Loaded ${allArticles.length} articles`);

        // Hide loading skeleton
        const skeleton = document.querySelector('.loading-skeleton');
        if (skeleton) skeleton.style.display = 'none';

    } catch (error) {
        console.error('❌ Error loading articles:', error);
        const skeleton = document.querySelector('.loading-skeleton');
        if (skeleton) skeleton.style.display = 'none';
        showEmptyState('Failed to load articles. Please try refreshing.');
    }
}

// Initialize carousel with top 5 articles that have images
function initCarousel() {
    const featuredArticles = allArticles
        .filter(article => article.image_url)
        .slice(0, 5);

    if (featuredArticles.length === 0) {
        // Hide carousel if no images
        document.querySelector('.featured-section').style.display = 'none';
        return;
    }

    const track = document.getElementById('carouselTrack');
    const indicators = document.getElementById('carouselIndicators');

    track.innerHTML = '';
    indicators.innerHTML = '';

    featuredArticles.forEach((article, index) => {
        // Create slide
        const slide = createCarouselSlide(article, index);
        track.appendChild(slide);

        // Create indicator
        const indicator = document.createElement('div');
        indicator.className = `carousel-indicator ${index === 0 ? 'active' : ''}`;
        indicator.addEventListener('click', () => goToSlide(index));
        indicators.appendChild(indicator);
    });

    currentCarouselIndex = 0;
    updateCarousel();
}

// Create carousel slide
function createCarouselSlide(article, index) {
    const isSaved = savedArticleIds.has(article.id);
    const saveIcon = isSaved ? '★' : '☆';
    const savedClass = isSaved ? 'saved' : '';
    const sourceName = article.source === 'ben_bites' ? 'Ben\'s Bites' : 'AI Rundown';

    const slide = document.createElement('div');
    slide.className = `carousel-slide ${index === 0 ? 'active' : ''}`;
    slide.innerHTML = `
        <div class="carousel-image-container">
            <img src="${article.image_url}" alt="${article.title}" class="carousel-image" loading="lazy">
            <div class="carousel-caption">
                <div class="carousel-meta">
                    <span class="carousel-source">${sourceName}</span>
                    <button class="carousel-save-btn ${savedClass}" data-article-id="${article.id}">${saveIcon}</button>
                </div>
                <h3 class="carousel-title">${article.title}</h3>
                ${article.description ? `<p class="carousel-description">${article.description}</p>` : ''}
                ${article.tags && article.tags.length ? `
                    <div class="carousel-tags">
                        ${article.tags.slice(0, 3).map(tag => `<span class="carousel-tag">${tag}</span>`).join('')}
                    </div>
                ` : ''}
            </div>
        </div>
    `;

    // Make slide clickable to open article
    slide.addEventListener('click', (e) => {
        if (!e.target.closest('.carousel-save-btn')) {
            window.open(article.url, '_blank');
        }
    });

    // Add save button listener
    const saveBtn = slide.querySelector('.carousel-save-btn');
    if (saveBtn) {
        saveBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleSave(article.id);
        });
    }

    return slide;
}

// Update carousel display
function updateCarousel() {
    const slides = document.querySelectorAll('.carousel-slide');
    const indicators = document.querySelectorAll('.carousel-indicator');

    slides.forEach((slide, index) => {
        slide.classList.toggle('active', index === currentCarouselIndex);
    });

    indicators.forEach((indicator, index) => {
        indicator.classList.toggle('active', index === currentCarouselIndex);
    });
}

// Navigate carousel
function nextSlide() {
    const slides = document.querySelectorAll('.carousel-slide');
    currentCarouselIndex = (currentCarouselIndex + 1) % slides.length;
    updateCarousel();
    resetCarouselAutoplay();
}

function prevSlide() {
    const slides = document.querySelectorAll('.carousel-slide');
    currentCarouselIndex = (currentCarouselIndex - 1 + slides.length) % slides.length;
    updateCarousel();
    resetCarouselAutoplay();
}

function goToSlide(index) {
    currentCarouselIndex = index;
    updateCarousel();
    resetCarouselAutoplay();
}

// Carousel autoplay
function startCarouselAutoplay() {
    carouselInterval = setInterval(nextSlide, 5000); // Change slide every 5 seconds
}

function resetCarouselAutoplay() {
    clearInterval(carouselInterval);
    startCarouselAutoplay();
}

// Update source status cards
function updateSourceStatus(sources) {
    if (!sources) return;

    // Ben's Bites
    if (sources.ben_bites) {
        const countEl = document.getElementById('benBitesCount');
        const badge = document.querySelector('#benBitesStatus .source-badge');

        countEl.textContent = `${sources.ben_bites.article_count} articles`;

        if (sources.ben_bites.status === 'success') {
            badge.classList.add('success');
            badge.classList.remove('error');
        } else {
            badge.classList.add('error');
            badge.classList.remove('success');
        }
    }

    // AI Rundown
    if (sources.ai_rundown) {
        const countEl = document.getElementById('aiRundownCount');
        const badge = document.querySelector('#aiRundownStatus .source-badge');

        countEl.textContent = `${sources.ai_rundown.article_count} articles`;

        if (sources.ai_rundown.status === 'success') {
            badge.classList.add('success');
            badge.classList.remove('error');
        } else {
            badge.classList.add('error');
            badge.classList.remove('success');
        }
    }
}

// Update last updated time
function updateLastUpdated(timestamp) {
    if (!timestamp) return;

    const date = new Date(timestamp);
    const formatted = date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });

    document.getElementById('lastUpdated').textContent = `Last updated: ${formatted}`;
}

// Render articles based on current filter
function renderArticles() {
    const container = document.getElementById('articlesContainer');
    const emptyState = document.getElementById('emptyState');

    // Filter articles
    let articlesToRender = allArticles;

    if (currentFilter === 'saved') {
        articlesToRender = allArticles.filter(article => savedArticleIds.has(article.id));
    }

    // Update counts
    document.getElementById('allCount').textContent = allArticles.length;
    document.getElementById('savedCount').textContent = savedArticleIds.size;

    // Show empty state if no articles
    if (articlesToRender.length === 0) {
        container.innerHTML = '';
        const message = currentFilter === 'saved'
            ? 'No saved articles yet. Click the bookmark icon to save articles!'
            : 'No articles found. Try refreshing!';
        showEmptyState(message);
        return;
    }

    // Hide empty state
    emptyState.classList.add('hidden');

    // Render article cards
    container.innerHTML = articlesToRender.map(article => renderArticleCard(article)).join('');

    // Add event listeners to save buttons
    document.querySelectorAll('.save-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleSave(btn.dataset.articleId);
        });
    });

    // Add event listeners to article cards
    document.querySelectorAll('.article-card').forEach(card => {
        card.addEventListener('click', () => {
            window.open(card.dataset.url, '_blank');
        });
    });
}

// Render single article card
function renderArticleCard(article) {
    const isSaved = savedArticleIds.has(article.id);
    const saveIcon = isSaved ? '★' : '☆';
    const savedClass = isSaved ? 'saved' : '';

    const tags = article.tags && article.tags.length > 0
        ? article.tags.slice(0, 3).map(tag => `<span class="tag">${tag}</span>`).join('')
        : '';

    const description = article.description
        ? `<p class="article-description">${article.description}</p>`
        : '';

    const sourceName = article.source === 'ben_bites' ? 'Ben\'s Bites' : 'AI Rundown';

    const imageHtml = article.image_url
        ? `<img src="${article.image_url}" alt="${article.title}" class="article-image" loading="lazy">`
        : '<div class="no-image">📰</div>';

    return `
        <div class="article-card" data-url="${article.url}">
            ${imageHtml}
            <div class="article-content">
                <div class="article-header">
                    <span class="article-source">${sourceName}</span>
                    <button class="save-btn ${savedClass}" data-article-id="${article.id}">${saveIcon}</button>
                </div>
                <h3 class="article-title">${article.title}</h3>
                ${description}
                <div class="article-footer">
                    <div class="article-tags">${tags}</div>
                </div>
            </div>
        </div>
    `;
}

// Toggle save state for an article
function toggleSave(articleId) {
    if (savedArticleIds.has(articleId)) {
        savedArticleIds.delete(articleId);
        console.log('🗑️ Removed from saved:', articleId);
    } else {
        savedArticleIds.add(articleId);
        console.log('💾 Saved article:', articleId);
    }

    saveSavedArticles();

    // Update both carousel and grid
    initCarousel();
    renderArticles();
}

// Show empty state
function showEmptyState(message) {
    const emptyState = document.getElementById('emptyState');
    emptyState.querySelector('.empty-message').textContent = message;
    emptyState.classList.remove('hidden');
}

// Setup event listeners
function setupEventListeners() {
    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active state
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Update filter
            currentFilter = btn.dataset.filter;
            renderArticles();
        });
    });

    // Refresh button
    document.getElementById('refreshBtn').addEventListener('click', async () => {
        const btn = document.getElementById('refreshBtn');
        btn.disabled = true;
        btn.innerHTML = '<span>↻</span> Refreshing...';

        await loadArticles();

        btn.disabled = false;
        btn.innerHTML = '<span>↻</span> Refresh';
    });

    // Carousel controls
    document.getElementById('prevBtn').addEventListener('click', prevSlide);
    document.getElementById('nextBtn').addEventListener('click', nextSlide);

    // Keyboard navigation for carousel
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') prevSlide();
        if (e.key === 'ArrowRight') nextSlide();
    });

    // Dock bounce animation on click
    document.querySelectorAll('.dock-item').forEach(item => {
        item.addEventListener('click', (e) => {
            item.classList.add('bouncing');
            setTimeout(() => {
                item.classList.remove('bouncing');
            }, 500);
        });
    });
}

// Initialize on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
