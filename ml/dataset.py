# ml/dataset.py

import random
import numpy as np
from core.cpu import CPUScheduler, Process


def generate_dataset(samples=1000):
    scheduler = CPUScheduler()

    X = []
    y = []

    for _ in range(samples):
        n = random.randint(4, 10)
        
        scenario = random.choice(["random", "srtf_favored", "rr_favored", "fcfs_favored", "priority_favored"])
        
        processes = []
        for i in range(n):
            if scenario == "srtf_favored":
                # High variance in burst times, some very small
                burst = random.choice([1, 2, random.randint(10, 20)])
                arrival = random.randint(0, 5)
                priority = random.randint(1, 5)
            elif scenario == "rr_favored":
                # Similar large burst times
                burst = random.randint(10, 15)
                arrival = 0
                priority = random.randint(1, 5)
            elif scenario == "fcfs_favored":
                # Increasing burst times with early arrivals
                burst = i * 2 + random.randint(1, 3)
                arrival = i
                priority = random.randint(1, 5)
            elif scenario == "priority_favored":
                burst = random.randint(5, 15)
                arrival = random.randint(0, 10)
                # Ensure high priority (small number) for long bursts to favor priority
                priority = 1 if burst > 10 else random.randint(3, 5)
            else:
                burst = random.randint(1, 15)
                arrival = random.randint(0, 10)
                priority = random.randint(1, 5)
                
            processes.append(Process(pid=i, arrival=arrival, burst=burst, priority=priority))

        bursts = [p.burst for p in processes]
        arrivals = [p.arrival for p in processes]

        features = [
            n,
            float(np.mean(bursts)),
            float(np.std(bursts)),
            max(bursts),
            min(bursts),
            max(arrivals) - min(arrivals),
            sum(bursts),
            len([b for b in bursts if b > np.mean(bursts)])
        ]

        results = scheduler.run_all(processes)
        best = min(results, key=lambda x: x["avg_wt"])["name"]

        X.append(features)
        y.append(best)

    return X, y