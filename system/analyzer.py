# system/analyzer.py

from core.cpu import CPUScheduler
from core.memory import fifo_detailed, lru, optimal
from core.disk import fcfs as disk_fcfs, sstf
from core.deadlock import is_safe_detailed
from ml.model import MLModel
from utils.explainer import explain_cpu, explain_memory
from utils.visualizer import plot_cpu, plot_memory, plot_disk


class SystemAnalyzer:

    def __init__(self):
        self.cpu = CPUScheduler()
        self.ml = MLModel()
        print("\n🔄 Training ML model...")
        self.ml.train()

    def analyze_all(self, processes, pages, frames, disk_req, head, alloc, max_need, avail):

        # ================= CPU =================
        print("\n" + "="*60)
        print("CPU SCHEDULING ANALYSIS")
        print("="*60)

        print("\nProcesses:")
        for p in processes:
            print(vars(p))

        cpu_results = self.cpu.run_all(processes)

        print("\n--- GANTT CHART (FCFS) ---")
        for g in cpu_results[0]["gantt"]:
            print(f"P{g[0]} [{g[1]}-{g[2]}]", end=" | ")

        print("\n\n--- DETAILED RESULTS ---")
        print("Algorithm        | Avg Waiting Time")
        print("------------------------------------")
        for r in cpu_results:
            print(f"{r['name']:15} | {r['avg_wt']}")

        best = min(cpu_results, key=lambda x: x["avg_wt"])
        ml_pred = self.ml.predict(processes)

        print("\n--- ANALYSIS ---")
        print("Best Algorithm (Actual):", best["name"])
        print("ML Predicted:", ml_pred)

        if best["name"] == ml_pred:
            print("✔ ML correctly identified optimal scheduling strategy")
        else:
            print("ℹ ML suggested alternative strategy based on learned patterns")

        print("Reason:", explain_cpu(processes))

        print("\n📊 Generating CPU graph...")
        plot_cpu(cpu_results)

        # ================= MEMORY =================
        print("\n" + "="*60)
        print("MEMORY MANAGEMENT ANALYSIS")
        print("="*60)

        print("\nPage Reference String:", pages)
        print("Frames:", frames)

        f = fifo_detailed(pages, frames)
        l = lru(pages, frames)
        o = optimal(pages, frames)

        print("\n--- COMPARISON TABLE ---")
        print("Algorithm | Page Faults")
        print("------------------------")
        print(f"FIFO      | {f}")
        print(f"LRU       | {l}")
        print(f"Optimal   | {o}")

        best_mem = min([("FIFO", f), ("LRU", l), ("OPT", o)], key=lambda x: x[1])

        print("\nBest Algorithm:", best_mem[0])
        print("Explanation:", explain_memory(f, l, o))

        print("\n📊 Generating Memory graph...")
        plot_memory(f, l, o)

        # ================= DISK =================
        print("\n" + "="*60)
        print("DISK SCHEDULING ANALYSIS")
        print("="*60)

        print("\nDisk Requests:", disk_req)
        print("Initial Head:", head)

        f1 = disk_fcfs(disk_req, head)
        s1 = sstf(disk_req, head)

        print("\n--- RESULTS ---")
        print("Algorithm | Seek Time")
        print("----------------------")
        print(f"FCFS      | {f1}")
        print(f"SSTF      | {s1}")

        if f1 < s1:
            print("\nBest Algorithm: FCFS")
        else:
            print("\nBest Algorithm: SSTF")

        print("\nInsight:")
        print("SSTF reduces head movement by selecting nearest request.")

        print("\n📊 Generating Disk graph...")
        plot_disk(f1, s1)

        # ================= DEADLOCK =================
        print("\n" + "="*60)
        print("DEADLOCK DETECTION ANALYSIS")
        print("="*60)

        print("\nAllocation Matrix:", alloc)
        print("Max Need Matrix:", max_need)
        print("Available Resources:", avail)

        safe, seq = is_safe_detailed(alloc, max_need, avail)

        print("\n--- FINAL RESULT ---")
        if safe:
            print("✔ System is SAFE")
            print("Sequence:", " -> ".join(f"P{i}" for i in seq))
        else:
            print("❌ System is UNSAFE (Deadlock)")
            print("Some processes cannot proceed due to insufficient resources.")

        print("\nConclusion:")
        print("Deadlock occurs when processes compete for limited resources without release.")