// App state
let questions = [];
let currentQuestionIndex = 0;
let customerData = {};
let responses = [];
let autoAdvanceTimeout = null; // Track timeout to prevent multiple timers

// DOM elements
const screens = {
    welcome: document.getElementById('welcome-screen'),
    quiz: document.getElementById('quiz-screen'),
    result: document.getElementById('result-screen')
};

const loading = document.getElementById('loading');

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
});

// Event listeners
function setupEventListeners() {
    const customerForm = document.getElementById('customer-form');
    customerForm.addEventListener('submit', handleCustomerSubmit);
    
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    
    prevBtn.addEventListener('click', showPreviousQuestion);
    nextBtn.addEventListener('click', showNextQuestion);
}

// Handle customer form submission
async function handleCustomerSubmit(e) {
    e.preventDefault();
    
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const whatsapp = document.getElementById('whatsapp').value.trim();
    const birthday = document.getElementById('birthday').value.trim();
    
    if (!name) {
        alert('Por favor, insira seu nome');
        return;
    }
    
    customerData = { name, email, whatsapp, birthday };
    
    // Load questions
    await loadQuestions();
    
    // Show quiz screen
    showScreen('quiz');
    showQuestion(0);
}

// Load questions from API
async function loadQuestions() {
    try {
        showLoading(true);
        const response = await fetch('/api/questions');
        questions = await response.json();
        
        document.getElementById('total-questions').textContent = questions.length;
        showLoading(false);
    } catch (error) {
        console.error('Error loading questions:', error);
        alert('Erro ao carregar perguntas. Por favor, tente novamente.');
        showLoading(false);
    }
}

// Show specific question
function showQuestion(index) {
    if (index < 0 || index >= questions.length) return;
    
    currentQuestionIndex = index;
    const question = questions[index];
    
    // Update question counter
    document.getElementById('current-question').textContent = index + 1;
    
    // Update progress bar
    const progress = ((index + 1) / questions.length) * 100;
    document.getElementById('progress-fill').style.width = `${progress}%`;
    
    // Update question text
    document.getElementById('question-text').textContent = question.text;
    
    // Render options
    renderOptions(question.options, question.id);
    
    // Update navigation buttons
    updateNavigationButtons();
}

// Render question options
function renderOptions(options, questionId) {
    const container = document.getElementById('options-container');
    container.innerHTML = '';
    
    // Check if this question was already answered
    const existingResponse = responses.find(r => r.question_id === questionId);
    
    options.forEach(option => {
        const optionCard = document.createElement('div');
        optionCard.className = 'option-card';
        optionCard.textContent = option.text;
        optionCard.dataset.optionId = option.id;
        optionCard.dataset.questionId = questionId;
        
        // Mark as selected if previously chosen
        if (existingResponse && existingResponse.option_id === option.id) {
            optionCard.classList.add('selected');
        }
        
        optionCard.addEventListener('click', () => selectOption(optionCard, questionId, option.id));
        
        container.appendChild(optionCard);
    });
}

// Handle option selection
function selectOption(optionCard, questionId, optionId) {
    // Clear any existing auto-advance timeout
    if (autoAdvanceTimeout) {
        clearTimeout(autoAdvanceTimeout);
        autoAdvanceTimeout = null;
    }
    
    // Remove selection from all options
    document.querySelectorAll('.option-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // Mark selected option
    optionCard.classList.add('selected');
    
    // Store response
    const existingIndex = responses.findIndex(r => r.question_id === questionId);
    const response = { question_id: questionId, option_id: optionId };
    
    if (existingIndex >= 0) {
        responses[existingIndex] = response;
    } else {
        responses.push(response);
    }
    
    // Show next button
    document.getElementById('next-btn').style.display = 'block';
    
    // Auto-advance after a delay (increased to 800ms for better UX)
    autoAdvanceTimeout = setTimeout(() => {
    if (currentQuestionIndex < questions.length - 1) {
        showNextQuestion();
    } else {
        submitQuiz();
    }
}, 800);
}

function showPreviousQuestion() {
    // Clear any auto-advance timeout when manually navigating
    if (autoAdvanceTimeout) {
        clearTimeout(autoAdvanceTimeout);
        autoAdvanceTimeout = null;
    }

    if (currentQuestionIndex > 0) {
        showQuestion(currentQuestionIndex - 1);
    }
}

function showNextQuestion() {
    // Clear any auto-advance timeout when manually navigating
    if (autoAdvanceTimeout) {
        clearTimeout(autoAdvanceTimeout);
        autoAdvanceTimeout = null;
    }

    if (currentQuestionIndex < questions.length - 1) {
        showQuestion(currentQuestionIndex + 1);
    } else {
        submitQuiz();
    }
}

function updateNavigationButtons() {
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    
    // Show/hide previous button
    prevBtn.style.display = currentQuestionIndex > 0 ? 'block' : 'none';
    
    // Check if current question is answered
    const currentQuestion = questions[currentQuestionIndex];
    const isAnswered = responses.some(r => r.question_id === currentQuestion.id);
    
    nextBtn.style.display = isAnswered ? 'block' : 'none';
    
    // Change text on last question
    if (currentQuestionIndex === questions.length - 1 && isAnswered) {
        nextBtn.textContent = 'Ver Resultado';
    } else {
        nextBtn.textContent = 'Próxima';
    }
}

// Submit quiz
async function submitQuiz() {
    if (responses.length !== questions.length) {
        alert('Por favor, responda todas as perguntas');
        return;
    }
    
    try {
        showLoading(true);
        
        const data = {
            ...customerData,
            responses
        };
        
        const response = await fetch('/api/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showResult(result.result);
        } else {
            alert('Erro ao processar respostas: ' + (result.error || 'Erro desconhecido'));
        }
        
        showLoading(false);
    } catch (error) {
        console.error('Error submitting quiz:', error);
        alert('Erro ao enviar respostas. Por favor, tente novamente.');
        showLoading(false);
    }
}

// Show result
function showResult(result) {
    showScreen('result');
    
    // Animate result
    document.getElementById('result-type').textContent = result.emoji + ' ' + result.name;
    document.getElementById('result-description').textContent = result.description;
    document.getElementById('result-phrase').textContent = '"' + result.phrase + '"';
    
    // Apply personality color
    const resultCard = document.getElementById('result-card');
    resultCard.style.borderLeft = `10px solid ${result.color}`;
    
    // Create confetti effect
    createConfetti();
}

// Utility functions
function showScreen(screenName) {
    Object.values(screens).forEach(screen => {
        screen.classList.remove('active');
    });
    screens[screenName].classList.add('active');
}

function showLoading(show) {
    loading.style.display = show ? 'flex' : 'none';
}

function createConfetti() {
    const confettiContainer = document.querySelector('.confetti');
    const colors = ['#FF6B9D', '#C44569', '#FFA07A', '#98D8C8', '#F7B731', '#5F27CD'];
    
    for (let i = 0; i < 50; i++) {
        const confetti = document.createElement('div');
        confetti.style.position = 'absolute';
        confetti.style.width = '10px';
        confetti.style.height = '10px';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.top = Math.random() * 100 + '%';
        confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
        confetti.style.opacity = Math.random();
        confetti.style.animation = `confettiFall ${2 + Math.random() * 3}s ease-out forwards`;
        confettiContainer.appendChild(confetti);
    }
}

// Add confetti animation
const style = document.createElement('style');
style.textContent = `
    @keyframes confettiFall {
        to {
            transform: translateY(100vh) rotate(360deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
