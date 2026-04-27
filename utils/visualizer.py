# utils/visualizer.py

import matplotlib.pyplot as plt


def plot_cpu(results):
    """
    Plots CPU scheduling comparison
    """
    names = [r["name"] for r in results]
    values = [r["avg_wt"] for r in results]

    plt.figure()
    plt.bar(names, values)

    plt.title("CPU Scheduling Comparison")
    plt.xlabel("Algorithms")
    plt.ylabel("Average Waiting Time")

    plt.tight_layout()
    plt.savefig("cpu_comparison.png")

    try:
        plt.show()
    except:
        pass

    plt.close()


def plot_memory(fifo_faults, lru_faults, opt_faults):
    """
    Plots memory page fault comparison
    """
    names = ["FIFO", "LRU", "Optimal"]
    values = [fifo_faults, lru_faults, opt_faults]

    plt.figure()
    plt.bar(names, values)

    plt.title("Memory Page Fault Comparison")
    plt.xlabel("Algorithms")
    plt.ylabel("Page Faults")

    plt.tight_layout()
    plt.savefig("memory_comparison.png")

    try:
        plt.show()
    except:
        pass

    plt.close()


def plot_disk(fcfs_seek, sstf_seek):
    """
    Plots disk scheduling comparison
    """
    names = ["FCFS", "SSTF"]
    values = [fcfs_seek, sstf_seek]

    plt.figure()
    plt.bar(names, values)

    plt.title("Disk Scheduling Comparison")
    plt.xlabel("Algorithms")
    plt.ylabel("Seek Time")

    plt.tight_layout()
    plt.savefig("disk_comparison.png")

    try:
        plt.show()
    except:
        pass

    plt.close()