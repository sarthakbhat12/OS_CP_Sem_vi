// app.js

const API_BASE = 'http://localhost:5000/api';

// Global state
let cpuProcesses = [];
let memPages = [];
let diskRequests = [];
let diskHead = 50;

let currentCpuChart = null;
let currentMemChart = null;
let currentDiskChart = null;

let memResults = {};

document.addEventListener('DOMContentLoaded', () => {
    // Navigation
    const navLinks = document.querySelectorAll('.nav-links li');
    const sections = document.querySelectorAll('.view-section');
    const pageTitle = document.getElementById('page-title');

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            const targetView = link.getAttribute('data-view');
            pageTitle.textContent = link.textContent.trim();
            
            sections.forEach(sec => {
                if(sec.id === targetView) sec.classList.remove('hidden');
                else sec.classList.add('hidden');
            });

            if (targetView === 'ml') fetchMLMetrics();
        });
    });

    // --- CPU Logic ---
    document.getElementById('generate-cpu-btn').addEventListener('click', () => {
        const n = Math.floor(Math.random() * 4) + 4; // 4 to 7
        cpuProcesses = [];
        const tbody = document.getElementById('cpu-tbody');
        tbody.innerHTML = '';

        for (let i = 0; i < n; i++) {
            const p = {
                pid: i,
                arrival: Math.floor(Math.random() * 6),
                burst: Math.floor(Math.random() * 10) + 1,
                priority: Math.floor(Math.random() * 5) + 1
            };
            cpuProcesses.push(p);
            tbody.innerHTML += `<tr>
                <td>P${p.pid}</td>
                <td>${p.arrival}</td>
                <td>${p.burst}</td>
                <td>${p.priority}</td>
            </tr>`;
        }
    });

    document.getElementById('run-cpu-btn').addEventListener('click', async () => {
        if (cpuProcesses.length === 0) return alert('Generate workload first!');
        
        try {
            const res = await fetch(`${API_BASE}/cpu`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ processes: cpuProcesses })
            });
            const data = await res.json();
            
            renderCpuChart(data.results);
            renderGanttCharts(data.results);
            
            const mlBox = document.getElementById('cpu-ml-insight');
            mlBox.classList.remove('hidden');
            document.getElementById('cpu-ml-text').innerHTML = `The ML model predicts that <strong>${data.ml_prediction}</strong> is the optimal scheduling algorithm for this specific workload.`;
            
        } catch (err) {
            console.error(err);
        }
    });

    // --- Memory Logic ---
    document.getElementById('generate-mem-btn').addEventListener('click', () => {
        memPages = Array.from({length: 15}, () => Math.floor(Math.random() * 6));
        const refDiv = document.getElementById('mem-ref-string');
        refDiv.innerHTML = memPages.map(p => `<div class="page-box">${p}</div>`).join('');
    });

    document.getElementById('run-mem-btn').addEventListener('click', async () => {
        if (memPages.length === 0) return alert('Generate reference string first!');
        const frames = parseInt(document.getElementById('mem-frames').value) || 3;
        
        try {
            const res = await fetch(`${API_BASE}/memory`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pages: memPages, frames: frames })
            });
            const data = await res.json();
            memResults = data;
            
            renderMemChart([data.fifo.faults, data.lru.faults, data.optimal.faults]);
            renderMemSteps('fifo'); // default tab
            
        } catch (err) {
            console.error(err);
        }
    });

    const memTabs = document.querySelectorAll('#memory .tab-btn');
    memTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            memTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            const target = tab.getAttribute('data-target').replace('mem-', '').replace('-steps', '');
            renderMemSteps(target);
        });
    });

    // --- Disk Logic ---
    document.getElementById('generate-disk-btn').addEventListener('click', () => {
        diskRequests = Array.from({length: 8}, () => Math.floor(Math.random() * 200));
        diskHead = parseInt(document.getElementById('disk-head').value) || 50;
        
        const refDiv = document.getElementById('disk-requests-string');
        refDiv.innerHTML = diskRequests.map(r => `<div class="page-box">${r}</div>`).join('');
    });

    document.getElementById('run-disk-btn').addEventListener('click', async () => {
        if (diskRequests.length === 0) return alert('Generate requests first!');
        diskHead = parseInt(document.getElementById('disk-head').value) || 50;
        
        try {
            const res = await fetch(`${API_BASE}/disk`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ requests: diskRequests, head: diskHead })
            });
            const data = await res.json();
            
            renderDiskChart([data.fcfs.seek_time, data.sstf.seek_time]);
            
            const seqDiv = document.getElementById('disk-sequence');
            seqDiv.innerHTML = `
                <div style="margin-bottom:10px;"><strong>FCFS:</strong> ${data.fcfs.sequence.join(' &rarr; ')}</div>
                <div><strong>SSTF:</strong> ${data.sstf.sequence.join(' &rarr; ')}</div>
            `;
            
        } catch (err) {
            console.error(err);
        }
    });

    // --- Deadlock Logic ---
    let deadlockPayload = null;
    document.getElementById('generate-deadlock-btn').addEventListener('click', () => {
        deadlockPayload = {
            allocation: [[0,1,0], [2,0,0], [3,0,2], [2,1,1], [0,0,2]],
            max_need: [[7,5,3], [3,2,2], [9,0,2], [2,2,2], [4,3,3]],
            available: [3,3,2]
        };
        
        document.getElementById('deadlock-matrices').textContent = JSON.stringify(deadlockPayload, null, 2);
    });

    document.getElementById('run-deadlock-btn').addEventListener('click', async () => {
        if (!deadlockPayload) return alert('Load matrices first!');
        
        try {
            const res = await fetch(`${API_BASE}/deadlock`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(deadlockPayload)
            });
            const data = await res.json();
            
            const resultBox = document.getElementById('deadlock-result');
            if (data.safe) {
                resultBox.className = 'result-box result-safe';
                resultBox.innerHTML = `System is SAFE ✅<br>Sequence: ${data.sequence.map(i=>'P'+i).join(' &rarr; ')}`;
            } else {
                resultBox.className = 'result-box result-unsafe';
                resultBox.innerHTML = `System is UNSAFE ❌<br>Deadlock detected.<br><small>${data.suggestion}</small>`;
            }

            const stepsCard = document.getElementById('deadlock-steps-card');
            stepsCard.classList.remove('hidden');
            const stepsDiv = document.getElementById('deadlock-steps');
            stepsDiv.innerHTML = '';
            
            data.steps.forEach(s => {
                const stepEl = document.createElement('div');
                stepEl.style.padding = '10px';
                stepEl.style.borderBottom = '1px solid rgba(255,255,255,0.1)';
                stepEl.innerHTML = `
                    <strong>Step ${s.step}:</strong> Checking P${s.process}... 
                    Need = [${s.need}], Available = [${s.work_before}].
                    ${s.can_allocate ? `<span style="color:var(--success)">Can Allocate. New Available = [${s.work_after}]</span>` : `<span style="color:var(--danger)">Cannot Allocate.</span>`}
                `;
                stepsDiv.appendChild(stepEl);
            });
            
        } catch (err) {
            console.error(err);
        }
    });
});

