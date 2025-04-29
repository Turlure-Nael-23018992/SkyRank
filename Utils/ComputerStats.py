import psutil
import GPUtil
from tabulate import tabulate

def display_pc_stats():
    # Retrieve information about the RAM
    mem = psutil.virtual_memory()
    ram_total = mem.total / (1024 ** 3)  # Convert to GB
    ram_used = mem.used / (1024 ** 3)  # Convert to GB
    ram_free = mem.available / (1024 ** 3)  # Convert to GB

    # Retrieve information about the processor
    cpu_logical_cores = psutil.cpu_count()
    cpu_physical_cores = psutil.cpu_count(logical=False)
    cpu_freq = psutil.cpu_freq()
    cpu_freq_max = cpu_freq.max
    cpu_freq_min = cpu_freq.min
    cpu_freq_current = cpu_freq.current
    cpu_usage = psutil.cpu_percent(interval=1)

    # Retrieve information about the GPU
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

    # Display information in a tabular format
    print("RAM:")
    ram_table = [
        ["Total", f"{ram_total:.2f} GB"],
        ["Used", f"{ram_used:.2f} GB"],
        ["Free", f"{ram_free:.2f} GB"]
    ]
    print(tabulate(ram_table, headers=["Type", "Value"], tablefmt="grid"))

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

# Call the function to display PC stats
display_pc_stats()



#g++ -shared -o liblm.so -fPIC C:\Users\Julie\Documents\Pro\Prog\Python\CoSky\CoSky\Utils\dpidp_cpp.cpp


#"D:\Documents\Documents\Pro\Prog\Python\pypy3.9-v7.3.11-win64\pypy3.9-v7.3.11-win64\python3.9.exe" C:\Users\Julie\Documents\Pro\Prog\Python\CoSky\CoSky\Algorithms\DP_IDP_cpp.py

#"D:\Documents\Documents\Pro\Prog\Python\pypy3.9-v7.3.11-win64\pypy3.9-v7.3.11-win64\python3.9.exe" AppRun.py
#"D:\Documents\Documents\Pro\Prog\Python\pypy3.9-v7.3.11-win64\pypy3.9-v7.3.11-win64\python3.9.exe" C:\Users\Julie\Documents\Pro\Prog\Python\CoSky\CoSky\Algorithms\DP_IDP.py

"""

[500] iterations...
        ALGO [SkyIR]
        ALGO [DP_IDP]

        ALGO [CoskySQL]
        ALGO [CoskyAlgorithme]
        [SkyIR]:
                [temps]:1.0662 s
                [temps/samples]:0.0021324877738952636
        [DP_IDP]:
                [temps]:8.1627 s
                [temps/samples]:0.016325428009033204
        [CoskySQL]:
                [temps]:0.007 s
                [temps/samples]:1.3994216918945312e-05
        [CoskyAlgorithme]:
                [temps]:0.012 s
                [temps/samples]:2.40020751953125e-05
[1000] iterations...
        ALGO [SkyIR]
        ALGO [DP_IDP]

        ALGO [CoskySQL]
        ALGO [CoskyAlgorithme]
        [SkyIR]:
                [temps]:10.6366 s
                [temps/samples]:0.01063663411140442
        [DP_IDP]:
                [temps]:1mins - 2secs
                [temps/samples]:0.062197747945785524
        [CoskySQL]:
                [temps]:0.013 s
                [temps/samples]:1.2959957122802734e-05
        [CoskyAlgorithme]:
                [temps]:0.064 s
                [temps/samples]:6.399798393249512e-05

"""