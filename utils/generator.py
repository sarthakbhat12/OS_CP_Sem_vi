# utils/generator.py

import random
from core.cpu import Process


def generate_cpu(n=5):
    """
    Generates random CPU processes
    """
    processes = []

    for i in range(n):
        processes.append(
            Process(
                pid=i,
                arrival=random.randint(0, 5),
                burst=random.randint(1, 10),
                priority=random.randint(1, 5)
            )
        )

    return processes


def generate_memory():
    """
    Generates page reference string and frame count
    """
    pages = [random.randint(0, 5) for _ in range(20)]
    frames = 3
    return pages, frames


def generate_disk():
    """
    Generates disk requests and initial head position
    """
    requests = [random.randint(0, 199) for _ in range(10)]
    head = random.randint(0, 199)
    return requests, head


def generate_deadlock():
    """
    Returns sample allocation, max_need, and available matrices
    (Banker's Algorithm example)
    """

    allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2]
    ]

    max_need = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2]
    ]

    available = [3, 3, 2]

    return allocation, max_need, available