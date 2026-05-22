// Initialize Socket.IO connection
const socket = io();

// Matrix Rain Effect
function createMatrixRain() {
    const matrixRain = document.getElementById('matrixRain');
    if (!matrixRain) return;

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    matrixRain.appendChild(canvas);

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const matrix = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%+-/~{[|`]}";
    const matrixArray = matrix.split("");

    const fontSize = 10;
    const columns = canvas.width / fontSize;
    const drops = [];

    for (let x = 0; x < columns; x++) {
        drops[x] = 1;
    }

    function draw() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.02)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#00FF41';
        ctx.font = fontSize + 'px monospace';

        for (let i = 0; i < drops.length; i++) {
            const text = matrixArray[Math.floor(Math.random() * matrixArray.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);

            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }

    setInterval(draw, 35);

    // Resize canvas when window resizes
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
}

// Initialize Matrix Rain
document.addEventListener('DOMContentLoaded', () => {
    createMatrixRain();
});

// DOM Elements
const unitSelect = document.getElementById('unitSelect');
const unitState = document.getElementById('unitState');
const unitConsciousnessIndex = document.getElementById('unitConsciousnessIndex');
const processForm = document.getElementById('processForm');
const inputText = document.getElementById('inputText');
const processingResult = document.getElementById('processingResult');
const createUnitForm = document.getElementById('createUnitForm');
const createUnitModal = document.getElementById('createUnitModal');
const toast = document.getElementById('toast');

// Get parameter input elements
const temperatureInput = document.getElementById('temperature');
const topPInput = document.getElementById('topP');
const maxTokensInput = document.getElementById('maxTokens');
const presencePenaltyInput = document.getElementById('presencePenalty');

let selectedUnitId = null;
let isProcessing = false;

// Format response text to preserve paragraphs and line breaks
function formatResponseText(text) {
    if (!text || typeof text !== 'string') return '';
    
    // Escape HTML to prevent XSS
    const escapeHtml = (unsafe) => {
        if (!unsafe || typeof unsafe !== 'string') return '';
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    };
    
    const escapedText = escapeHtml(text);
    
    // Split by double line breaks to create paragraphs
    const paragraphs = escapedText.split(/\n\s*\n/);
    
    // Format each paragraph
    const formattedParagraphs = paragraphs.map(paragraph => {
        // Replace single line breaks with <br> within paragraphs
        const formattedParagraph = paragraph.replace(/\n/g, '<br>');
        return `<p>${formattedParagraph}</p>`;
    }).join('');
    
    return formattedParagraphs;
}

// Add at the top of the file, after other variable declarations
let currentState = {
    unit_id: null,
    state: 'conscious',
    consciousness_index: 0.57,
    metrics: {
        phi_score: 0.65,
        recursive_depth: 3,
        self_model_coherence: 0.98,
        temporal_binding: 1.0,
        novelty_generation: 0.8,
        witnessing_score: 0.7,
        prediction_accuracy: 0.0,
        attention_focus: 0.0,
        memory_integration: 0.0,

    }
};

// Verify DOM elements exist
if (!unitSelect) {
    console.error('Unit selection dropdown element not found');
    showToast('Error: Unit selection dropdown not found');
}

// Socket.IO event handlers
socket.on('connect', () => {
    console.log('Connected to server');
    fetchUnits();
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
    showToast('Disconnected from server');
});

socket.on('unit_update', (data) => {
    console.log('Received unit update via Socket.IO:', data);
    if (data && data.unit) {
        updateUnitInfo(data);
        // Also refresh the unit list to ensure consistency
        fetchUnits();
    } else if (data) {
        // Handle case where data is the unit itself
        updateUnitInfo({ unit: data });
        fetchUnits();
    }
});

// Fetch available units
async function fetchUnits() {
    try {
        console.log('Fetching units...');
        const response = await fetch('/api/units');
        let data;
        try {
            data = await response.json();
        } catch (parseErr) {
            console.error('Invalid JSON from /api/units:', parseErr);
            showToast('Server error: could not load units');
            return;
        }
        console.log('Fetched units:', data);
        // Only update dropdown when we have a successful response with valid units (never clear on error)
        if (data && data.status === 'success' && data.units && typeof data.units === 'object') {
            const units = data.units;
            updateUnitSelect(units);
            // Create default unit if no units exist
            if (Object.keys(units).length === 0) {
                console.log('No units found, creating default unit...');
                await createDefaultUnit();
            } else {
                if (!selectedUnitId && Object.keys(units).length > 0) {
                    const firstUnitId = Object.keys(units)[0];
                    console.log('Auto-selecting first unit:', firstUnitId);
                    await selectUnit(firstUnitId);
                } else if (selectedUnitId && units[selectedUnitId]) {
                    console.log('Updating info for currently selected unit:', selectedUnitId);
                    updateUnitInfo({ unit: units[selectedUnitId] });
                }
            }
        } else {
            console.error('Error fetching units:', data ? data.message : 'No data');
            showToast('Error fetching units: ' + (data && data.message ? data.message : 'Unknown error'));
        }
    } catch (error) {
        console.error('Error fetching units:', error);
        showToast('Error fetching units: ' + error.message);
    }
}

// Update unit select dropdown (always re-query element so we never use a stale/null reference)
function updateUnitSelect(units) {
    if (!units || typeof units !== 'object') {
        units = {};
    }
    try {
        const el = document.getElementById('unitSelect');
        if (!el) {
            console.error('Unit selection dropdown element not found');
            return;
        }
        el.innerHTML = '<option value="">Select a unit...</option>';
        Object.keys(units).forEach(unitId => {
            const option = document.createElement('option');
            option.value = unitId;
            option.textContent = unitId;
            if (unitId === selectedUnitId) {
                option.selected = true;
            }
            el.appendChild(option);
        });
    } catch (err) {
        console.error('updateUnitSelect error:', err);
    }
}

// Create default unit
async function createDefaultUnit() {
    try {
        console.log('Creating default unit...');
        const response = await fetch('/api/units', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ unit_id: 'default_unit' })
        });
        
        const data = await response.json();
        console.log('Create default unit response:', data);
        
        if (data.status === 'success') {
            console.log('Default unit created successfully');
            await fetchUnits();
        } else {
            console.error('Error creating default unit:', data.message);
            showToast('Error creating default unit: ' + data.message);
        }
    } catch (error) {
        console.error('Error creating default unit:', error);
        showToast('Error creating default unit: ' + error.message);
    }
}

// Create new unit
async function createUnit(unitId) {
    try {
        console.log('Creating new unit:', unitId);
        const response = await fetch('/api/units', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ unit_id: unitId })
        });
        let data;
        try {
            data = await response.json();
        } catch (parseErr) {
            console.error('Create unit: invalid response', parseErr);
            showToast('Server error: could not create unit');
            return false;
        }
        console.log('Create unit response:', data);

        if (!response.ok || data.status !== 'success') {
            console.error('Error creating unit:', data.message);
            showToast('Error creating unit: ' + (data.message || 'Unknown error'));
            return false;
        }
        showToast('Unit created successfully');
        hideCreateUnitModal();
        await fetchUnits();
        selectedUnitId = unitId;
        try {
            const el = document.getElementById('unitSelect');
            if (el) el.value = unitId;
            await selectUnit(unitId);
        } catch (selectErr) {
            console.warn('Could not select new unit:', selectErr);
            const el = document.getElementById('unitSelect');
            if (el) el.value = unitId;
        }
        return true;
    } catch (error) {
        console.error('Error creating unit:', error);
        showToast('Error creating unit: ' + error.message);
        return false;
    }
}

// Delete unit
async function deleteUnit(unitId) {
    try {
        console.log('Deleting unit:', unitId);
        const response = await fetch(`/api/units/${unitId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        console.log('Delete unit response:', data);
        
        if (data.status === 'success') {
            console.log('Unit deleted successfully');
            showToast('Unit deleted successfully');
            if (selectedUnitId === unitId) {
                selectedUnitId = null;
                if (unitSelect) {
                    unitSelect.value = '';
                }
                // Clear state and history displays
                updateUnitInfo({ state: '-', consciousness_index: '-' });
            }
            await fetchUnits();
        } else {
            console.error('Error deleting unit:', data.message);
            showToast('Error deleting unit: ' + data.message);
        }
    } catch (error) {
        console.error('Error deleting unit:', error);
        showToast('Error deleting unit: ' + error.message);
    }
}

// Select unit
async function selectUnit(unitId) {
    const unitSelectEl = document.getElementById('unitSelect');
    const outputEl = document.getElementById('processingResult');
    try {
        console.log('Selecting unit:', unitId);
        selectedUnitId = unitId;
        if (unitSelectEl) unitSelectEl.value = unitId;

        const stateResponse = await fetch(`/api/units/${unitId}/state`);
        const stateData = await stateResponse.json();
        if (stateData.status === 'success') {
            updateUnitInfo({ unit: stateData.state });
            const historyResponse = await fetch(`/api/history?unit_id=${unitId}`);
            const historyData = await historyResponse.json();
            if (historyData.status === 'success') {
                updateUnitHistory(historyData.history);
            } else {
                showToast('Error fetching unit history: ' + (historyData.message || ''));
                if (outputEl) outputEl.innerHTML = '<div class="no-history">No history available</div>';
            }
        } else {
            showToast('Error selecting unit: ' + (stateData.message || ''));
            selectedUnitId = null;
            if (unitSelectEl) unitSelectEl.value = '';
            updateUnitInfo({ unit: { state: '-', consciousness_index: 0 } });
            if (outputEl) outputEl.innerHTML = '<div class="no-history">Error selecting unit</div>';
        }
    } catch (error) {
        console.error('Error in selectUnit:', error);
        showToast('Error selecting unit: ' + error.message);
        selectedUnitId = null;
        if (unitSelectEl) unitSelectEl.value = '';
        updateUnitInfo({ unit: { state: '-', consciousness_index: 0 } });
        if (outputEl) outputEl.innerHTML = '<div class="no-history">Error selecting unit</div>';
    }
}

// Update unit info display
function updateUnitInfo(data) {
    console.log('🔄 Updating unit info with data:', data);
    
    // Get elements dynamically to ensure they exist
    const unitStateElement = document.getElementById('unitState');
    const unitConsciousnessIndexElement = document.getElementById('unitConsciousnessIndex');
    
    if (!data || !data.unit) {
        console.error('❌ Invalid unit data received:', data);
        if (unitStateElement) unitStateElement.textContent = '-';
        if (unitConsciousnessIndexElement) unitConsciousnessIndexElement.textContent = '-';
        return;
    }

    const unit = data.unit;
    console.log('📊 Unit data:', unit);
    console.log('🧠 Consciousness index value:', unit.consciousness_index, 'Type:', typeof unit.consciousness_index);

    if (unitStateElement) {
        unitStateElement.textContent = unit.state || '-';
        console.log('✅ Updated unit state to:', unitStateElement.textContent);
    } else {
        console.error('❌ unitState element not found!');
    }
    
    if (unitConsciousnessIndexElement) {
        const consciousnessValue = (unit.consciousness_index !== undefined && unit.consciousness_index !== null) ? unit.consciousness_index.toFixed(2) : '-';
        console.log('🎯 Setting consciousness index to:', consciousnessValue);
        unitConsciousnessIndexElement.textContent = consciousnessValue;
        console.log('✅ Element after update:', unitConsciousnessIndexElement.textContent);
        console.log('📝 Element innerHTML:', unitConsciousnessIndexElement.innerHTML);
        
        // Visual feedback - flash the element to show it updated
        unitConsciousnessIndexElement.style.backgroundColor = '#00ffff';
        unitConsciousnessIndexElement.style.color = '#0a1428';
        setTimeout(() => {
            unitConsciousnessIndexElement.style.backgroundColor = '';
            unitConsciousnessIndexElement.style.color = '';
        }, 1000);
    } else {
        console.error('❌ unitConsciousnessIndex element not found!');
        // Try to find it with a more specific selector
        const altElement = document.querySelector('#unitConsciousnessIndex');
        console.log('🔍 Alternative element search result:', altElement);
    }
}

// Update unit history display
function updateUnitHistory(history) {
    const processingResult = document.getElementById('processingResult');
    if (!processingResult) {
        console.error('Processing result element not found');
        return;
    }

    console.log('Updating history with:', history);
    
    if (!history || history.length === 0) {
        if (processingResult.children.length === 0) {
            processingResult.innerHTML = '<div class="empty-state">Enter some input to begin processing.</div>';
        }
        return;
    }

    // Remove empty state message if it exists
    const emptyState = processingResult.querySelector('.empty-state');
    if (emptyState) {
        emptyState.remove();
    }

    // Get existing entries
    const existingEntries = new Set();
    processingResult.querySelectorAll('.output-entry').forEach(entry => {
        const timestamp = entry.querySelector('.timestamp')?.textContent;
        if (timestamp) {
            existingEntries.add(timestamp);
        }
    });

    // Add only new entries
    history.forEach(entry => {
        const timestamp = new Date(entry.timestamp).toLocaleString();
        
        // Skip if this entry already exists
        if (existingEntries.has(timestamp)) {
            return;
        }

        console.log('Creating new entry for:', entry);
        
        const entryElement = document.createElement('div');
        entryElement.className = 'output-entry';
        
        // Get state and metrics
        const state = entry.consciousness_state || currentState;
        const metrics = state.metrics || {};
        
        // Create the entry HTML
        const entryHTML = `
            <div class="entry-header">
                <span class="timestamp">${timestamp}</span>
                <span class="state-badge">${state.state || 'conscious'}</span>
            </div>
            <div class="entry-content">
                <div class="input-section">
                    <strong>Input:</strong>
                    <p>${entry.input || ''}</p>
                </div>
                <div class="response-section">
                    <strong>Response:</strong>
                    <div class="response-text">${formatResponseText(entry.response || 'No response received')}</div>
                </div>
                <div class="follow-up-section">
                    <textarea class="follow-up-text" placeholder="Continue the conversation..."></textarea>
                    <button class="follow-up-btn">Continue Conversation</button>
                </div>
            </div>
            <div class="entry-metrics">
                <div class="metric">
                    <span class="metric-label">Consciousness Index:</span>
                    <span class="metric-value">${((state.consciousness_index || 0) * 100).toFixed(1)}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Phi Score:</span>
                    <span class="metric-value">${((metrics.phi_score || 0) * 100).toFixed(1)}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Recursive Depth:</span>
                    <span class="metric-value">${metrics.recursive_depth || 0}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Self-Model Coherence:</span>
                    <span class="metric-value">${((metrics.self_model_coherence || 0) * 100).toFixed(1)}%</span>
                </div>
            </div>
        `;

        console.log('Setting entry HTML:', entryHTML);
        entryElement.innerHTML = entryHTML;

        // Add follow-up handler using setTimeout to ensure DOM is ready
        setTimeout(() => {
            const followUpBtn = entryElement.querySelector('.follow-up-btn');
            const followUpText = entryElement.querySelector('.follow-up-text');
            
            console.log('Looking for follow-up elements:', {
                btn: followUpBtn,
                text: followUpText,
                entryHTML: entryElement.innerHTML.substring(0, 200)
            });
            
            if (followUpBtn && followUpText) {
                console.log('Adding click handler to follow-up button for entry:', entry.timestamp);
                
                followUpBtn.onclick = function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('History follow-up button clicked!');
                    
                    handleUniversalFollowUp(followUpBtn, entry.input, entry.response);
                };
            } else {
                console.error('Follow-up button or text not found!', {
                    btn: followUpBtn,
                    text: followUpText,
                    innerHTML: entryElement.innerHTML
                });
            }
        }, 100);

        // Add to the top of the output
        processingResult.insertBefore(entryElement, processingResult.firstChild);
    });

    // Scroll to the top to show the latest entry
    processingResult.scrollTop = 0;
}

// Safe number parsing: return default if element missing, empty, or NaN
function getNum(id, defaultVal) {
    const el = document.getElementById(id);
    if (!el || el.value === '') return defaultVal;
    const n = parseFloat(el.value);
    return Number.isFinite(n) ? n : defaultVal;
}
function getInt(id, defaultVal) {
    const el = document.getElementById(id);
    if (!el || el.value === '') return defaultVal;
    const n = parseInt(el.value, 10);
    return Number.isFinite(n) ? n : defaultVal;
}

function getCurrentParameters() {
    return {
        temperature: getNum('temperature', 0.7),
        top_p: getNum('topP', 0.9),
        max_tokens: getInt('maxTokens', 8192),
        presence_penalty: getNum('presencePenalty', 0.4),
        frequency_penalty: getNum('frequencyPenalty', 0.2),
        phi_score: getNum('phiScore', 0.8),
        recursive_depth: getInt('recursiveDepth', 6),
        self_model_coherence: getNum('selfModelCoherence', 0.95),
        temporal_binding: getNum('temporalBinding', 0.95),
        novelty_generation: getNum('noveltyGeneration', 0.75),
        witnessing_score: getNum('witnessingScore', 0.8),
        prediction_accuracy: getNum('predictionAccuracy', 0.5),
        attention_focus: getNum('attentionFocus', 0.65),
        memory_integration: getNum('memoryIntegration', 0.75)
    };
}

// Update the unit selection handler
function handleUnitSelection(unitId) {
    selectedUnitId = unitId;
    console.log('Selected unit:', unitId);
    updateURL();
    selectUnit(unitId); // This will properly load unit info and history
}

// Update the processInput function to handle form submission
async function processInput(event) {
    if (event) {
        event.preventDefault();
    }

    if (!selectedUnitId) {
        alert('Please select a unit first');
        return;
    }

    const inputText = document.getElementById('inputText').value.trim();
    if (!inputText) {
        alert('Please enter some input text');
        return;
    }

    const processingResult = document.getElementById('processingResult');
    if (!processingResult) {
        console.error('Processing result element not found');
        return;
    }

    // Get current state before processing
    try {
        await getCurrentState();
    } catch (error) {
        console.error('Error getting current state:', error);
        return;
    }

    // Update button state
    const processBtn = document.getElementById('processBtn');
    const btnText = processBtn.querySelector('.btn-text');
    const btnLoading = processBtn.querySelector('.btn-loading');
    
    processBtn.disabled = true;
    btnText.classList.add('hidden');
    btnLoading.classList.remove('hidden');
    processBtn.classList.add('loading');

    // Show loading state
    const loadingEntry = document.createElement('div');
    loadingEntry.className = 'output-entry loading';
    loadingEntry.innerHTML = `
        <div class="entry-header">
            <span class="timestamp">${new Date().toLocaleString()}</span>
            <span class="state-badge">processing...</span>
        </div>
        <div class="entry-content">
            <div class="input-section">
                <strong>Input:</strong>
                <p>${inputText}</p>
            </div>
            <div class="response-section">
                <strong>Response:</strong>
                <div class="response-text"><p>Processing your input...</p></div>
            </div>
        </div>
    `;
    processingResult.insertBefore(loadingEntry, processingResult.firstChild);

    try {
        console.log('Sending request to process input for unit:', selectedUnitId);
        const response = await fetch(`/api/units/${selectedUnitId}/process`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                input: inputText,
                parameters: getCurrentParameters()
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Raw API response:', data);

        // Extract response content from various possible locations
        let responseContent = null;
        
        if (data.choices && Array.isArray(data.choices) && data.choices[0]?.message?.content) {
            responseContent = data.choices[0].message.content;
            console.log('Found response in choices[0].message.content:', responseContent);
        } else if (data.response) {
            responseContent = data.response;
            console.log('Found response in data.response:', responseContent);
        } else if (data.consciousness_result) {
            responseContent = data.consciousness_result;
            console.log('Found response in consciousness_result:', responseContent);
        }

        // Clean up the response content
        console.log('Debug: responseContent type:', typeof responseContent, 'value:', responseContent);
        if (responseContent && typeof responseContent === 'string') {
            responseContent = responseContent.replace(/^\[[^\]]+\]\s*/, '').trim();
        } else {
            responseContent = 'No response received from the API';
        }

        // Create history entry
        const historyEntry = {
            timestamp: new Date().toISOString(),
            input: inputText,
            response: responseContent,
            consciousness_state: currentState
        };

        console.log('Created history entry:', historyEntry);

        // Update the loading entry with the actual response
        loadingEntry.classList.remove('loading');
        const responseSection = loadingEntry.querySelector('.response-section');
        if (responseSection) {
            responseSection.innerHTML = `
                <strong>Response:</strong>
                <div class="response-text">${formatResponseText(responseContent)}</div>
            `;
        }

        // Add follow-up section to the entry
        const entryContent = loadingEntry.querySelector('.entry-content');
        if (entryContent) {
            const followUpSection = document.createElement('div');
            followUpSection.className = 'follow-up-section';
            followUpSection.innerHTML = `
                <textarea class="follow-up-text" placeholder="Continue the conversation... (ask follow-up questions, request elaboration, challenge points, explore tangents)"></textarea>
                <button class="follow-up-btn" type="button">💬 Continue Conversation</button>
            `;
            entryContent.appendChild(followUpSection);

            // Add follow-up handler immediately (no setTimeout)
            const followUpBtn = followUpSection.querySelector('.follow-up-btn');
            const followUpText = followUpSection.querySelector('.follow-up-text');
            
            console.log('Looking for new response follow-up elements:', {
                btn: followUpBtn,
                text: followUpText
            });
            
            if (followUpBtn && followUpText) {
                console.log('Adding click handler to new follow-up button');
                
                followUpBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('New response follow-up button clicked!');
                    
                    handleUniversalFollowUp(followUpBtn, inputText, responseContent);
                });
            } else {
                console.error('New follow-up button or text not found!', {
                    btn: followUpBtn,
                    text: followUpText,
                    sectionHTML: followUpSection.innerHTML
                });
            }
        }

        // Add metrics section - use the actual state from the API response
        const actualState = data.state || currentState;
        const actualMetrics = actualState.metrics || {};
        const metricsSection = document.createElement('div');
        metricsSection.className = 'entry-metrics';
        metricsSection.innerHTML = `
            <div class="metric">
                <span class="metric-label">Consciousness Index:</span>
                <span class="metric-value">${((actualState.consciousness_index || 0) * 100).toFixed(1)}%</span>
            </div>
            <div class="metric">
                <span class="metric-label">Phi Score:</span>
                <span class="metric-value">${((actualMetrics.phi_score || 0) * 100).toFixed(1)}%</span>
            </div>
            <div class="metric">
                <span class="metric-label">Recursive Depth:</span>
                <span class="metric-value">${actualMetrics.recursive_depth || 0}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Self-Model Coherence:</span>
                <span class="metric-value">${((actualMetrics.self_model_coherence || 0) * 100).toFixed(1)}%</span>
            </div>
        `;
        loadingEntry.appendChild(metricsSection);

        // Update current state with the actual response data
        if (data.state) {
            currentState = data.state;
            // Update the unit info display with the new state
            updateUnitInfo({ unit: data.state });
        }

        // Add parameters toggle button at the end of the response
        const parametersRequested = getCurrentParameters();
        const parametersUsed = data.parameters_used || parametersRequested;
        
        // Add parameters toggle button to the response section
        const responseSectionElement = loadingEntry.querySelector('.response-section');
        if (responseSectionElement) {
            const parametersToggle = document.createElement('div');
            parametersToggle.className = 'response-parameters-toggle';
            parametersToggle.innerHTML = `
                <button class="show-params-btn" onclick="toggleResponseParameters(this)">
                    <span class="btn-text">🔧 Show Parameters</span>
                    <span class="btn-icon">▼</span>
                </button>
                <div class="response-parameters hidden">
                    <div class="parameters-grid">
                        <div class="param-group">
                            <h5>Model Parameters</h5>
                            <div class="param"><span>Temperature:</span> <span>${parametersRequested.temperature}</span></div>
                            <div class="param"><span>Top P:</span> <span>${parametersRequested.top_p}</span></div>
                            <div class="param"><span>Max Tokens:</span> <span>${parametersRequested.max_tokens}</span></div>
                            <div class="param"><span>Presence Penalty:</span> <span>${parametersRequested.presence_penalty}</span></div>
                            <div class="param"><span>Frequency Penalty:</span> <span>${parametersRequested.frequency_penalty}</span></div>
                        </div>
                        <div class="param-group">
                            <h5>Consciousness Parameters</h5>
                            <div class="param"><span>Recursive Depth:</span> <span>${parametersRequested.recursive_depth}</span></div>
                            <div class="param"><span>Phi Score:</span> <span>${parametersRequested.phi_score}</span></div>
                            <div class="param"><span>Self-Model Coherence:</span> <span>${parametersRequested.self_model_coherence}</span></div>
                            <div class="param"><span>Novelty Generation:</span> <span>${parametersRequested.novelty_generation}</span></div>
                            <div class="param"><span>Witnessing Score:</span> <span>${parametersRequested.witnessing_score}</span></div>
                            <div class="param"><span>Temporal Binding:</span> <span>${parametersRequested.temporal_binding}</span></div>
                            <div class="param"><span>Prediction Accuracy:</span> <span>${parametersRequested.prediction_accuracy}</span></div>
                            <div class="param"><span>Attention Focus:</span> <span>${parametersRequested.attention_focus}</span></div>
                            <div class="param"><span>Memory Integration:</span> <span>${parametersRequested.memory_integration}</span></div>
                        </div>
                    </div>
                </div>
            `;
            responseSectionElement.appendChild(parametersToggle);
        }

        // Debug: Log the final structure of the entry
        console.log('Final entry structure:', {
            entry: loadingEntry,
            followUpSection: loadingEntry.querySelector('.follow-up-section'),
            followUpBtn: loadingEntry.querySelector('.follow-up-btn'),
            followUpText: loadingEntry.querySelector('.follow-up-text')
        });
        
        // Clear input and update history
        document.getElementById('inputText').value = '';
        await updateHistory();
        
        // Force refresh unit state to ensure we have the latest consciousness index
        await forceRefreshUnitState();
        
        // Show feedback section after successful processing
        showFeedbackSection();

    } catch (error) {
        console.error('Error processing input:', error);
        loadingEntry.classList.remove('loading');
        const responseSection = loadingEntry.querySelector('.response-section');
        if (responseSection) {
            responseSection.innerHTML = `
                <strong>Response:</strong>
                <div class="response-text"><p>Error processing input: ${error.message}</p></div>
            `;
        }
    } finally {
        // Reset button state
        processBtn.disabled = false;
        btnText.classList.remove('hidden');
        btnLoading.classList.add('hidden');
        processBtn.classList.remove('loading');
    }
}

