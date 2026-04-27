# system/features.py

import numpy as np


def extract_features(processes):
    """
    Extracts workload features for ML or analysis
    """

    bursts = [p.burst for p in processes]
    arrivals = [p.arrival for p in processes]

    features = {
        "num_processes": len(processes),
        "avg_burst": float(np.mean(bursts)),
        "std_burst": float(np.std(bursts)),
        "max_burst": max(bursts),
        "arrival_spread": max(arrivals) - min(arrivals)
    }

    return features