// =================================================================================
// CROWDFUNDING PLATFORM - FRONTEND SCRIPT
// Клиентская часть FastAPI + SQLAlchemy integration
// =================================================================================

// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// Global state
let currentProjects = [];
let currentUser = null;
let state = {
    projects: [],
    users: [],
    categories: [],
    investments: [],
    reviews: []
};

// =================================================================================
// API HELPERS
// =================================================================================

const API = {
    async get(endpoint, params = {}) {
        const query = new URLSearchParams(params);
        const url = `${API_BASE_URL}${endpoint}${query.toString() ? '?' + query : ''}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
    },

    async post(endpoint, data) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
    },

    async put(endpoint, data) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
    }
};

// =================================================================================
// PROJECT OPERATIONS
// =================================================================================

async function getProjects(params = {}) {
    try {
        const projects = await API.get('/projects', params);
        state.projects = projects;
        return projects;
    } catch (error) {
        console.error('Ошибка при загрузке проектов:', error);
        return [];
    }
}

async function getProject(projectId) {
    try {
        return await API.get(`/projects/${projectId}`);
    } catch (error) {
        console.error(`Ошибка при загрузке проекта ${projectId}:`, error);
        return null;
    }
}

async function createProject(projectData) {
    try {
        return await API.post('/projects', projectData);
    } catch (error) {
        console.error('Ошибка при создании проекта:', error);
        return null;
    }
}

// =================================================================================
// INVESTMENT OPERATIONS
// =================================================================================

async function createInvestment(investmentData) {
    try {
        const investment = await API.post('/investments', investmentData);
        console.log('Инвестиция сохранена:', investment);
        return investment;
    } catch (error) {
        console.error('Ошибка при сохранении инвестиции:', error);
        alert('Ошибка при сохранении инвестиции');
        return null;
    }
}

async function getProjectInvestments(projectId) {
    try {
        return await API.get(`/investments/project/${projectId}`);
    } catch (error) {
        console.error('Ошибка при загрузке инвестиций:', error);
        return [];
    }
}

// =================================================================================
// REVIEW OPERATIONS
// =================================================================================

async function createReview(reviewData) {
    try {
        return await API.post('/reviews', reviewData);
    } catch (error) {
        console.error('Ошибка при сохранении отзыва:', error);
        return null;
    }
}

async function getProjectReviews(projectId) {
    try {
        return await API.get(`/reviews/project/${projectId}`);
    } catch (error) {
        console.error('Ошибка при загрузке отзывов:', error);
        return [];
    }
}

// =================================================================================
// USER OPERATIONS
// =================================================================================

async function createUser(userData) {
    try {
        const user = await API.post('/users', userData);
        currentUser = user;
        localStorage.setItem('currentUser', JSON.stringify(user));
        return user;
    } catch (error) {
        console.error('Ошибка при регистрации:', error);
        return null;
    }
}

async function getUser(userId) {
    try {
        return await API.get(`/users/${userId}`);
    } catch (error) {
        console.error(`Ошибка при загрузке пользователя ${userId}:`, error);
        return null;
    }
}

// =================================================================================
// CATEGORIES
// =================================================================================

async function getCategories() {
    try {
        const categories = await API.get('/categories');
        state.categories = categories;
        return categories;
    } catch (error) {
        console.error('Ошибка при загрузке категорий:', error);
        return [];
    }
}

// =================================================================================
// SEARCH & FILTER
// =================================================================================

async function searchProjects(query, params = {}) {
    try {
        return await API.get('/search', { q: query, ...params });
    } catch (error) {
        console.error('Ошибка при поиске:', error);
        return { results: [], total: 0 };
    }
}

async function getStatistics() {
    try {
        return await API.get('/statistics');
    } catch (error) {
        console.error('Ошибка при загрузке статистики:', error);
        return { total_projects: 0, total_raised: 0, total_backers: 0, total_users: 0 };
    }
}

// =================================================================================
// SEARCH & SORT FUNCTIONALITY
// =================================================================================

function performSearch() {
    const queryEl = document.getElementById('search-input');
    const sortEl = document.getElementById('sort-select');
    const query = queryEl ? queryEl.value.toLowerCase() : '';
    const sortBy = sortEl ? sortEl.value : 'popular';

    if (!query) {
        getProjects({ sort_by: sortBy }).then(projects => {
            renderProjects(projects, 'projects-grid');
            navigateTo('projects');
        });
        return;
    }

    getProjects({ search: query, sort_by: sortBy }).then(projects => {
        renderProjects(projects, 'projects-grid');
        navigateTo('projects');
    });
}

// =================================================================================
// RENDERING FUNCTIONS
// =================================================================================

function renderProjects(projects, containerId = 'projects-grid') {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!projects || projects.length === 0) {
        container.innerHTML = '<p>Проекты не найдены</p>';
        return;
    }

    container.innerHTML = projects.map(project => createProjectCard(project)).join('');
}

function createProjectCard(project) {
    const progress = Math.round((project.raised_amount / project.goal) * 100);
    const daysLeft = Math.max(0, Math.ceil((new Date(project.deadline) - new Date()) / (1000 * 60 * 60 * 24)));

    return `
        <div class="project-card" data-id="${project.id}">
            <div class="project-image">
                <img src="${project.image_url || 'https://via.placeholder.com/400x200'}" alt="${project.title}">
                <span class="project-category">Выбранные</span>
            </div>
            <div class="project-content">
                <h3 class="project-title">${project.title}</h3>
                <p class="project-description">${project.description}</p>
                <div class="project-progress">
                    <div class="progress-labels">
                        <span class="progress-raised">Собрано: ${formatCurrency(project.raised_amount)} руб.</span>
                        <span class="progress-goal">Цель: ${formatCurrency(project.goal)} руб.</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${Math.min(progress, 100)}%"></div>
                    </div>
                </div>
                <div class="project-stats">
                    <div class="stat-item">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                            <circle cx="9" cy="7" r="4"></circle>
                        </svg>
                        ${project.backers_count} поддерживающих
                    </div>
                    <div class="stat-item">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="1"></circle>
                            <path d="M12 1v6m0 6v6"></path>
                        </svg>
                        ${daysLeft} дней осталось
                    </div>
                </div>
                <button class="btn-open" data-id="${project.id}">Поддержать проект</button>
            </div>
        </div>
    `;
}

// =================================================================================
// MODAL & FORM HANDLING
// =================================================================================

function openProjectModal(projectId) {
    getProject(projectId).then(project => {
        if (!project) return;

        const existing = document.getElementById('project-modal');
        if (existing) existing.remove();

        const progress = Math.round((project.raised_amount / project.goal) * 100);

        const modal = document.createElement('div');
        modal.id = 'project-modal';
        modal.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);display:flex;align-items:center;justify-content:center;z-index:9999;';

        modal.innerHTML = `
            <div style="background:white;padding:40px;border-radius:12px;max-width:500px;max-height:80vh;overflow-y:auto;position:relative;">
                <button onclick="document.getElementById('project-modal').remove()" style="position:absolute;top:10px;right:10px;background:none;border:none;font-size:24px;cursor:pointer;">&times;</button>
                
                <h2>${project.title}</h2>
                <p>${project.description}</p>
                
                <div style="margin:20px 0;">
                    <p><strong>Прогресс: ${progress}%</strong></p>
                    <div style="background:#e0e0e0;height:10px;border-radius:5px;overflow:hidden;">
                        <div style="background:#ea580c;height:100%;width:${Math.min(progress, 100)}%;"></div>
                    </div>
                    <p>Собрано: ${formatCurrency(project.raised_amount)} / ${formatCurrency(project.goal)}</p>
                    <p>Поддерживающих: ${project.backers_count}</p>
                </div>

                <div style="margin-bottom:20px;">
                    <label>Сумма поддержки (руб.):</label>
                    <input type="number" id="investment-amount" min="100" placeholder="1000" style="width:100%;padding:8px;margin:10px 0;border:1px solid #ccc;border-radius:4px;">
                    
                    <label>Ваше имя:</label>
                    <input type="text" id="investor-name" placeholder="Полное имя" style="width:100%;padding:8px;margin:10px 0;border:1px solid #ccc;border-radius:4px;">
                    
                    <label>Комментарий:</label>
                    <textarea id="investment-message" placeholder="Оставьте свои мысли..." style="width:100%;padding:8px;margin:10px 0;border:1px solid #ccc;border-radius:4px;min-height:80px;"></textarea>
                    
                    <button onclick="submitInvestment(${projectId})" style="width:100%;padding:12px;background:#ea580c;color:white;border:none;border-radius:4px;cursor:pointer;font-weight:bold;margin-top:10px;">Поддержать проект</button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
    });
}