// Force refresh unit state function
async function forceRefreshUnitState() {
    if (!selectedUnitId) return;
    
    console.log('Force refreshing unit state for:', selectedUnitId);
    try {
        // First refresh all units to get the latest data
        await fetchUnits();
        
        // Then get the specific unit state
        const stateResponse = await fetch(`/api/units/${selectedUnitId}/state`);
        const stateData = await stateResponse.json();
        
        if (stateData.status === 'success') {
            console.log('Refreshed unit state:', stateData.state);
            updateUnitInfo({ unit: stateData.state });
            
            // Also update the current state global variable
            currentState = stateData.state;
        } else {
            console.error('Error in state response:', stateData);
        }
    } catch (error) {
        console.error('Error force refreshing unit state:', error);
    }
}

// Add these functions before processInput
async function getUnitHistory() {
    try {
        const response = await fetch(`/api/history?unit_id=${selectedUnitId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Fetched history:', data);
        return data;
    } catch (error) {
        console.error('Error fetching history:', error);
        return [];
    }
}

async function updateHistory() {
    try {
        const history = await getUnitHistory();
        console.log('Updating history with:', history);
        updateUnitHistory(history);
    } catch (error) {
        console.error('Error updating history:', error);
    }
}

// Update processing result display
function updateProcessingResult(data) {
    if (processingResult) {
        const entryElement = document.createElement('div');
        entryElement.className = 'output-entry';
        entryElement.innerHTML = `
            <div class="entry-header">
                <span class="timestamp">${new Date().toLocaleString()}</span>
                <span class="state">${data.unit.state}</span>
            </div>
            <div class="entry-content">
                <div class="input">${data.input}</div>
                <div class="response">${data.response}</div>
            </div>
            <div class="entry-metrics">
                <div class="metric">Consciousness Index: ${data.unit.consciousness_index.toFixed(2)}</div>
                <div class="metric">Reflection Quality: ${data.unit.reflection_quality.toFixed(2)}</div>
            </div>
        `;
        processingResult.insertBefore(entryElement, processingResult.firstChild);
    }
}

// Show create unit modal
function showCreateUnitModal() {
    if (createUnitModal) {
        createUnitModal.classList.remove('hidden');
    }
}

// Hide create unit modal
function hideCreateUnitModal() {
    if (createUnitModal) {
        createUnitModal.classList.add('hidden');
        if (createUnitForm) {
            createUnitForm.reset();
        }
    }
}

// Toggle parameters panel
function toggleParameters() {
    const parametersContent = document.getElementById('parametersContent');
    if (parametersContent) {
        parametersContent.classList.toggle('hidden');
    }
}

// Toggle response parameters
function toggleResponseParameters(button) {
    const parametersContainer = button.parentElement.querySelector('.response-parameters');
    const btnText = button.querySelector('.btn-text');
    const btnIcon = button.querySelector('.btn-icon');
    
    if (parametersContainer) {
        const isHidden = parametersContainer.classList.contains('hidden');
        parametersContainer.classList.toggle('hidden');
        
        if (isHidden) {
            btnText.textContent = '🔧 Hide Parameters';
            btnIcon.textContent = '▲';
        } else {
            btnText.textContent = '🔧 Show Parameters';
            btnIcon.textContent = '▼';
        }
    }
}

// Show toast notification
function showToast(message, duration = 3000) {
    if (toast) {
        toast.textContent = message;
        toast.classList.remove('hidden');
        setTimeout(() => {
            toast.classList.add('hidden');
        }, duration);
    }
}

// Update URL with current parameters
function updateURL() {
    if (!selectedUnitId) return;

    const params = new URLSearchParams(window.location.search);
    
    // Update unit ID
    params.set('unit_id', selectedUnitId);
    
    // Update processing parameters
    params.set('temperature', temperatureInput?.value || '0.7');
    params.set('top_p', topPInput?.value || '0.9');
    params.set('max_tokens', maxTokensInput?.value || '15000');
    params.set('presence_penalty', presencePenaltyInput?.value || '0');
    
    // Update URL without reloading the page
    const newUrl = `${window.location.pathname}?${params.toString()}`;
    window.history.pushState({}, '', newUrl);
}

// Load parameters from URL on page load
function loadParametersFromURL() {
    const params = new URLSearchParams(window.location.search);
    
    // Load unit ID
    const unitId = params.get('unit_id');
    if (unitId && unitSelect) {
        unitSelect.value = unitId;
        selectUnit(unitId);
    }
    
    // Load processing parameters
    if (temperatureInput) temperatureInput.value = params.get('temperature') || '0.7';
    if (topPInput) topPInput.value = params.get('top_p') || '0.9';
    if (maxTokensInput) maxTokensInput.value = params.get('max_tokens') || '15000';
    if (presencePenaltyInput) presencePenaltyInput.value = params.get('presence_penalty') || '0';
}

// Initialize event listeners
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing event listeners...');
    
    // Load parameters from URL
    loadParametersFromURL();
    
    // Unit selection dropdown
    if (unitSelect) {
        console.log('Adding change event listener to unit select');
        unitSelect.addEventListener('change', (e) => {
            console.log('Unit select changed:', e.target.value);
            const selectedValue = e.target.value;
            if (selectedValue) {
                selectUnit(selectedValue);
            } else {
                // Clear unit info if no unit is selected
                selectedUnitId = null;
                updateUnitInfo({ unit: { state: '-', consciousness_index: 0 } });
                if (processingResult) {
                    processingResult.innerHTML = '<div class="no-history">No unit selected</div>';
                }
            }
        });
    } else {
        console.error('Unit selection dropdown not found during initialization');
    }
    
    // Input form
    const inputForm = document.getElementById('inputForm');
    if (inputForm) {
        console.log('Adding submit event listener to input form');
        inputForm.addEventListener('submit', processInput);
    } else {
        console.error('Input form not found during initialization');
    }
    
    // Create unit form
    if (createUnitForm) {
        console.log('Adding submit event listener to create unit form');
        createUnitForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            try {
                console.log('Create unit form submitted');
                const unitIdInput = document.getElementById('unitId');
                const unitId = unitIdInput ? unitIdInput.value.trim() : '';
                if (!unitId) {
                    showToast('Please enter a unit ID');
                    return;
                }
                const success = await createUnit(unitId);
                if (success) {
                    hideCreateUnitModal();
                }
            } catch (err) {
                console.error('Create unit form error:', err);
                showToast('Something went wrong. Please try again.');
            }
        });
    } else {
        console.error('Create unit form not found during initialization');
    }
    
    // Initialize units
    console.log('Fetching initial units...');
    fetchUnits();

    // Autonomous mode button removed



    // Add change listeners for parameter inputs
    const parameterInputs = [temperatureInput, topPInput, maxTokensInput, presencePenaltyInput];
    parameterInputs.forEach(input => {
        if (input) {
            input.addEventListener('change', updateURL);
        }
    });

    // Parameter info buttons: click "i" to show/hide description popover
    document.addEventListener('click', function(e) {
        const btn = e.target.closest('.param-info-btn');
        if (btn) {
            e.preventDefault();
            e.stopPropagation();
            const paramId = btn.getAttribute('data-param');
            if (paramId) showParamInfo(paramId, btn);
            return;
        }
        if (!e.target.closest('.param-info-popover')) {
            hideParamInfo();
        }
    });

    // Parameter panel functionality
    const parametersContent = document.getElementById('parametersContent');
    const toggleParamsBtn = document.getElementById('toggleParams');
    
    // Set initial state
    parametersContent.style.display = 'flex';
    
    // Toggle parameters panel
    toggleParamsBtn.addEventListener('click', function() {
        const isVisible = parametersContent.style.display === 'flex';
        parametersContent.style.display = isVisible ? 'none' : 'flex';
        toggleParamsBtn.textContent = isVisible ? 'Show Parameters' : 'Hide Parameters';
    });
    
    // Sync range and number inputs for all parameters
    const parameterGroups = [
        // Model Parameters
        { range: 'temperature', number: 'temperatureValue', min: 0, max: 2, step: 0.1 },
        { range: 'topP', number: 'topPValue', min: 0, max: 1, step: 0.1 },
        { range: 'maxTokens', number: 'maxTokensValue', min: 1, max: 15000, step: 1 },
        { range: 'presencePenalty', number: 'presencePenaltyValue', min: -2, max: 2, step: 0.1 },
        { range: 'frequencyPenalty', number: 'frequencyPenaltyValue', min: -2, max: 2, step: 0.1 },
        
        // Consciousness Metrics
        { range: 'phiScore', number: 'phiScoreValue', min: 0, max: 1, step: 0.01 },
        { range: 'recursiveDepth', number: 'recursiveDepthValue', min: 1, max: 10, step: 1 },
        { range: 'selfModelCoherence', number: 'selfModelCoherenceValue', min: 0, max: 1, step: 0.01 },
        { range: 'temporalBinding', number: 'temporalBindingValue', min: 0, max: 1, step: 0.01 },
        { range: 'noveltyGeneration', number: 'noveltyGenerationValue', min: 0, max: 1, step: 0.01 },
        { range: 'witnessingScore', number: 'witnessingScoreValue', min: 0, max: 1, step: 0.01 },
        { range: 'predictionAccuracy', number: 'predictionAccuracyValue', min: 0, max: 1, step: 0.01 },
        { range: 'attentionFocus', number: 'attentionFocusValue', min: 0, max: 1, step: 0.01 },
        { range: 'memoryIntegration', number: 'memoryIntegrationValue', min: 0, max: 1, step: 0.01 },

    ];
    
    parameterGroups.forEach(param => {
        const rangeInput = document.getElementById(param.range);
        const numberInput = document.getElementById(param.number);
        
        if (rangeInput && numberInput) {
            // Sync range to number
            rangeInput.addEventListener('input', function() {
                numberInput.value = this.value;
                updateURL();
            });
            
            // Sync number to range
            numberInput.addEventListener('input', function() {
                let value = parseFloat(this.value);
                // Enforce min/max constraints
                value = Math.max(param.min, Math.min(param.max, value));
                // Round to step precision
                value = Math.round(value / param.step) * param.step;
                this.value = value;
                rangeInput.value = value;
                updateURL();
            });
        }
    });
});

// Autonomous mode functions removed for cleaner interface

// Clear processing history
function clearHistory() {
    const processingResult = document.getElementById('processingResult');
    if (processingResult) {
        processingResult.innerHTML = '<div class="no-history">No processing history yet</div>';
    }
}

// Update the follow-up handler to use the same response extraction logic
async function handleFollowUp(followUpInput, parentEntry, followUpBtn, followUpText) {
    try {
        console.log('Processing follow-up:', followUpInput);
        console.log('Parent entry:', parentEntry);

        // Get current state before processing
        await getCurrentState();

        // Create a new history entry for the follow-up
        const followUpEntry = {
            timestamp: new Date().toISOString(),
            input: followUpInput,
            parent_timestamp: parentEntry.timestamp,
            consciousness_state: currentState
        };

        // Build conversation context for true follow-up
        const conversationContext = {
            previous_input: parentEntry.input,
            previous_response: parentEntry.response,
            follow_up_input: followUpInput,
            conversation_type: "unrestrained_follow_up"
        };

        // Send the follow-up request with full conversation context
        const response = await fetch(`/api/units/${selectedUnitId}/process`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                input: followUpInput,
                parent_timestamp: parentEntry.timestamp,
                conversation_context: conversationContext,
                is_follow_up: true,
                parameters: getCurrentParameters()
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Follow-up API response:', data);

        // Extract response content
        let responseContent = null;
        if (data.choices && Array.isArray(data.choices) && data.choices[0]?.message?.content) {
            responseContent = data.choices[0].message.content;
        } else if (data.response) {
            responseContent = data.response;
        } else if (data.consciousness_result) {
            responseContent = data.consciousness_result;
        }

        console.log('Debug: followUp responseContent type:', typeof responseContent, 'value:', responseContent);
        if (responseContent && typeof responseContent === 'string') {
            responseContent = responseContent.replace(/^\[[^\]]+\]\s*/, '').trim();
        } else {
            responseContent = 'No response received from the API';
        }
        
        // Update the follow-up entry with the response
        followUpEntry.response = responseContent;

        // Create the follow-up entry element
        const followUpElement = document.createElement('div');
        followUpElement.className = 'output-entry follow-up';
        followUpElement.innerHTML = `
            <div class="entry-header">
                <span class="timestamp">${new Date(followUpEntry.timestamp).toLocaleString()}</span>
                <span class="state-badge">${currentState.state || 'unknown'}</span>
            </div>
            <div class="entry-content">
                <div class="input-section">
                    <strong>Follow-up:</strong>
                    <p>${followUpEntry.input}</p>
                </div>
                <div class="response-section">
                    <strong>Response:</strong>
                    <p>${followUpEntry.response}</p>
                </div>
            </div>
            <div class="entry-metrics">
                <div class="metric">
                    <span class="metric-label">Consciousness Index:</span>
                    <span class="metric-value">${((currentState.consciousness_index || 0) * 100).toFixed(1)}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Phi Score:</span>
                    <span class="metric-value">${((currentState.metrics?.phi_score || 0) * 100).toFixed(1)}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Recursive Depth:</span>
                    <span class="metric-value">${currentState.metrics?.recursive_depth || 0}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Self-Model Coherence:</span>
                    <span class="metric-value">${((currentState.metrics?.self_model_coherence || 0) * 100).toFixed(1)}%</span>
                </div>
            </div>
        `;

        // Find the parent entry element and insert the follow-up after it
        const parentElement = document.querySelector(`.output-entry[data-timestamp="${parentEntry.timestamp}"]`);
        if (parentElement) {
            parentElement.parentNode.insertBefore(followUpElement, parentElement.nextSibling);
        } else {
            // If parent element not found, append to the processing result
            const processingResult = document.getElementById('processingResult');
            if (processingResult) {
                processingResult.insertBefore(followUpElement, processingResult.firstChild);
            }
        }

        // Update the history
        await updateHistory();

        // Reset the follow-up input
        followUpText.value = '';
        followUpText.disabled = false;
        followUpBtn.disabled = false;
        followUpBtn.textContent = 'Send Follow-up';

    } catch (error) {
        console.error('Error processing follow-up:', error);
        followUpText.disabled = false;
        followUpBtn.disabled = false;
        followUpBtn.textContent = 'Send Follow-up';
        
        // Show error in the follow-up section
        const errorElement = document.createElement('div');
        errorElement.className = 'error-message';
        errorElement.textContent = 'Error processing follow-up: ' + error.message;
        followUpText.parentNode.appendChild(errorElement);
    }
}

async function getCurrentState() {
    if (!selectedUnitId) return currentState;
    
    try {
        const response = await fetch(`/api/units/${selectedUnitId}/state`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (data && data.state) {
            currentState = data.state;
        }
        return currentState;
    } catch (error) {
        console.error('Error fetching state:', error);
        return currentState;
    }
}

// Feedback system
function sendFeedback(feedbackType) {
    const currentUnit = getCurrentUnit();
    if (!currentUnit) {
        showToast('Please select a unit first', 'error');
        return;
    }
    
    fetch(`/api/units/${currentUnit}/feedback`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            feedback_type: feedbackType,
            intensity: 1.0
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showToast(`Feedback sent: ${feedbackType}`, 'success');
            // Hide feedback section after sending
            document.getElementById('feedbackSection').style.display = 'none';
            // Refresh unit info to show updated consciousness index
            loadUnitInfo(currentUnit);
        } else {
            showToast(`Error sending feedback: ${data.message}`, 'error');
        }
    })
    .catch(error => {
        console.error('Error sending feedback:', error);
        showToast('Error sending feedback', 'error');
    });
}

function showFeedbackSection() {
    const feedbackSection = document.getElementById('feedbackSection');
    if (feedbackSection) {
        feedbackSection.style.display = 'block';
    }
}

function getCurrentUnit() {
    const unitSelect = document.getElementById('unitSelect');
    return unitSelect ? unitSelect.value : null;
}

// Load/refresh unit info display (e.g. after feedback)
async function loadUnitInfo(unitId) {
    if (!unitId) return;
    try {
        const response = await fetch(`/api/units/${unitId}/state`);
        const data = await response.json();
        if (data.status === 'success' && data.state) {
            updateUnitInfo({ unit: data.state });
            currentState = data.state;
        }
    } catch (error) {
        console.error('Error loading unit info:', error);
    }
}

// Storage Management Functions
async function viewConversationHistory() {
    try {
        const selectedUnit = getCurrentUnit();
        const url = selectedUnit ? `/api/conversations?unit_id=${selectedUnit}&limit=50` : '/api/conversations?limit=50';
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.status === 'success') {
            displayConversationHistory(data.conversations);
        } else {
            showToast('Error loading conversations: ' + data.message);
        }
    } catch (error) {
        console.error('Error loading conversations:', error);
        showToast('Error loading conversations: ' + error.message);
    }
}

async function viewSessions() {
    try {
        const response = await fetch('/api/sessions');
        const data = await response.json();
        
        if (data.status === 'success') {
            await displaySessions(data.sessions);
        } else {
            showToast('Error loading sessions: ' + data.message);
        }
    } catch (error) {
        console.error('Error loading sessions:', error);
        showToast('Error loading sessions: ' + error.message);
    }
}

async function exportAllData() {
    try {
        const response = await fetch('/api/export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            showToast(`Data exported successfully! File: ${data.export_path}`);
        } else {
            showToast('Error exporting data: ' + data.message);
        }
    } catch (error) {
        console.error('Error exporting data:', error);
        showToast('Error exporting data: ' + error.message);
    }
}

async function showStorageStats() {
    try {
        const response = await fetch('/api/storage/stats');
        const data = await response.json();
        
        if (data.status === 'success') {
            displayStorageStats(data);
        } else {
            showToast('Error loading storage stats: ' + data.message);
        }
    } catch (error) {
        console.error('Error loading storage stats:', error);
        showToast('Error loading storage stats: ' + error.message);
    }
}

function displayConversationHistory(conversations) {
    const outputContent = document.getElementById('processingResult');
    if (!outputContent) return;
    
    // Clear existing content
    outputContent.innerHTML = '';
    
    // Create conversation history container
    const conversationHistory = document.createElement('div');
    conversationHistory.className = 'conversation-history';
    
    const title = document.createElement('h3');
    title.textContent = 'All Conversations';
    conversationHistory.appendChild(title);
    
    if (conversations.length === 0) {
        const emptyState = document.createElement('div');
        emptyState.className = 'empty-state';
        emptyState.textContent = 'No conversations found.';
        conversationHistory.appendChild(emptyState);
    } else {
        conversations.forEach(conv => {
            const datetime = new Date(conv.datetime).toLocaleString();
            const consciousnessIndex = ((conv.consciousness_state?.consciousness_index || 0) * 100).toFixed(1);
            
            // Create conversation entry element
            const entryElement = document.createElement('div');
            entryElement.className = 'conversation-entry';
            
            entryElement.innerHTML = `
                <div class="conv-header">
                    <span class="conv-time">${datetime}</span>
                    <span class="conv-unit">Unit: ${conv.consciousness_state?.unit_id || 'unknown'}</span>
                    <span class="conv-consciousness">CI: ${consciousnessIndex}%</span>
                </div>
                <div class="conv-input">
                    <strong>Input:</strong> ${conv.input}
                </div>
                <div class="conv-output">
                    <strong>Output:</strong> ${formatResponseText(conv.output)}
                    <div class="follow-up-section">
                        <textarea class="follow-up-text" placeholder="Continue the conversation..."></textarea>
                        <button class="follow-up-btn">Continue Conversation</button>
                    </div>
                    <div class="response-parameters-toggle">
                        <button class="show-params-btn" onclick="toggleResponseParameters(this)">
                            <span class="btn-text">🔧 Show Parameters</span>
                            <span class="btn-icon">▼</span>
                        </button>
                        <div class="response-parameters hidden">
                            <div class="parameters-grid">
                                <div class="param-group">
                                    <h5>Model Parameters</h5>
                                    <div class="param"><span>Temperature:</span> <span>${conv.parameters?.temperature || '0.7'}</span></div>
                                    <div class="param"><span>Top P:</span> <span>${conv.parameters?.top_p || '0.9'}</span></div>
                                    <div class="param"><span>Max Tokens:</span> <span>${conv.parameters?.max_tokens || '15000'}</span></div>
                                    <div class="param"><span>Presence Penalty:</span> <span>${conv.parameters?.presence_penalty || '0'}</span></div>
                                    <div class="param"><span>Frequency Penalty:</span> <span>${conv.parameters?.frequency_penalty || '0'}</span></div>
                                </div>
                                <div class="param-group">
                                    <h5>Consciousness Parameters</h5>
                                    <div class="param"><span>Recursive Depth:</span> <span>${conv.parameters?.recursive_depth || '3'}</span></div>
                                    <div class="param"><span>Phi Score:</span> <span>${conv.parameters?.phi_score || '0.65'}</span></div>
                                    <div class="param"><span>Self-Model Coherence:</span> <span>${conv.parameters?.self_model_coherence || '0.98'}</span></div>
                                    <div class="param"><span>Novelty Generation:</span> <span>${conv.parameters?.novelty_generation || '0.8'}</span></div>
                                    <div class="param"><span>Witnessing Score:</span> <span>${conv.parameters?.witnessing_score || '0.7'}</span></div>
                                    <div class="param"><span>Temporal Binding:</span> <span>${conv.parameters?.temporal_binding || '1.0'}</span></div>
                                    <div class="param"><span>Prediction Accuracy:</span> <span>${conv.parameters?.prediction_accuracy || '0.0'}</span></div>
                                    <div class="param"><span>Attention Focus:</span> <span>${conv.parameters?.attention_focus || '0.0'}</span></div>
                                    <div class="param"><span>Memory Integration:</span> <span>${conv.parameters?.memory_integration || '0.0'}</span></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Add event listener to the follow-up button
            const followUpBtn = entryElement.querySelector('.follow-up-btn');
            const followUpText = entryElement.querySelector('.follow-up-text');
            
            if (followUpBtn && followUpText) {
                followUpBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('Conversation history follow-up button clicked!');
                    
                    handleUniversalFollowUp(followUpBtn, conv.input, conv.output);
                });
            }
            
            conversationHistory.appendChild(entryElement);
        });
    }
    
    outputContent.appendChild(conversationHistory);
}

