# CPU Scheduling Simulator (Python + Tkinter)

A graphical CPU Scheduling Simulator built using **Python** and **Tkinter**.  
It visually demonstrates how major CPU scheduling algorithms work, displays  
Gantt charts, and calculates important performance metrics like **Waiting Time**  
and **Turnaround Time**.

---

## 🚀 Features

### ✅ Supported Algorithms
- **FCFS** (First Come First Serve)  
- **SJF (Non-Preemptive)**  
- **SRTF (Preemptive SJF)**  
- **Round Robin** (Custom Time Quantum)  
- **Priority Scheduling (Non-Preemptive)**  

### ✅ What this Simulator Provides
- Add multiple processes (Arrival, Burst, Priority)  
- Visual **Gantt Chart**  
- Per-process Wait & Turnaround times  
- Average Waiting & TAT values  
- Export results as **.txt file**  
- Clean Tkinter GUI  

---

## 🖥️ GUI Preview (Example)

| Add Process: Arrival | Burst | Priority |
| Process Table (PID, Arrival, Burst, Priority)|
| Select Algorithm → Run → View Results |
| Text Output + Gantt Chart Visualization |


---

## 🔧 Installation

### 1. Install Python (3.8+ recommended)
Download from: https://www.python.org/downloads/  
✔️ Make sure to check **Add Python to PATH** during install.

### 2. Install Tkinter (if missing)

**Windows/macOS:** Tkinter comes pre-installed.  
If needed:
```bash
pip install tk
cd cpu_scheduler
python cpu_scheduler.py