// --- Helper Functions ---

function renderCpuChart(results) {
    const ctx = document.getElementById('cpu-chart').getContext('2d');
    if(currentCpuChart) currentCpuChart.destroy();
    
    currentCpuChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: results.map(r => r.name),
            datasets: [{
                label: 'Avg Waiting Time',
                data: results.map(r => r.avg_wt),
                backgroundColor: 'rgba(59, 130, 246, 0.7)',
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 1
            }, {
                label: 'Avg Turnaround Time',
                data: results.map(r => r.avg_tat),
                backgroundColor: 'rgba(139, 92, 246, 0.7)',
                borderColor: 'rgba(139, 92, 246, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true, grid: {color: 'rgba(255,255,255,0.1)'}, ticks: {color: '#94a3b8'} }, x: { grid: {display: false}, ticks: {color: '#94a3b8'} } },
            plugins: { legend: { labels: {color: '#f8fafc'} } }
        }
    });
}

function renderGanttCharts(results) {
    const container = document.getElementById('gantt-charts');
    container.innerHTML = '<h3>Gantt Charts</h3>';
    
    results.forEach(res => {
        let maxTime = res.gantt.length > 0 ? res.gantt[res.gantt.length-1][2] : 1;
        
        let html = `<div class="gantt-chart-wrapper">
            <h4>${res.name}</h4>
            <div class="gantt-chart">`;
            
        res.gantt.forEach(block => {
            const name = block[0];
            const start = block[1];
            const end = block[2];
            const duration = end - start;
            const widthPct = (duration / maxTime) * 100;
            
            let colorClass = name === 'Idle' ? 'gantt-idle' : `gantt-${name.toLowerCase()}`;
            
            html += `<div class="gantt-block ${colorClass}" style="width: ${widthPct}%" title="Start: ${start}, End: ${end}">
                ${name} <br> ${duration}
            </div>`;
        });
        
        html += `</div></div>`;
        container.innerHTML += html;
    });
}

