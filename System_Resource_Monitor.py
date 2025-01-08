import psutil
from time import sleep
from rich.live import Live
from rich.table import Table
from rich.console import Console

def get_system_stats():
    """Collects system resource statistics."""
    # CPU usage
    cpu_percent = psutil.cpu_percent(interval=0.1, percpu=False)
    cpu_freq = psutil.cpu_freq()
    cpu_cores = psutil.cpu_count(logical=True)

    # Memory usage
    memory = psutil.virtual_memory()

    # Disk usage
    disk = psutil.disk_usage('/')

    # Network activity
    net_io = psutil.net_io_counters()

    stats = {
        "CPU Usage (%)": cpu_percent,
        "CPU Frequency (MHz)": round(cpu_freq.current, 2) if cpu_freq else 'N/A',
        "CPU Cores": cpu_cores,
        "Memory Usage (%)": memory.percent,
        "Used Memory (GB)": round(memory.used / (1024 ** 3), 2),
        "Total Memory (GB)": round(memory.total / (1024 ** 3), 2),
        "Disk Usage (%)": disk.percent,
        "Used Disk (GB)": round(disk.used / (1024 ** 3), 2),
        "Total Disk (GB)": round(disk.total / (1024 ** 3), 2),
        "Bytes Sent (MB)": round(net_io.bytes_sent / (1024 ** 2), 2),
        "Bytes Received (MB)": round(net_io.bytes_recv / (1024 ** 2), 2),
    }
    return stats

def create_dashboard(stats):
    """Creates a dashboard table with system stats."""
    table = Table(title="System Resource Monitor", expand=True)

    table.add_column("Resource", justify="left", style="cyan", no_wrap=True)
    table.add_column("Value", justify="right", style="magenta")

    for key, value in stats.items():
        table.add_row(key, str(value))

    return table

def main():
    console = Console()
    with Live(console=console, refresh_per_second=1, screen=True) as live:
        while True:
            try:
                # Gather system stats
                stats = get_system_stats()

                # Create dashboard table
                dashboard = create_dashboard(stats)

                # Update live dashboard
                live.update(dashboard)

                sleep(1)
            except KeyboardInterrupt:
                console.print("[bold red]Exiting System Resource Monitor...")
                break

if __name__ == "__main__":
    main()
