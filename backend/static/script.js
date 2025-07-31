// DOM Elements
const sidebar = document.querySelector('.sidebar');
const modeButtons = document.querySelectorAll('.mode-btn');
const chatContainer = document.getElementById('chatContainer');
const userPrompt = document.getElementById('userPrompt');
const sendBtn = document.getElementById('sendBtn');
const voiceBtn = document.getElementById('voiceBtn');
const clearBtn = document.getElementById('clearBtn');
const configPanel = document.getElementById('configPanel');
const numItemsInput = document.getElementById('numItems');
const decreaseBtn = document.getElementById('decreaseBtn');
const increaseBtn = document.getElementById('increaseBtn');
const completedValue = document.getElementById('completedValue');
const scoreValue = document.getElementById('scoreValue');

// State
let currentMode = 'general';
let isProcessing = false;
let stats = {
    completed: 0,
    score: 0
};

// Initialize
function init() {
    try {
        if (!userPrompt || !sendBtn || !chatContainer) {
            console.error('Required DOM elements not found');
            return;
        }
        
        adjustTextareaHeight();
        setupEventListeners();
        updateStats();
        
        if (configPanel) {
            configPanel.style.display = currentMode === 'general' ? 'none' : 'flex';
        }
    } catch (error) {
        console.error('Initialization error:', error);
    }
}

// Event Listeners
function setupEventListeners() {
    // Mode switching
    modeButtons.forEach(btn => {
        btn.addEventListener('click', () => switchMode(btn.dataset.mode));
    });

    // Input handling
    userPrompt.addEventListener('input', adjustTextareaHeight);
    userPrompt.addEventListener('keydown', handleEnterPress);
    
    // Button actions
    sendBtn.addEventListener('click', handleSend);
    voiceBtn.addEventListener('click', handleVoiceInput);
    clearBtn.addEventListener('click', clearChat);
    
    // Number input controls
    decreaseBtn.addEventListener('click', () => updateNumItems(-1));
    increaseBtn.addEventListener('click', () => updateNumItems(1));
    numItemsInput.addEventListener('change', validateNumItems);
}

// UI Updates
function adjustTextareaHeight() {
    userPrompt.style.height = 'auto';
    userPrompt.style.height = userPrompt.scrollHeight + 'px';
}

function updateStats() {
    completedValue.textContent = stats.completed;
    scoreValue.textContent = stats.score + '%';
}

function switchMode(mode) {
    // Update active state
    modeButtons.forEach(btn => {
        // Remove both the 'active' and background classes
        btn.classList.remove('active', 'bg-primary');
        if (btn.dataset.mode === mode) {
            btn.classList.add('active', 'bg-primary');
        }
    });
    
    // Update current mode
    currentMode = mode;
    
    // Clear chat when switching modes
    clearChat();
    
    // Update UI text
    const descriptions = {
        general: 'Ask any question and get detailed answers',
        flashcards: 'Practice with interactive flashcards',
        mcq: 'Test your knowledge with multiple choice questions',
        casestudies: 'Learn from real-world case studies',
        summarize: 'Get concise summaries of long texts'
    };
    
    const currentModeElement = document.querySelector('.current-mode');
    const modeDescriptionElement = document.querySelector('.mode-description');
    
    if (currentModeElement && modeDescriptionElement) {
        currentModeElement.textContent = mode.charAt(0).toUpperCase() + mode.slice(1);
        modeDescriptionElement.textContent = descriptions[mode] || '';
    }
    
    // Show/hide number control
    if (configPanel) {
        configPanel.style.display = mode === 'general' || mode === 'summarize' ? 'none' : 'flex';
    }
    
    // Update placeholder
    if (userPrompt) {
        userPrompt.placeholder = getPlaceholder(mode);
    }
}

function getPlaceholder(mode) {
    const placeholders = {
        general: 'Ask any question...',
        flashcards: 'Enter a topic to generate flashcards...',
        mcq: 'Enter a topic for quiz questions...',
        casestudies: 'Describe the case study topic...',
        summarize: 'Paste the text to summarize...'
    };
    return placeholders[mode] || 'Type your message...';
}

