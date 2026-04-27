# utils/explainer.py

import numpy as np


def explain_cpu(processes):
    """
    Explains why a CPU scheduling algorithm is suitable
    based on burst time variation.
    """

    bursts = [p.burst for p in processes]
    std = float(np.std(bursts))

    if std > 3:
        return "High burst time variation → Preemptive scheduling (SRTF/Priority) performs better."
    else:
        return "Low burst variation → FCFS or simple scheduling performs efficiently."


def explain_memory(fifo_faults, lru_faults, opt_faults):
    """
    Explains which page replacement algorithm performed best.
    """

    best = min(fifo_faults, lru_faults, opt_faults)

    if best == opt_faults:
        return "Optimal performs best because it replaces pages based on future knowledge."
    elif best == lru_faults:
        return "LRU performs well due to temporal locality (recent pages reused)."
    else:
        return "FIFO is simple but may lead to more page faults (no usage awareness)."