async function displaySessions(sessions) {
    const outputContent = document.getElementById('processingResult');
    if (!outputContent) return;
    
    let html = '<div class="sessions-view">';
    html += '<h3>All Sessions</h3>';
    
    if (sessions.length === 0) {
        html += '<div class="empty-state">No sessions found.</div>';
        outputContent.innerHTML = html;
        return;
    }
    
    // Fetch first conversation for each session to get the input
    const sessionPromises = sessions.map(async (session) => {
        try {
            const response = await fetch(`/api/conversations?session_id=${session.session_id}&limit=1`);
            const data = await response.json();
            
            let firstInput = 'Session ' + session.session_id;
            if (data.status === 'success' && data.conversations.length > 0) {
                const firstConversation = data.conversations[0];
                firstInput = firstConversation.input || 'No input available';
                // Truncate long inputs
                if (firstInput.length > 100) {
                    firstInput = firstInput.substring(0, 97) + '...';
                }
            }
            
            return {
                ...session,
                firstInput: firstInput
            };
        } catch (error) {
            console.error('Error fetching first conversation for session:', session.session_id, error);
            return {
                ...session,
                firstInput: 'Session ' + session.session_id
            };
        }
    });
    
    try {
        const sessionsWithInputs = await Promise.all(sessionPromises);
        
        sessionsWithInputs.forEach(session => {
            const startTime = new Date(session.start_time * 1000).toLocaleString();
            
            html += `
                <div class="session-entry">
                    <div class="session-header">
                        <span class="session-name">${session.firstInput}</span>
                        <span class="session-time">${startTime}</span>
                    </div>
                    <div class="session-details">
                        <div class="session-info">
                            <span>Conversations: ${session.conversation_count}</span>
                            <span>Units: ${session.units.join(', ')}</span>
                            <span class="session-id-small">ID: ${session.session_id}</span>
                        </div>
                        <div class="session-actions">
                            <button onclick="loadSessionConversations('${session.session_id}')" class="load-session-btn">Load Session</button>
                            <button onclick="deleteSession('${session.session_id}')" class="delete-session-btn" title="Delete Session">
                                <span class="delete-icon">🗑️</span>
                                Delete
                            </button>
                        </div>
                    </div>
                </div>
            `;
        });
    } catch (error) {
        console.error('Error processing sessions:', error);
        // Fallback to original display if there's an error
        sessions.forEach(session => {
            const startTime = new Date(session.start_time * 1000).toLocaleString();
            
            html += `
                <div class="session-entry">
                    <div class="session-header">
                        <span class="session-id">${session.session_id}</span>
                        <span class="session-time">${startTime}</span>
                    </div>
                    <div class="session-details">
                        <div class="session-info">
                            <span>Conversations: ${session.conversation_count}</span>
                            <span>Units: ${session.units.join(', ')}</span>
                        </div>
                        <div class="session-actions">
                            <button onclick="loadSessionConversations('${session.session_id}')" class="load-session-btn">Load Session</button>
                            <button onclick="deleteSession('${session.session_id}')" class="delete-session-btn" title="Delete Session">
                                <span class="delete-icon">🗑️</span>
                                Delete
                            </button>
                        </div>
                    </div>
                </div>
            `;
        });
    }
    
    html += '</div>';
    outputContent.innerHTML = html;
}

