# main.py

"""
Intelligent OS Workload Analyzer & Optimization Simulator

Entry point of the system.
Handles initialization and launches CLI interface.
"""

import sys
import traceback

from interface.cli import CLI


def print_banner():
    print("\n" + "=" * 60)
    print("   INTELLIGENT OS WORKLOAD ANALYZER")
    print("   Resource Management & Optimization Simulator")
    print("=" * 60)
    print("Features:")
    print(" - CPU Scheduling (FCFS, SRTF, RR, Priority)")
    print(" - Memory Management (FIFO, LRU, Optimal)")
    print(" - Disk Scheduling (FCFS, SSTF)")
    print(" - Deadlock Detection (Banker's Algorithm)")
    print(" - Machine Learning Recommendation System")
    print("=" * 60)


def main():
    try:
        print_banner()

        cli = CLI()

        cli.menu()

    except KeyboardInterrupt:
        print("\n\n⚠️ Program interrupted by user. Exiting safely...")

    except Exception as e:
        print("\n❌ Unexpected error occurred:")
        print(str(e))

        print("\n--- Debug Info ---")
        traceback.print_exc()

    finally:
        print("\nThank you for using OS Workload Analyzer!")
        sys.exit(0)


if __name__ == "__main__":
    main()