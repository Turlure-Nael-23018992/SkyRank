import psutil
import GPUtil
from tabulate import tabulate

def display_pc_stats():
    """
    Display detailed statistics about the PC hardware, including RAM, CPU, and GPU information.
    """

    # Retrieve RAM information
    mem = psutil.virtual_memory()
    ram_total = mem.total / (1024 ** 3)  # Convert bytes to GB
    ram_used = mem.used / (1024 ** 3)    # Convert bytes to GB
    ram_free = mem.available / (1024 ** 3)  # Convert bytes to GB

    # Retrieve CPU information
    cpu_logical_cores = psutil.cpu_count()
    cpu_physical_cores = psutil.cpu_count(logical=False)
    cpu_freq = psutil.cpu_freq()
    cpu_freq_max = cpu_freq.max
    cpu_freq_min = cpu_freq.min
    cpu_freq_current = cpu_freq.current
    cpu_usage = psutil.cpu_percent(interval=1)

    # Retrieve GPU information
    gpus = GPUtil.getGPUs()
    gpu_info = []
    for gpu in gpus:
        gpu_info.append({
            "id": gpu.id,
            "name": gpu.name,
            "load": f"{gpu.load * 100} %",
            "free_memory": f"{gpu.memoryFree} MB",
            "used_memory": f"{gpu.memoryUsed} MB",
            "total_memory": f"{gpu.memoryTotal} MB",
            "temperature": f"{gpu.temperature} °C"
        })

    # Display RAM information
    print("RAM:")
    ram_table = [
        ["Total", f"{ram_total:.2f} GB"],
        ["Used", f"{ram_used:.2f} GB"],
        ["Free", f"{ram_free:.2f} GB"]
    ]
    print(tabulate(ram_table, headers=["Type", "Value"], tablefmt="grid"))

    # Display CPU information
    print("\nProcessor:")
    cpu_table = [
        ["Logical Cores", cpu_logical_cores],
        ["Physical Cores", cpu_physical_cores],
        ["Max Frequency", f"{cpu_freq_max:.2f} MHz"],
        ["Min Frequency", f"{cpu_freq_min:.2f} MHz"],
        ["Current Frequency", f"{cpu_freq_current:.2f} MHz"],
        ["Usage", f"{cpu_usage} %"]
    ]
    print(tabulate(cpu_table, headers=["Type", "Value"], tablefmt="grid"))

    # Display GPU information
    if gpu_info:
        print("\nGPU:")
        gpu_table = []
        for gpu in gpu_info:
            gpu_table.append([
                gpu["id"],
                gpu["name"],
                gpu["load"],
                gpu["free_memory"],
                gpu["used_memory"],
                gpu["total_memory"],
                gpu["temperature"]
            ])
        print(tabulate(gpu_table, headers=["ID", "Name", "Load", "Free Memory", "Used Memory", "Total Memory", "Temperature"], tablefmt="grid"))
    else:
        print("\nGPU: No GPU detected")

# Call the function to display all PC statistics
display_pc_stats()

# --- Notes ---

# Command to compile a C++ file into a shared library (for use in Python):
# g++ -shared -o liblm.so -fPIC C:\Users\Julie\Documents\Pro\Prog\Python\CoSky\CoSky\Utils\dpidp_cpp.cpp

# Example of how to execute Python scripts with PyPy interpreter:
# "D:\Documents\Documents\Pro\Prog\Python\pypy3.9-v7.3.11-win64\pypy3.9-v7.3.11-win64\python3.9.exe" C:\Users\Julie\Documents\Pro\Prog\Python\CoSky\CoSky\Algorithms\DP_IDP_cpp.py
# "D:\Documents\Documents\Pro\Prog\Python\pypy3.9-v7.3.11-win64\pypy3.9-v7.3.11-win64\python3.9.exe" AppRun.py
# "D:\Documents\Documents\Pro\Prog\Python\pypy3.9-v7.3.11-win64\pypy3.9-v7.3.11-win64\python3.9.exe" C:\Users\Julie\Documents\Pro\Prog\Python\CoSky\CoSky\Algorithms\DP_IDP.py

"""
--- Example of benchmark results (500 and 1000 iterations) ---

[500] iterations...
    ALGO [SkyIR]
    ALGO [DP_IDP]
    ALGO [CoskySQL]
    ALGO [CoskyAlgorithme]

    [SkyIR]:
        [Time]: 1.0662 s
        [Time/sample]: 0.0021324877738952636
    [DP_IDP]:
        [Time]: 8.1627 s
        [Time/sample]: 0.016325428009033204
    [CoskySQL]:
        [Time]: 0.007 s
        [Time/sample]: 1.3994216918945312e-05
    [CoskyAlgorithme]:
        [Time]: 0.012 s
        [Time/sample]: 2.40020751953125e-05

[1000] iterations...
    ALGO [SkyIR]
    ALGO [DP_IDP]
    ALGO [CoskySQL]
    ALGO [CoskyAlgorithme]

    [SkyIR]:
        [Time]: 10.6366 s
        [Time/sample]: 0.01063663411140442
    [DP_IDP]:
        [Time]: 1min - 2s
        [Time/sample]: 0.062197747945785524
    [CoskySQL]:
        [Time]: 0.013 s
        [Time/sample]: 1.2959957122802734e-05
    [CoskyAlgorithme]:
        [Time]: 0.064 s
        [Time/sample]: 6.399798393249512e-05
"""
