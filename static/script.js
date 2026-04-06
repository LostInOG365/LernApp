// ========================
// GLOBAL VARIABLES
// ========================

const API_URL = 'http://localhost:5000/api';
let currentToken = null;
let currentUserId = null;
let currentUsername = null;

// ========================
// DARK MODE TOGGLE
// ========================

const themeToggle = document.getElementById('themeToggle');
const htmlElement = document.documentElement;

// Initialize theme from localStorage
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (savedTheme === 'dark') {
        htmlElement.classList.add('dark-mode');
        themeToggle.textContent = '☀️';
    } else {
        htmlElement.classList.remove('dark-mode');
        themeToggle.textContent = '🌙';
    }
}

themeToggle.addEventListener('click', () => {
    if (htmlElement.classList.contains('dark-mode')) {
        htmlElement.classList.remove('dark-mode');
        localStorage.setItem('theme', 'light');
        themeToggle.textContent = '🌙';
    } else {
        htmlElement.classList.add('dark-mode');
        localStorage.setItem('theme', 'dark');
        themeToggle.textContent = '☀️';
    }
});

// ========================
// AUTH FUNCTIONS
// ========================

const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const loginError = document.getElementById('loginError');
const registerError = document.getElementById('registerError');

// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        const tabName = e.target.dataset.tab;
        
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
        
        e.target.classList.add('active');
        document.getElementById(tabName + 'Form').classList.add('active');
        
        // Clear error messages
        loginError.classList.remove('show');
        registerError.classList.remove('show');
    });
});

// Login
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentToken = data.access_token;
            currentUserId = data.user_id;
            currentUsername = data.username;
            
            localStorage.setItem('token', currentToken);
            localStorage.setItem('userId', currentUserId);
            localStorage.setItem('username', currentUsername);
            
            showScreen('quizScreen');
            updateUserInfo();
            loadNextQuestion();
        } else {
            showError(loginError, data.error || 'Login fehlgeschlagen');
        }
    } catch (error) {
        showError(loginError, 'Verbindungsfehler: ' + error.message);
    }
    
    loginForm.reset();
});

// Register
registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    
    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentToken = data.access_token;
            currentUserId = data.user_id;
            currentUsername = data.username;
            
            localStorage.setItem('token', currentToken);
            localStorage.setItem('userId', currentUserId);
            localStorage.setItem('username', currentUsername);
            
            showScreen('quizScreen');
            updateUserInfo();
            loadNextQuestion();
        } else {
            showError(registerError, data.error || 'Registrierung fehlgeschlagen');
        }
    } catch (error) {
        showError(registerError, 'Verbindungsfehler: ' + error.message);
    }
    
    registerForm.reset();
});

// Logout
document.getElementById('logoutBtn').addEventListener('click', () => {
    currentToken = null;
    currentUserId = null;
    currentUsername = null;
    
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    localStorage.removeItem('username');
    
    document.getElementById('loginUsername').value = '';
    document.getElementById('loginPassword').value = '';
    
    showScreen('authScreen');
    updateUserInfo();
});

// ========================
// UI FUNCTIONS
// ========================

function updateUserInfo() {
    const userInfo = document.getElementById('userInfo');
    
    if (currentToken) {
        userInfo.style.display = 'flex';
        document.getElementById('currentUser').textContent = currentUsername;
    } else {
        userInfo.style.display = 'none';
    }
}

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
}

function showError(element, message) {
    element.textContent = message;
    element.classList.add('show');
}

function hideError(element) {
    element.classList.remove('show');
}

// ========================
// QUIZ FUNCTIONS
// ========================

let currentQuestion = null;
let questionsAnswered = 0;
let questionsCorrect = 0;

const submitAnswerBtn = document.getElementById('submitAnswerBtn');
const answerInput = document.getElementById('answerInput');
const resultMessage = document.getElementById('resultMessage');

