# interface/cli.py

from utils.generator import (
    generate_cpu,
    generate_memory,
    generate_disk,
    generate_deadlock
)

from system.analyzer import SystemAnalyzer


class CLI:

    def __init__(self):
        self.analyzer = SystemAnalyzer()
        self.cpu_data = None   # initialize to avoid attribute errors

    def menu(self):
        while True:
            print("\n====== OS WORKLOAD ANALYZER ======")
            print("1. Generate Workload")
            print("2. Run Full Analysis")
            print("3. Exit")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.generate()

            elif choice == "2":
                self.run()

            elif choice == "3":
                print("Exiting...")
                break

            else:
                print("Invalid choice!")

    def generate(self):
        print("\n--- Generating Random Workload ---")

        self.cpu_data = generate_cpu()
        self.mem_data, self.frames = generate_memory()
        self.disk_data, self.head = generate_disk()
        self.alloc, self.max_need, self.avail = generate_deadlock()

        print("\nCPU Processes:")
        for p in self.cpu_data:
            print(vars(p))

        print("\nMemory Pages:", self.mem_data)
        print("Frames:", self.frames)

        print("\nDisk Requests:", self.disk_data)
        print("Head:", self.head)

        print("\nDeadlock Data Loaded")

    def run(self):
        if self.cpu_data is None:
            print("⚠️ Please generate workload first!")
            return

        print("\n====== RUNNING FULL ANALYSIS ======")

        try:
            self.analyzer.analyze_all(
                self.cpu_data,
                self.mem_data,
                self.frames,
                self.disk_data,
                self.head,
                self.alloc,
                self.max_need,
                self.avail
            )
        except Exception as e:
            print("❌ Error during analysis:", e)