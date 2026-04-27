# core/memory.py

from typing import List, Dict


def fifo(pages: List[int], frames: int) -> Dict:
    memory = []
    faults = 0
    hits = 0
    steps = []

    for p in pages:
        action = "HIT"
        if p not in memory:
            faults += 1
            action = "FAULT"
            if len(memory) < frames:
                memory.append(p)
            else:
                memory.pop(0)
                memory.append(p)
        else:
            hits += 1
            
        steps.append({
            "page": p,
            "action": action,
            "memory": memory.copy()
        })

    return {"name": "FIFO", "faults": faults, "hits": hits, "steps": steps}


def lru(pages: List[int], frames: int) -> Dict:
    memory = []
    faults = 0
    hits = 0
    steps = []

    for p in pages:
        action = "HIT"
        if p not in memory:
            faults += 1
            action = "FAULT"
            if len(memory) < frames:
                memory.append(p)
            else:
                memory.pop(0)
                memory.append(p)
        else:
            hits += 1
            memory.remove(p)
            memory.append(p)
            
        steps.append({
            "page": p,
            "action": action,
            "memory": memory.copy()
        })

    return {"name": "LRU", "faults": faults, "hits": hits, "steps": steps}


def optimal(pages: List[int], frames: int) -> Dict:
    memory = []
    faults = 0
    hits = 0
    steps = []

    for i in range(len(pages)):
        p = pages[i]
        action = "HIT"
        
        if p not in memory:
            faults += 1
            action = "FAULT"
            if len(memory) < frames:
                memory.append(p)
            else:
                future = pages[i + 1:]
                idx = -1
                farthest = -1

                for j in range(len(memory)):
                    if memory[j] not in future:
                        idx = j
                        break
                    else:
                        pos = future.index(memory[j])
                        if pos > farthest:
                            farthest = pos
                            idx = j

                memory[idx] = p
        else:
            hits += 1
            
        steps.append({
            "page": p,
            "action": action,
            "memory": memory.copy()
        })

    return {"name": "Optimal", "faults": faults, "hits": hits, "steps": steps}