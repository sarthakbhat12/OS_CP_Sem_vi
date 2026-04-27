# core/cpu.py

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Process:
    pid: int
    arrival: int
    burst: int
    priority: int = 0


class CPUScheduler:

    def fcfs(self, processes: List[Process]) -> Dict:
        procs = sorted(processes, key=lambda x: x.arrival)
        
        time = 0
        gantt = []
        waiting_times = {}
        turnaround_times = {}
        response_times = {}
        first_run = {}

        for p in procs:
            if time < p.arrival:
                gantt.append(("Idle", time, p.arrival))
                time = p.arrival
            
            start_time = time
            if p.pid not in first_run:
                first_run[p.pid] = start_time
                response_times[p.pid] = start_time - p.arrival

            gantt.append((f"P{p.pid}", time, time + p.burst))
            time += p.burst
            completion_time = time
            
            turnaround_times[p.pid] = completion_time - p.arrival
            waiting_times[p.pid] = turnaround_times[p.pid] - p.burst

        return {
            "name": "FCFS",
            "avg_wt": round(sum(waiting_times.values()) / len(processes), 2),
            "avg_tat": round(sum(turnaround_times.values()) / len(processes), 2),
            "avg_rt": round(sum(response_times.values()) / len(processes), 2),
            "gantt": gantt
        }

    def srtf(self, processes: List[Process]) -> Dict:
        n = len(processes)
        rem_bt = {p.pid: p.burst for p in processes}
        arrivals = {p.pid: p.arrival for p in processes}
        bursts = {p.pid: p.burst for p in processes}
        
        time = 0
        complete = 0
        gantt = []
        waiting_times = {}
        turnaround_times = {}
        response_times = {}
        first_run = {}
        
        last_pid = None
        last_start = 0
        
        while complete < n:
            available = [p for p in processes if p.arrival <= time and rem_bt[p.pid] > 0]
            
            if not available:
                if last_pid is not None:
                    gantt.append((f"P{last_pid}", last_start, time))
                    last_pid = None
                    
                if not gantt or gantt[-1][0] != "Idle":
                    last_start = time
                    last_pid = "Idle"
                    
                time += 1
                continue
            
            # Select shortest remaining time
            best_p = min(available, key=lambda x: (rem_bt[x.pid], x.arrival))
            
            if best_p.pid not in first_run:
                first_run[best_p.pid] = time
                response_times[best_p.pid] = time - best_p.arrival
            
            if last_pid != best_p.pid:
                if last_pid is not None:
                    gantt.append((f"P{last_pid}" if last_pid != "Idle" else "Idle", last_start, time))
                last_start = time
                last_pid = best_p.pid
                
            rem_bt[best_p.pid] -= 1
            time += 1
            
            if rem_bt[best_p.pid] == 0:
                complete += 1
                completion_time = time
                turnaround_times[best_p.pid] = completion_time - arrivals[best_p.pid]
                waiting_times[best_p.pid] = turnaround_times[best_p.pid] - bursts[best_p.pid]
                
        if last_pid is not None:
            gantt.append((f"P{last_pid}" if last_pid != "Idle" else "Idle", last_start, time))

        # Consolidate Gantt
        clean_gantt = []
        for g in gantt:
            if clean_gantt and clean_gantt[-1][0] == g[0]:
                clean_gantt[-1] = (g[0], clean_gantt[-1][1], g[2])
            else:
                clean_gantt.append(g)

        return {
            "name": "SRTF",
            "avg_wt": round(sum(waiting_times.values()) / n, 2),
            "avg_tat": round(sum(turnaround_times.values()) / n, 2),
            "avg_rt": round(sum(response_times.values()) / n, 2),
            "gantt": clean_gantt
        }

    def round_robin(self, processes: List[Process], quantum=2) -> Dict:
        n = len(processes)
        procs = sorted(processes, key=lambda x: x.arrival)
        
        rem_bt = {p.pid: p.burst for p in processes}
        arrivals = {p.pid: p.arrival for p in processes}
        bursts = {p.pid: p.burst for p in processes}
        
        time = 0
        gantt = []
        waiting_times = {}
        turnaround_times = {}
        response_times = {}
        first_run = {}
        
        ready_queue = []
        i = 0
        
        while i < n and procs[i].arrival <= time:
            ready_queue.append(procs[i])
            i += 1
            
        while ready_queue or i < n:
            if not ready_queue:
                gantt.append(("Idle", time, procs[i].arrival))
                time = procs[i].arrival
                while i < n and procs[i].arrival <= time:
                    ready_queue.append(procs[i])
                    i += 1
                continue
                
            p = ready_queue.pop(0)
            
            if p.pid not in first_run:
                first_run[p.pid] = time
                response_times[p.pid] = time - p.arrival
                
            exec_time = min(quantum, rem_bt[p.pid])
            gantt.append((f"P{p.pid}", time, time + exec_time))
            time += exec_time
            rem_bt[p.pid] -= exec_time
            
            # New processes arriving during execution time
            while i < n and procs[i].arrival <= time:
                ready_queue.append(procs[i])
                i += 1
                
            if rem_bt[p.pid] > 0:
                ready_queue.append(p)
            else:
                completion_time = time
                turnaround_times[p.pid] = completion_time - p.arrival
                waiting_times[p.pid] = turnaround_times[p.pid] - bursts[p.pid]

        clean_gantt = []
        for g in gantt:
            if clean_gantt and clean_gantt[-1][0] == g[0]:
                clean_gantt[-1] = (g[0], clean_gantt[-1][1], g[2])
            else:
                clean_gantt.append(g)

        return {
            "name": "Round Robin",
            "avg_wt": round(sum(waiting_times.values()) / n, 2),
            "avg_tat": round(sum(turnaround_times.values()) / n, 2),
            "avg_rt": round(sum(response_times.values()) / n, 2),
            "gantt": clean_gantt
        }

    def priority_preemptive(self, processes: List[Process]) -> Dict:
        n = len(processes)
        rem_bt = {p.pid: p.burst for p in processes}
        arrivals = {p.pid: p.arrival for p in processes}
        bursts = {p.pid: p.burst for p in processes}
        
        time = 0
        complete = 0
        gantt = []
        waiting_times = {}
        turnaround_times = {}
        response_times = {}
        first_run = {}
        
        last_pid = None
        last_start = 0
        
        while complete < n:
            available = [p for p in processes if p.arrival <= time and rem_bt[p.pid] > 0]
            
            if not available:
                if last_pid is not None:
                    gantt.append((f"P{last_pid}", last_start, time))
                    last_pid = None
                    
                if not gantt or gantt[-1][0] != "Idle":
                    last_start = time
                    last_pid = "Idle"
                    
                time += 1
                continue
            
            # Select lowest priority number = highest priority
            best_p = min(available, key=lambda x: (x.priority, x.arrival))
            
            if best_p.pid not in first_run:
                first_run[best_p.pid] = time
                response_times[best_p.pid] = time - best_p.arrival
            
            if last_pid != best_p.pid:
                if last_pid is not None:
                    gantt.append((f"P{last_pid}" if last_pid != "Idle" else "Idle", last_start, time))
                last_start = time
                last_pid = best_p.pid
                
            rem_bt[best_p.pid] -= 1
            time += 1
            
            if rem_bt[best_p.pid] == 0:
                complete += 1
                completion_time = time
                turnaround_times[best_p.pid] = completion_time - arrivals[best_p.pid]
                waiting_times[best_p.pid] = turnaround_times[best_p.pid] - bursts[best_p.pid]
                
        if last_pid is not None:
            gantt.append((f"P{last_pid}" if last_pid != "Idle" else "Idle", last_start, time))

        # Consolidate Gantt
        clean_gantt = []
        for g in gantt:
            if clean_gantt and clean_gantt[-1][0] == g[0]:
                clean_gantt[-1] = (g[0], clean_gantt[-1][1], g[2])
            else:
                clean_gantt.append(g)

        return {
            "name": "Priority",
            "avg_wt": round(sum(waiting_times.values()) / n, 2),
            "avg_tat": round(sum(turnaround_times.values()) / n, 2),
            "avg_rt": round(sum(response_times.values()) / n, 2),
            "gantt": clean_gantt
        }

    def run_all(self, processes: List[Process]) -> List[Dict]:
        return [
            self.fcfs(processes),
            self.srtf(processes),
            self.round_robin(processes),
            self.priority_preemptive(processes)
        ]