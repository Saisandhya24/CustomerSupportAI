document.addEventListener('DOMContentLoaded', () => {
    // Navigation Tab Switching
    const navButtons = document.querySelectorAll('.nav-btn');
    const tabPages = document.querySelectorAll('.tab-page');

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');

            navButtons.forEach(b => b.classList.remove('active'));
            tabPages.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
});

function fillQuery(text) {
    document.getElementById('tweet-input').value = text;
}

async function processTweet() {
    const inputArea = document.getElementById('tweet-input');
    const queryText = inputArea.value.trim();

    if (!queryText) {
        alert('Please enter a customer tweet to process.');
        return;
    }

    const emptyState = document.getElementById('output-empty');
    const loaderState = document.getElementById('output-loader');
    const resultContent = document.getElementById('output-content');

    emptyState.classList.add('hidden');
    resultContent.classList.add('hidden');
    loaderState.classList.remove('hidden');

    try {
        const response = await fetch('/api/process', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: queryText })
        });

        const data = await response.json();

        if (response.ok) {
            renderOutput(data);
        } else {
            alert('Error: ' + (data.error || 'Failed to process tweet'));
        }
    } catch (err) {
        alert('Network error communicating with AI Agent API server.');
    } finally {
        loaderState.classList.add('hidden');
    }
}

function renderOutput(data) {
    const resultContent = document.getElementById('output-content');
    
    // Intent
    document.getElementById('intent-badge').textContent = data.predicted_intent;
    const confVal = data.intent_confidence || 0.85;
    document.getElementById('intent-conf').textContent = (confVal * 100).toFixed(1) + '%';
    document.getElementById('conf-fill').style.width = (confVal * 100) + '%';

    // Action & Reason
    const actionBadge = document.getElementById('action-badge');
    actionBadge.textContent = data.action;
    actionBadge.className = 'action-pill ' + data.action;
    document.getElementById('escalation-reason').textContent = data.escalation_reason;

    // RAG Context
    const ragList = document.getElementById('rag-context-list');
    ragList.innerHTML = '';
    if (data.retrieved_context && data.retrieved_context.length > 0) {
        data.retrieved_context.forEach(ctx => {
            const div = document.createElement('div');
            div.className = 'rag-item';
            div.style.padding = '0.5rem 0';
            div.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
            div.innerHTML = `<p style="font-size:0.8rem; color:#9ca3af;">[Sim Score: ${ctx.similarity_score}] <strong>${ctx.resolution_category}:</strong> ${ctx.brand_resolution}</p>`;
            ragList.appendChild(div);
        });
    } else {
        ragList.innerHTML = '<p style="font-size:0.8rem; color:#9ca3af;">No direct historical RAG context retrieved.</p>';
    }

    // Draft Reply
    document.getElementById('draft-reply-text').textContent = data.draft_reply;

    resultContent.classList.remove('hidden');
}