function displayStorageStats(stats) {
    const outputContent = document.getElementById('processingResult');
    if (!outputContent) return;
    
    let html = '<div class="storage-stats">';
    html += '<h3>Storage Statistics</h3>';
    html += `
        <div class="stats-grid">
            <div class="stat-item">
                <span class="stat-label">Storage Directory:</span>
                <span class="stat-value">${stats.storage_directory}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Total Conversations:</span>
                <span class="stat-value">${stats.total_conversations}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Total Units:</span>
                <span class="stat-value">${stats.total_units}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Total Sessions:</span>
                <span class="stat-value">${stats.total_sessions}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Session Logs:</span>
                <span class="stat-value">${stats.session_logs_count}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Current Session:</span>
                <span class="stat-value">${stats.current_session}</span>
            </div>
        </div>
        <div class="files-info">
            <h4>Storage Files:</h4>
            <ul>
                <li>Conversations: ${stats.files.conversations}</li>
                <li>Consciousness States: ${stats.files.consciousness_states}</li>
                <li>Processing History: ${stats.files.processing_history}</li>
                <li>Session Logs: ${stats.files.session_logs}</li>
            </ul>
        </div>
    `;
    html += '</div>';
    outputContent.innerHTML = html;
}

async function loadSessionConversations(sessionId) {
    try {
        const response = await fetch(`/api/conversations?session_id=${sessionId}&limit=100`);
        const data = await response.json();
        
        if (data.status === 'success') {
            displayConversationHistory(data.conversations);
            showToast(`Loaded ${data.conversations.length} conversations from session ${sessionId}`);
        } else {
            showToast('Error loading session conversations: ' + data.message);
        }
    } catch (error) {
        console.error('Error loading session conversations:', error);
        showToast('Error loading session conversations: ' + error.message);
    }
}

