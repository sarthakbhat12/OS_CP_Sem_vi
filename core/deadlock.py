# core/deadlock.py

from typing import List, Dict


def is_safe_detailed(allocation: List[List[int]],
                     max_need: List[List[int]],
                     available: List[int]) -> Dict:

    n = len(allocation)
    m = len(available)

    need = [
        [max_need[i][j] - allocation[i][j] for j in range(m)]
        for i in range(n)
    ]

    finish = [False] * n
    safe_seq = []
    work = available.copy()
    
    steps = []
    step_num = 1

    while len(safe_seq) < n:
        found = False

        for i in range(n):
            if not finish[i]:
                can_allocate = all(need[i][j] <= work[j] for j in range(m))
                
                step_info = {
                    "step": step_num,
                    "process": i,
                    "need": need[i],
                    "work_before": work.copy(),
                    "can_allocate": can_allocate
                }

                if can_allocate:
                    for j in range(m):
                        work[j] += allocation[i][j]
                    
                    step_info["work_after"] = work.copy()
                    
                    safe_seq.append(i)
                    finish[i] = True
                    found = True
                    steps.append(step_info)
                    step_num += 1
                else:
                    steps.append(step_info)

        if not found:
            remaining = [i for i in range(n) if not finish[i]]
            return {
                "safe": False,
                "sequence": safe_seq,
                "steps": steps,
                "deadlock_processes": remaining,
                "suggestion": f"Terminate P{remaining[0]} to release resources." if remaining else "",
                "need_matrix": need
            }

    return {
        "safe": True,
        "sequence": safe_seq,
        "steps": steps,
        "deadlock_processes": [],
        "suggestion": "",
        "need_matrix": need
    }