async function loadNextQuestion() {
    // VERSTECKE ALTE NACHRICHT SOFORT
    resultMessage.style.display = 'none';
    
    try {
        const response = await fetch(`${API_URL}/next-question`, {
            headers: { 'Authorization': `Bearer ${currentToken}` }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentQuestion = data;
            displayQuestion(data);
        } else {
            console.error('Fehler beim Laden der Frage:', data.error);
        }
    } catch (error) {
        console.error('Fehler:', error);
    }
}

function displayQuestion(question) {
    document.getElementById('questionText').textContent = question.text;
    
    const difficultyBadge = document.getElementById('difficultyBadge');
    const difficultyLevels = ['', 'Leicht', 'Mittel', 'Schwer', 'Sehr schwer', 'Expert'];
    difficultyBadge.textContent = `Schwierigkeit: ${difficultyLevels[question.difficulty] || 'Unbekannt'}`;
    
    // NICHT VERSTECKEN!
    submitAnswerBtn.disabled = false;
}false;


submitAnswerBtn.addEventListener('click', async () => {
    const userAnswer = answerInput.value.trim();
    
    if (!userAnswer) {
        alert('Bitte gib eine Antwort ein!');
        return;
    }
    
    submitAnswerBtn.disabled = true;
    answerInput.disabled = true;  // ← Input auch disabled
    
    try {
        const response = await fetch(`${API_URL}/test-results`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${currentToken}`
            },
            body: JSON.stringify({
                user_id: currentUserId,
                question_id: currentQuestion.id,
                user_answer: userAnswer
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            const isCorrect = data.correct;
           // SYNC MIT BACKEND-DATEN!
    try {
    const statsResponse = await fetch(`${API_URL}/user-stats/${currentUserId}`);
    
    if (statsResponse.ok) {
        const userData = await statsResponse.json();
        const stats = userData.stats;
        
        // Sync mit echten Backend-Daten!
        questionsAnswered = stats.total_attempted;
        questionsCorrect = stats.total_correct;
    }
    } catch (err) {
    console.error('Fehler beim Sync:', err);
    }

updateQuizStats();
            
            // ZEIGE ERGEBNIS
            displayResult(isCorrect, data.correct_answer);
            
            // WARTE 4 SEKUNDEN BEVOR NEUE FRAGE KOMMT
            setTimeout(() => {
                answerInput.value = '';
                answerInput.disabled = false;
                loadNextQuestion();
                submitAnswerBtn.disabled = false;
            }, 4000);
        } else {
            alert('Fehler: ' + data.error);
            submitAnswerBtn.disabled = false;
            answerInput.disabled = false;
        }
    } catch (error) {
        console.error('Fehler:', error);
        alert('Verbindungsfehler');
        submitAnswerBtn.disabled = false;
        answerInput.disabled = false;
    }
});
    
    answerInput.value = '';
    resultMessage.style.display = 'none';


function displayResult(isCorrect, correctAnswer) {
    resultMessage.style.display = 'block';
    
    if (isCorrect) {
        resultMessage.classList.add('correct');
        resultMessage.classList.remove('incorrect');
        resultMessage.textContent = '✓ Richtig! Weiter so!';
    } else {
        resultMessage.classList.add('incorrect');
        resultMessage.classList.remove('correct');
        resultMessage.textContent = `✗ Falsch! Richtig wäre: "${correctAnswer}"`;
    }
}

function updateQuizStats() {
    document.getElementById('questionsAnswered').textContent = questionsAnswered;
    document.getElementById('questionsCorrect').textContent = questionsCorrect;
}

// ========================
// NAVIGATION
// ========================

document.getElementById('toRankingBtn').addEventListener('click', () => {
    showScreen('rankingScreen');
    loadRanking();
});

document.getElementById('toDashboardBtn').addEventListener('click', () => {
    showScreen('dashboardScreen');
    loadDashboard();
});

document.getElementById('backToQuizBtn').addEventListener('click', () => {
    showScreen('quizScreen');
});

document.getElementById('backToQuizFromDashBtn').addEventListener('click', () => {
    showScreen('quizScreen');
});

// ========================
// RANKING SCREEN
// ========================

async function loadRanking() {
    try {
        const response = await fetch(`${API_URL}/ranking`);
        const data = await response.json();
        
        if (response.ok) {
            displayRanking(data.ranking);
        }
    } catch (error) {
        console.error('Fehler beim Laden des Rankings:', error);
    }
}

function displayRanking(ranking) {
    const tbody = document.getElementById('rankingBody');
    tbody.innerHTML = '';
    
    if (ranking.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5">Noch keine Rankings verfügbar</td></tr>';
        return;
    }
    
    ranking.forEach(user => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${user.rank}</strong></td>
            <td>${user.username}</td>
            <td>${(user.success_rate * 100).toFixed(1)}%</td>
            <td>${user.total_attempted}</td>
            <td>${user.total_correct}</td>
        `;
        tbody.appendChild(row);
    });
}

// ========================
// DASHBOARD SCREEN
// ========================

async function loadDashboard() {
    try {
        const response = await fetch(`${API_URL}/user-stats/${currentUserId}`);
        
        if (response.ok) {
            const data = await response.json();
            displayDashboard(data);
        } else {
            console.warn('Dashboard-Fehler');
            displayDashboard({
                stats: {
                    total_attempted: 0,
                    total_correct: 0,
                    success_rate: 0
                }
            });
        }
    } catch (error) {
        console.error('Fehler beim Laden des Dashboards:', error);
        displayDashboard({
            stats: {
                total_attempted: 0,
                total_correct: 0,
                success_rate: 0
            }
        });
    
    }
}
function displayDashboard(userData) {
    const stats = userData.stats;
    
    document.getElementById('successRate').textContent = 
        stats.total_attempted > 0 
            ? `${(stats.total_correct / stats.total_attempted * 100).toFixed(1)}%`
            : '-';
    
    document.getElementById('totalAttempted').textContent = stats.total_attempted;
    document.getElementById('totalCorrect').textContent = stats.total_correct;
}
// ========================
// ALGORITHM DEBUG MODAL
// ========================

const algorithmModal = document.getElementById('algorithmModal');
const closeBtn = document.querySelector('.close');

document.getElementById('viewAlgorithmBtn').addEventListener('click', () => {
    algorithmModal.style.display = 'flex';
    loadAlgorithmDebug();
});

closeBtn.addEventListener('click', () => {
    algorithmModal.style.display = 'none';
});

window.addEventListener('click', (event) => {
    if (event.target === algorithmModal) {
        algorithmModal.style.display = 'none';
    }
});

async function loadAlgorithmDebug() {
    try {
        const response = await fetch(`${API_URL}/algorithm-debug`);
        const data = await response.json();
        
        const debugContent = document.getElementById('algorithmDebugContent');
        debugContent.innerHTML = `
            <h3>Algorithm: ${data.algorithm}</h3>
            <p><strong>Formel:</strong> ${data.formula}</p>
            <p><strong>Strategie:</strong> ${data.strategy}</p>
            <hr>
            <h4>Fragen nach Priorität:</h4>
            <pre>${JSON.stringify(data.questions_ranked_by_priority, null, 2)}</pre>
        `;
    } catch (error) {
        console.error('Fehler beim Laden des Algorithm-Debug:', error);
        document.getElementById('algorithmDebugContent').innerHTML = 
            '<p style="color: red;">Fehler beim Laden der Daten</p>';
    }
}

// ========================
// INITIALIZATION
// ========================

function checkLoggedIn() {
    const token = localStorage.getItem('token');
    const userId = localStorage.getItem('userId');
    const username = localStorage.getItem('username');
    
    if (token && userId && username) {
        currentToken = token;
        currentUserId = userId;
        currentUsername = username;
        
        updateUserInfo();
        showScreen('quizScreen');
        loadNextQuestion();
        updateQuizStats();
    } else {
        showScreen('authScreen');
    }
}

// Initialize app on page load
window.addEventListener('DOMContentLoaded', () => {
    initializeTheme();
    checkLoggedIn();
});