async function submitInvestment(projectId) {
    const amount = parseFloat(document.getElementById('investment-amount').value);
    const name = document.getElementById('investor-name').value;
    const message = document.getElementById('investment-message').value;

    if (!amount || amount < 100) {
        alert('Пожалуйста, внесите сумму не менее 100 руб.');
        return;
    }

    if (!name) {
        alert('Пожалуйста, внесите ваше имя');
        return;
    }

    // Наочередь, нужно создать пользователя или использовать существующего
    let userId = 1; // демо пользователя

    if (!currentUser) {
        // Пытаемся сохранить нового пользователя
        const newUser = await createUser({
            username: name.replace(/\s+/g, '_').toLowerCase(),
            email: `user_${Date.now()}@example.com`,
            full_name: name
        });
        if (newUser) userId = newUser.id;
    } else {
        userId = currentUser.id;
    }

    const investment = await createInvestment({
        amount: amount,
        project_id: projectId,
        user_id: userId,
        message: message || null
    });

    if (investment) {
        alert('Спасибо за поддержку! Ваша инвестиция сохранена.');
        document.getElementById('project-modal')?.remove();
        getProjects({ sort_by: 'popular' }).then(projects => renderProjects(projects, 'projects-grid'));
    }
}

// =================================================================================
// UTILITY FUNCTIONS
// =================================================================================