// Message Handling
function appendMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`;
    
    const messageContent = document.createElement('div');
    messageContent.className = `max-w-[70%] p-4 rounded-2xl ${
        isUser 
            ? 'bg-primary text-white rounded-br-none' 
            : 'bg-gray-50 text-gray-900 rounded-bl-none'
    }`;

    // Format the content based on whether it contains newlines
    if (content.includes('\n')) {
        messageContent.innerHTML = content.split('\n').map(line => {
            // Add bold formatting to question numbers, card numbers, etc.
            line = line.replace(/^(Question \d+:|Card \d+:|Background:|Analysis:|Conclusion:|Recommendations:)/g, '<strong>$1</strong>');
            // Add spacing after colons
            line = line.replace(/:\n/g, ':</br>');
            return line;
        }).join('<br>');
    } else {
        messageContent.textContent = content;
    }
    
    messageDiv.appendChild(messageContent);
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function handleSend() {
    if (isProcessing || !userPrompt.value.trim()) return;
    
    const message = userPrompt.value.trim();
    const numItems = parseInt(numItemsInput.value) || 5;
    
    appendMessage(message, true);
    
    isProcessing = true;
    sendBtn.disabled = true;
    userPrompt.value = '';
    adjustTextareaHeight();
    
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                mode: currentMode,
                numItems: numItems
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        
        if (data.error) {
            appendMessage('Error: ' + data.error);
        } else {
            const formattedResponse = formatResponse(data.response, currentMode);
            appendMessage(formattedResponse);
            
            // Update stats
            stats.completed++;
            stats.score = Math.min(100, stats.score + 5);
            updateStats();
        }
    } catch (error) {
        console.error('Error:', error);
        appendMessage('Sorry, there was an error processing your request. Please try again.');
    } finally {
        isProcessing = false;
        sendBtn.disabled = false;
    }
}

function formatResponse(response, mode) {
    switch (mode) {
        case 'flashcards':
            return response.replace(/Card \d+:/g, '\n$&')
                         .replace(/Front:/g, '\n$&')
                         .replace(/Back:/g, '\n$&');
        case 'mcq':
            return response.replace(/Question \d+:/g, '\n$&')
                         .replace(/Correct Answer:/g, '\n$&')
                         .replace(/Explanation:/g, '\n$&');
        case 'casestudies':
            return response.replace(/Background:|Analysis:|Conclusion:|Recommendations:/g, '\n$&');
        case 'summarize':
            return response.replace(/Key Points:|Main Takeaways:/g, '\n$&');
        default:
            return response;
    }
}

function handleEnterPress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
    }
}

// Voice Input
function handleVoiceInput() {
    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        
        recognition.onstart = () => {
            voiceBtn.classList.add('bg-gray-200');
        };
        
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            userPrompt.value = transcript;
            adjustTextareaHeight();
        };
        
        recognition.onend = () => {
            voiceBtn.classList.remove('bg-gray-200');
        };
        
        recognition.start();
    } else {
        appendMessage('Voice input is not supported in your browser.');
    }
}

// Utility Functions
function clearChat() {
    chatContainer.innerHTML = '';
}

function updateNumItems(change) {
    const currentValue = parseInt(numItemsInput.value);
    const newValue = Math.max(1, Math.min(20, currentValue + change));
    numItemsInput.value = newValue;
    
    // Add visual feedback
    const btn = change > 0 ? increaseBtn : decreaseBtn;
    btn.classList.add('bg-primary', 'text-white');
    setTimeout(() => {
        btn.classList.remove('bg-primary', 'text-white');
    }, 200);
}

function validateNumItems() {
    const value = parseInt(numItemsInput.value);
    numItemsInput.value = Math.max(1, Math.min(20, value));
}

function getMockResponse(mode) {
    const responses = {
        general: "Here's a detailed answer to your question about " + userPrompt.value,
        flashcards: "Here are your flashcards about " + userPrompt.value + ":\n\n1. Front: Key concept\nBack: Definition\n\n2. Front: Important term\nBack: Explanation",
        mcq: "Here are multiple choice questions about " + userPrompt.value + ":\n\n1. Question one?\na) Option 1\nb) Option 2\nc) Option 3\nd) Option 4\n\n2. Question two?...",
        casestudies: "Analysis of case study about " + userPrompt.value + ":\n\nBackground:\n...\n\nKey Points:\n1...\n2...\n\nConclusion:\n...",
        summarize: "Summary of the text:\n\nKey Points:\n1...\n2...\n\nMain Takeaways:\n..."
    };
    return responses[mode] || "I'm here to help you learn! Please ask a question.";
}

// Initialize the app
init();



