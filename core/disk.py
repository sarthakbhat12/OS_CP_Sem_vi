# core/disk.py

from typing import List, Dict


def fcfs(requests: List[int], head: int) -> Dict:
    """
    FCFS Disk Scheduling
    Returns dict with seek time and sequence
    """
    seek = 0
    sequence = [head]

    for r in requests:
        seek += abs(head - r)
        head = r
        sequence.append(head)

    return {"name": "FCFS", "seek_time": seek, "sequence": sequence}


def sstf(requests: List[int], head: int) -> Dict:
    """
    SSTF Disk Scheduling
    Returns dict with seek time and sequence
    """
    seek = 0
    req = requests.copy()
    sequence = [head]

    while req:
        # find closest request
        closest = min(req, key=lambda x: abs(x - head))
        seek += abs(head - closest)
        head = closest
        sequence.append(head)
        req.remove(closest)

    return {"name": "SSTF", "seek_time": seek, "sequence": sequence}