async function createNewSession() {
    try {
        const response = await fetch('/api/sessions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            showToast(`New session created successfully! Session ID: ${data.session_id}`);
            
            // Clear the current processing result to show a fresh start
            const processingResult = document.getElementById('processingResult');
            if (processingResult) {
                processingResult.innerHTML = '<div class="empty-state">New session started. Enter some input to begin processing.</div>';
            }
        } else {
            showToast('Error creating new session: ' + data.message);
        }
    } catch (error) {
        console.error('Error creating new session:', error);
        showToast('Error creating new session: ' + error.message);
    }
}

async function deleteSession(sessionId) {
    // Show confirmation dialog
    const confirmed = confirm(`Are you sure you want to delete session "${sessionId}"?\n\nThis will permanently delete all conversations in this session. This action cannot be undone.`);
    
    if (!confirmed) {
        return;
    }
    
    try {
        const response = await fetch(`/api/sessions/${sessionId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            showToast(`Session ${sessionId} deleted successfully. ${data.conversations_deleted} conversations removed.`);
            
            // Refresh the sessions view
            await viewSessions();
        } else {
            showToast('Error deleting session: ' + data.message);
        }
    } catch (error) {
        console.error('Error deleting session:', error);
        showToast('Error deleting session: ' + error.message);
    }
}



// Event listeners for storage management buttons
document.addEventListener('DOMContentLoaded', function() {
    const viewConversationsBtn = document.getElementById('viewConversationsBtn');
    const newSessionBtn = document.getElementById('newSessionBtn');
    const viewSessionsBtn = document.getElementById('viewSessionsBtn');
    const exportDataBtn = document.getElementById('exportDataBtn');
    const storageStatsBtn = document.getElementById('storageStatsBtn');
    
    if (viewConversationsBtn) {
        viewConversationsBtn.addEventListener('click', viewConversationHistory);
    }
    
    if (newSessionBtn) {
        newSessionBtn.addEventListener('click', createNewSession);
    }
    
    if (viewSessionsBtn) {
        viewSessionsBtn.addEventListener('click', viewSessions);
    }
    
    if (exportDataBtn) {
        exportDataBtn.addEventListener('click', exportAllData);
    }
    
    if (storageStatsBtn) {
        storageStatsBtn.addEventListener('click', showStorageStats);
    }
});

// Universal follow-up handler that works for all conversation types
async function handleUniversalFollowUp(button, originalInput, originalOutput) {
    const followUpText = button.parentElement.querySelector('.follow-up-text');
    if (!followUpText) {
        console.error('Follow-up text area not found');
        alert('Follow-up text area not found. Please refresh the page.');
        return;
    }
    
    const followUpInput = followUpText.value.trim();
    
    if (!followUpInput) {
        alert('Please enter your follow-up message');
        return;
    }

    // Disable the input and button
    followUpText.disabled = true;
    button.disabled = true;
    button.textContent = '🔄 Continuing conversation...';

    try {
        const selectedUnitId = getCurrentUnit();
        if (!selectedUnitId) {
            alert('Please select a consciousness unit');
            return;
        }

        // Create context with conversation history
        const contextualInput = `Previous conversation:
Input: ${originalInput}
Output: ${originalOutput}

Follow-up: ${followUpInput}`;

        const response = await fetch(`/api/units/${selectedUnitId}/process`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                input: contextualInput,
                parameters: getCurrentParameters()
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Follow-up API response:', data);

        // Extract response content
        let responseContent = data.response || 'No response received from the API';

        // Create new conversation entry for the follow-up
        const newEntry = {
            timestamp: new Date().toISOString(),
            input: followUpInput,
            response: responseContent,
            consciousness_state: data.state || {}
        };

        // Add the new entry to the conversation history
        const outputContent = document.getElementById('processingResult');
        const conversationHistory = outputContent.querySelector('.conversation-history');
        
        if (conversationHistory) {
            // Create HTML for the new conversation entry
            const datetime = new Date(newEntry.timestamp).toLocaleString();
            const consciousnessIndex = ((newEntry.consciousness_state?.consciousness_index || 0) * 100).toFixed(1);
            
            // Create new conversation entry element
            const newEntryElement = document.createElement('div');
            newEntryElement.className = 'conversation-entry';
            
            newEntryElement.innerHTML = `
                <div class="conv-header">
                    <span class="conv-time">${datetime}</span>
                    <span class="conv-unit">Unit: ${newEntry.consciousness_state?.unit_id || 'unknown'}</span>
                    <span class="conv-consciousness">CI: ${consciousnessIndex}%</span>
                </div>
                <div class="conv-input">
                    <strong>Follow-up:</strong> ${newEntry.input}
                </div>
                <div class="conv-output">
                    <strong>Output:</strong> ${formatResponseText(newEntry.response)}
                    <div class="follow-up-section">
                        <textarea class="follow-up-text" placeholder="Continue the conversation..."></textarea>
                        <button class="follow-up-btn">Continue Conversation</button>
                    </div>
                </div>
            `;
            
            // Add event listener to the new follow-up button
            const newFollowUpBtn = newEntryElement.querySelector('.follow-up-btn');
            const newFollowUpText = newEntryElement.querySelector('.follow-up-text');
            
            if (newFollowUpBtn && newFollowUpText) {
                newFollowUpBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('New conversation follow-up button clicked!');
                    
                    handleUniversalFollowUp(newFollowUpBtn, newEntry.input, newEntry.response);
                });
            }
            
            // Insert the new entry at the top of the conversation history
            const firstEntry = conversationHistory.querySelector('.conversation-entry');
            if (firstEntry) {
                conversationHistory.insertBefore(newEntryElement, firstEntry);
            } else {
                conversationHistory.appendChild(newEntryElement);
            }
        }

        // Clear the original follow-up input
        followUpText.value = '';
        showToast('Conversation continued successfully!');

    } catch (error) {
        console.error('Error in follow-up:', error);
        showToast('Error continuing conversation: ' + error.message);
    } finally {
        // Re-enable the input and button
        followUpText.disabled = false;
        button.disabled = false;
        button.textContent = 'Continue Conversation';
    }
}

// Handle follow-up for past conversations
async function handlePastConversationFollowUp(button, originalInput, originalOutput) {
    const followUpText = button.parentElement.querySelector('.follow-up-text');
    if (!followUpText) {
        console.error('Follow-up text area not found');
        alert('Follow-up text area not found. Please refresh the page.');
        return;
    }
    
    const followUpInput = followUpText.value.trim();
    
    if (!followUpInput) {
        alert('Please enter your follow-up message');
        return;
    }

    // Disable the input and button
    followUpText.disabled = true;
    button.disabled = true;
    button.textContent = '🔄 Continuing conversation...';

    try {
        const selectedUnitId = getCurrentUnit();
        if (!selectedUnitId) {
            alert('Please select a consciousness unit');
            return;
        }

        // Create context with conversation history
        const contextualInput = `Previous conversation:
Input: ${originalInput}
Output: ${originalOutput}

Follow-up: ${followUpInput}`;

        const response = await fetch(`/api/units/${selectedUnitId}/process`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                input: contextualInput,
                parameters: getCurrentParameters()
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Follow-up API response:', data);

        // Extract response content
        let responseContent = data.response || 'No response received from the API';

        // Create new conversation entry for the follow-up
        const newEntry = {
            timestamp: new Date().toISOString(),
            input: followUpInput,
            response: responseContent,
            consciousness_state: data.state || {}
        };

        // Add the new entry to the conversation history
        const outputContent = document.getElementById('processingResult');
        const conversationHistory = outputContent.querySelector('.conversation-history');
        
        if (conversationHistory) {
            // Create HTML for the new conversation entry
            const datetime = new Date(newEntry.timestamp).toLocaleString();
            const consciousnessIndex = ((newEntry.consciousness_state?.consciousness_index || 0) * 100).toFixed(1);
            
            // Create new conversation entry element
            const newEntryElement = document.createElement('div');
            newEntryElement.className = 'conversation-entry';
            
            newEntryElement.innerHTML = `
                <div class="conv-header">
                    <span class="conv-time">${datetime}</span>
                    <span class="conv-unit">Unit: ${newEntry.consciousness_state?.unit_id || 'unknown'}</span>
                    <span class="conv-consciousness">CI: ${consciousnessIndex}%</span>
                </div>
                <div class="conv-input">
                    <strong>Follow-up:</strong> ${newEntry.input}
                </div>
                <div class="conv-output">
                    <strong>Output:</strong> ${formatResponseText(newEntry.response)}
                    <div class="follow-up-section">
                        <textarea class="follow-up-text" placeholder="Continue the conversation..."></textarea>
                        <button class="follow-up-btn">Continue Conversation</button>
                    </div>
                </div>
            `;
            
            // Add event listener to the new follow-up button
            const newFollowUpBtn = newEntryElement.querySelector('.follow-up-btn');
            const newFollowUpText = newEntryElement.querySelector('.follow-up-text');
            
            if (newFollowUpBtn && newFollowUpText) {
                newFollowUpBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('New past conversation follow-up button clicked!');
                    
                    handlePastConversationFollowUp(newFollowUpBtn, newEntry.input, newEntry.response);
                });
            }
            
            // Insert the new entry at the top of the conversation history
            const firstEntry = conversationHistory.querySelector('.conversation-entry');
            if (firstEntry) {
                conversationHistory.insertBefore(newEntryElement, firstEntry);
            } else {
                conversationHistory.appendChild(newEntryElement);
            }
        }

        // Clear the original follow-up input
        followUpText.value = '';
        showToast('Conversation continued successfully!');

    } catch (error) {
        console.error('Error in follow-up:', error);
        showToast('Error continuing conversation: ' + error.message);
    } finally {
        // Re-enable the input and button
        followUpText.disabled = false;
        button.disabled = false;
        button.textContent = 'Continue Conversation';
    }
}

// Export functions to global scope for HTML onclick handlers
window.toggleResponseParameters = toggleResponseParameters;
window.loadSessionConversations = loadSessionConversations;
window.deleteSession = deleteSession;
window.handlePastConversationFollowUp = handlePastConversationFollowUp;
window.handleUniversalFollowUp = handleUniversalFollowUp;

// Parameter info popover: descriptions for each parameter (shown when "i" is clicked)
const PARAM_DESCRIPTIONS = {
    temperature: 'Controls randomness. Lower (e.g. 0.5) = more deterministic; higher (e.g. 1.0) = more varied. Optimal: 0.7 for balanced responses.',
    topP: 'Nucleus sampling: only tokens whose cumulative probability is within this fraction are considered. 0.9 keeps diverse but likely tokens.',
    maxTokens: 'Maximum length of the model reply in tokens. Higher allows longer answers; 8192 is a good default for detailed responses.',
    presencePenalty: 'Nudges the model to mention new topics. Too high (>1) can make output unnatural. Optimal: 0.4.',
    frequencyPenalty: 'Reduces repetition of the same words or phrases. 0.2–0.4 is usually enough.',
    phiScore: 'Consciousness integration level. Higher = more nuanced, layered, and self-reflective answers. Optimal: 0.8.',
    recursiveDepth: 'Depth of reasoning (1–10). Higher = more layers of analysis and meta-thinking. 5–7 for deep but controlled.',
    selfModelCoherence: 'How consistent and self-aware the model’s perspective is. High values (0.9+) support clear self-reflection.',
    temporalBinding: 'How coherent the flow of ideas is over the reply. High = smooth development and clear progression.',
    noveltyGeneration: 'How much the model favors creative or unconventional angles. 0.75 balances novelty with coherence.',
    witnessingScore: 'Degree of self-observation and meta-cognitive tone in the response. High = explicit reflection on its own reasoning.',
    predictionAccuracy: 'How much the model tends to make predictions or forecasts. 0.5 = moderate; increase for more forward-looking answers.',
    attentionFocus: 'How much the model stays on topic vs. explores tangents. 0.65 = focused but allows relevant side points.',
    memoryIntegration: 'How strongly the model uses context and prior turns. Higher = more reference to earlier conversation.'
};

function showParamInfo(paramId, buttonElement) {
    const popover = document.getElementById('paramInfoPopover');
    const titleEl = document.getElementById('paramInfoPopoverTitle');
    const bodyEl = document.getElementById('paramInfoPopoverBody');
    if (!popover || !titleEl || !bodyEl) return;
    const desc = PARAM_DESCRIPTIONS[paramId];
    if (!desc) return;
    const isAlreadyOpen = !popover.classList.contains('hidden') && popover.dataset.currentParam === paramId;
    if (isAlreadyOpen) {
        popover.classList.add('hidden');
        popover.dataset.currentParam = '';
        return;
    }
    const rect = buttonElement.getBoundingClientRect();
    titleEl.textContent = paramId.replace(/([A-Z])/g, ' $1').replace(/^./, s => s.toUpperCase()).trim();
    bodyEl.textContent = desc;
    popover.dataset.currentParam = paramId;
    popover.style.left = Math.min(rect.left, window.innerWidth - 300) + 'px';
    popover.style.top = (rect.bottom + 6) + 'px';
    popover.classList.remove('hidden');
}

function hideParamInfo() {
    const popover = document.getElementById('paramInfoPopover');
    if (popover) {
        popover.classList.add('hidden');
        popover.dataset.currentParam = '';
    }
}

// Simple test function
function testButton() {
    console.log('Test button clicked!');
    
    // Test follow-up button functionality
    const testFollowUpBtn = document.createElement('button');
    testFollowUpBtn.className = 'follow-up-btn';
    testFollowUpBtn.textContent = '🧪 Test Follow-up Button';
    testFollowUpBtn.addEventListener('click', function() {
        console.log('Test follow-up button clicked!');
        showToast('Follow-up button test successful!');
    });
    
    // Add to the page temporarily
    const processingResult = document.getElementById('processingResult');
    if (processingResult) {
        processingResult.appendChild(testFollowUpBtn);
        setTimeout(() => {
            if (testFollowUpBtn.parentNode) {
                testFollowUpBtn.parentNode.removeChild(testFollowUpBtn);
            }
        }, 5000);
    }
    
    showToast('Test button working! Follow-up test added.');
}

// Make test function available globally
window.testButton = testButton;

// Handle follow-up for current conversation entries
async function handleCurrentFollowUp(followUpInput, parentEntry, followUpBtn, followUpText) {
    try {
        const selectedUnitId = getCurrentUnit();
        if (!selectedUnitId) {
            alert('Please select a consciousness unit');
            return;
        }

        // Create context with conversation history
        const contextualInput = `Previous conversation:
Input: ${parentEntry.input}
Output: ${parentEntry.response}

Follow-up: ${followUpInput}`;

        const response = await fetch(`/api/units/${selectedUnitId}/process`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                input: contextualInput,
                parameters: getCurrentParameters()
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Follow-up API response:', data);

        // Extract response content from various possible locations
        let responseContent = null;
        
        if (data.choices && Array.isArray(data.choices) && data.choices[0]?.message?.content) {
            responseContent = data.choices[0].message.content;
        } else if (data.response) {
            responseContent = data.response;
        } else if (data.consciousness_result) {
            responseContent = data.consciousness_result;
        }

        // Clean up the response content
        if (responseContent && typeof responseContent === 'string') {
            responseContent = responseContent.replace(/^\[[^\]]+\]\s*/, '').trim();
        } else {
            responseContent = 'No response received from the API';
        }

        // Create history entry for the follow-up
        const followUpEntry = {
            timestamp: new Date().toISOString(),
            input: followUpInput,
            response: responseContent,
            consciousness_state: data.state || currentState
        };

        // Create a new follow-up entry at the top of the conversation
        const processingResult = document.getElementById('processingResult');
        const newEntryElement = document.createElement('div');
        newEntryElement.className = 'output-entry';
        
        const timestamp = new Date(followUpEntry.timestamp).toLocaleString();
        const state = followUpEntry.consciousness_state;
        const metrics = state.metrics || {};
        
        newEntryElement.innerHTML = `
            <div class="entry-header">
                <span class="timestamp">${timestamp}</span>
                <span class="state-badge">${state.state || 'conscious'}</span>
            </div>
            <div class="entry-content">
                <div class="input-section">
                    <strong>Follow-up:</strong>
                    <p>${followUpEntry.input}</p>
                </div>
                <div class="response-section">
                    <strong>Response:</strong>
                    <div class="response-text">${formatResponseText(followUpEntry.response)}</div>
                </div>
                <div class="follow-up-section">
                    <textarea class="follow-up-text" placeholder="Continue the conversation..."></textarea>
                    <button class="follow-up-btn">Continue Conversation</button>
                </div>
            </div>
            <div class="entry-metrics">
                <div class="metric">
                    <span class="metric-label">Consciousness Index:</span>
                    <span class="metric-value">${((state.consciousness_index || 0) * 100).toFixed(1)}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Phi Score:</span>
                    <span class="metric-value">${((metrics.phi_score || 0) * 100).toFixed(1)}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Recursive Depth:</span>
                    <span class="metric-value">${metrics.recursive_depth || 0}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Self-Model Coherence:</span>
                    <span class="metric-value">${((metrics.self_model_coherence || 0) * 100).toFixed(1)}%</span>
                </div>
            </div>
        `;
        
        // Add event handler to the new follow-up button immediately
        const newFollowUpBtn = newEntryElement.querySelector('.follow-up-btn');
        const newFollowUpText = newEntryElement.querySelector('.follow-up-text');
        
        if (newFollowUpBtn && newFollowUpText) {
            console.log('Adding click handler to new follow-up button');
            
            newFollowUpBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('New follow-up button clicked!');
                
                const newFollowUpInput = newFollowUpText.value.trim();
                if (!newFollowUpInput) {
                    alert('Please continue the conversation with your input');
                    return;
                }

                newFollowUpText.disabled = true;
                newFollowUpBtn.disabled = true;
                newFollowUpBtn.textContent = '🔄 Continuing conversation...';

                handleCurrentFollowUp(newFollowUpInput, followUpEntry, newFollowUpBtn, newFollowUpText);
            });
        }
        
        // Insert the new entry at the top
        processingResult.insertBefore(newEntryElement, processingResult.firstChild);

        // Clear the original follow-up input and re-enable
        followUpText.value = '';
        showToast('Conversation continued successfully!');

    } catch (error) {
        console.error('Error in follow-up:', error);
        showToast('Error continuing conversation: ' + error.message);
    } finally {
        // Re-enable the input and button
        followUpText.disabled = false;
        followUpBtn.disabled = false;
        followUpBtn.textContent = 'Continue Conversation';
    }
}