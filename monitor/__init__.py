import psutil


rom = psutil.disk_usage("/").percent


def monitor():
    NetIO = psutil.net_io_counters()
    info = {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "recv": NetIO.bytes_recv,
        "send": NetIO.bytes_sent,
    }
    print(info)


if __name__ == "__main__":
    from timeit import timeit
    print(1/(timeit(stmt=monitor, number=100) / 100))
