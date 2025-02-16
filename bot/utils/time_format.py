import time
import psutil
import platform
import datetime
from bot import StartTime

def get_readable_time(seconds: int) -> str:
    count = 0
    readable_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", " days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        readable_time += time_list.pop() + ", "
    time_list.reverse()
    readable_time += ": ".join(time_list)
    return readable_time
    

def get_system_info():
    # Basic OS info
    os_info = f"{platform.system()} {platform.release()}"
    kernel = platform.version()
    cpu = platform.processor() or "N/A"
    
    # Memory info (in GB)
    mem = psutil.virtual_memory()
    total_memory = mem.total / (1024 ** 3)
    
    # Uptime (you could also use psutil.boot_time() if preferred)
    uptime_seconds = time.time() - StartTime
    uptime_str = str(datetime.timedelta(seconds=int(uptime_seconds)))
    
    # Load average (Unix only; for Windows, consider alternatives)
    try:
        load = psutil.getloadavg()
        load_str = f"{load[0]:.2f}, {load[1]:.2f}, {load[2]:.2f}"
    except AttributeError:
        load_str = "N/A"

    return {
        "os": os_info,
        "kernel": kernel,
        "cpu": cpu,
        "memory": f"{total_memory:.2f} GB",
        "uptime": uptime_str,
        "load": load_str
    }