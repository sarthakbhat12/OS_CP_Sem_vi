# AI-Based Operating System Resource Management Simulator

This is an advanced, production-grade OS simulation platform designed to visualize and compare core Operating System algorithms alongside Machine Learning predictions. 

## 🌟 Features
- **CPU Scheduling**: Simulates FCFS, SRTF, Round Robin, and Priority (Preemptive). Computes Waiting Time, Turnaround Time, and Response Time with fully interactive Gantt charts.
- **Memory Management**: Step-by-step interactive simulation for FIFO, LRU, and Optimal page replacement algorithms, calculating exact fault rates.
- **Disk Scheduling**: Visualizes head movement sequence for FCFS and SSTF.
- **Deadlock Detection**: Implements Banker's Algorithm with detailed, step-by-step verification of safe/unsafe states and recovery suggestions.
- **Machine Learning Integration**: Uses `scikit-learn` (Decision Tree & Random Forest) to predict the best CPU scheduling algorithm for a given workload.

## 🚀 Getting Started

### Prerequisites
Make sure you have Python 3.9+ installed.

```bash
pip install -r requirements.txt
```

### Running the App
The application has been upgraded from a basic CLI to a full **Web Application** featuring a stunning glassmorphic UI.

1. Start the Flask Backend Server:
```bash
python app.py
```
*(Note: It may take a few seconds to boot up initially as the Machine Learning models train on synthetic datasets)*

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## 🧠 Architecture
- **Backend**: Flask API (`app.py`) providing endpoints for OS resource algorithms and ML inference.
- **Core Algorithms**: Located in `core/` containing the exact mathematical models for CPU, Memory, Disk, and Deadlocks.
- **Frontend**: A custom Vanilla JS frontend (`static/` folder) with dynamic Chart.js graphing and DOM manipulation.

---
*Created as a final-year University Project.*