function renderMemChart(data) {
    const ctx = document.getElementById('mem-chart').getContext('2d');
    if(currentMemChart) currentMemChart.destroy();
    
    currentMemChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['FIFO', 'LRU', 'Optimal'],
            datasets: [{
                label: 'Page Faults',
                data: data,
                backgroundColor: ['rgba(239, 68, 68, 0.7)', 'rgba(245, 158, 11, 0.7)', 'rgba(16, 185, 129, 0.7)'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true, grid: {color: 'rgba(255,255,255,0.1)'}, ticks: {color: '#94a3b8'} }, x: { grid: {display: false}, ticks: {color: '#94a3b8'} } },
            plugins: { legend: { display: false } }
        }
    });
}

function renderMemSteps(algo) {
    if (!memResults[algo]) return;
    const tbody = document.getElementById('mem-steps-tbody');
    tbody.innerHTML = '';
    
    memResults[algo].steps.forEach((step, idx) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${idx + 1}</td>
            <td>${step.page}</td>
            <td style="color: ${step.action === 'HIT' ? 'var(--success)' : 'var(--danger)'}"><b>${step.action}</b></td>
            <td>[ ${step.memory.join(', ')} ]</td>
        `;
        tbody.appendChild(row);
    });
}

function renderDiskChart(data) {
    const ctx = document.getElementById('disk-chart').getContext('2d');
    if(currentDiskChart) currentDiskChart.destroy();
    
    currentDiskChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['FCFS', 'SSTF'],
            datasets: [{
                label: 'Total Seek Time',
                data: data,
                backgroundColor: ['rgba(139, 92, 246, 0.7)', 'rgba(59, 130, 246, 0.7)'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true, grid: {color: 'rgba(255,255,255,0.1)'}, ticks: {color: '#94a3b8'} }, x: { grid: {display: false}, ticks: {color: '#94a3b8'} } },
            plugins: { legend: { display: false } }
        }
    });
}

async function fetchMLMetrics() {
    try {
        const res = await fetch(`${API_BASE}/ml/metrics`);
        const data = await res.json();
        
        if (data.decision_tree_accuracy) {
            document.getElementById('ml-dt-acc').textContent = (data.decision_tree_accuracy * 100).toFixed(1) + '%';
            document.getElementById('ml-rf-acc').textContent = (data.random_forest_accuracy * 100).toFixed(1) + '%';
            document.getElementById('ml-selected-model').textContent = data.selected_model;
            document.getElementById('ml-report').textContent = JSON.stringify(data.report, null, 2);
        }
    } catch (err) {
        console.error(err);
    }
}