function formatCurrency(amount) {
    return new Intl.NumberFormat('ru-RU').format(Math.floor(amount));
}

function navigateTo(page) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    const targetPage = document.getElementById(page);
    if (targetPage) targetPage.classList.add('active');
}

// =================================================================================
// EVENT LISTENERS & INITIALIZATION
// =================================================================================

document.addEventListener('DOMContentLoaded', async function() {
    console.log('Приложение загружается...');

    // Получить статистику
    const stats = await getStatistics();
    if (stats) {
        const statsContainer = document.querySelector('.stats-grid');
        if (statsContainer) {
            const statCards = statsContainer.querySelectorAll('.stat-card');
            if (statCards[0]) statCards[0].querySelector('.stat-value').textContent = stats.total_projects || 0;
            if (statCards[1]) statCards[1].querySelector('.stat-value').textContent = formatCurrency(stats.total_raised || 0);
            if (statCards[2]) statCards[2].querySelector('.stat-value').textContent = stats.total_backers || 0;
            if (statCards[3]) statCards[3].querySelector('.stat-value').textContent = stats.total_users || 0;
        }
    }

    // Получить проекты
    await getProjects({ sort_by: 'popular', limit: 12 }).then(projects => {
        renderProjects(projects, 'projects-grid');
    });

    // Обработчик Enter в поиске
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') performSearch();
        });
    }

    // Обработчик изменения сортировки
    const sortSelect = document.getElementById('sort-select');
    if (sortSelect) {
        sortSelect.addEventListener('change', performSearch);
    }

    // Кнопка поиска
    const searchButton = document.querySelector('[role="search"] button, .btn-search');
    if (searchButton) {
        searchButton.addEventListener('click', performSearch);
    }

    // Навигация
    const navLinks = document.querySelectorAll('.nav-link, [data-nav]');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const page = link.getAttribute('data-nav') || link.textContent.toLowerCase();
            if (page === 'Проекты' || page === 'projects') navigateTo('projects');
            else if (page === 'О нас' || page === 'about') navigateTo('about');
        });
    });

    // Открытие модали проекта по клику кнопки
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.btn-open, .project-card');
        if (btn) {
            const projectId = parseInt(btn.getAttribute('data-id'));
            if (projectId) openProjectModal(projectId);
        }
    });

    console.log('Приложение готово!');
});

// Пдели для навигации
window.navigateTo = navigateTo;
window.openProjectModal = openProjectModal;
window.submitInvestment = submitInvestment;
window.performSearch = performSearch;
