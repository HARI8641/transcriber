import platform
import cpuinfo
import psutil
import GPUtil
import sys 


def to_gb(num_bytes):
    return f"{num_bytes / (1024 ** 3):.2f} GB"

# 1. System / OS Info
os_name = f"{platform.system()} {platform.release()} ({platform.architecture()[0]})"

# 1.1 python info
py_version = sys.version

# 2. CPU Metrics
cpu = cpuinfo.get_cpu_info()
freq = psutil.cpu_freq()
phys = psutil.cpu_count(logical=False) or 1
logi = psutil.cpu_count(logical=True) or 1

# 3. RAM Metrics
vmem = psutil.virtual_memory()
swap = psutil.swap_memory()

# 4. GPU Metrics
gpus = GPUtil.getGPUs()

# 5. Build Table Rows
rows = [
    ("OS", "Platform", os_name),
    ("Py", "Interpretor", py_version),
    ("CPU", "Model", cpu.get("brand_raw", "Unknown")),
    ("CPU", "Architecture", f"{cpu.get('arch', 'N/A')} ({cpu.get('bits', '')}-bit)"),
    ("CPU", "Clock (Base / Live)", f"{cpu.get('hz_advertised_friendly', 'N/A')} / {freq.current:.0f} MHz" if freq else "N/A"),
    ("CPU", "Cores / Threads", f"{phys} Cores / {logi} Threads ({logi // phys} per core)"),
    ("CPU", "L2 / L3 Cache", f"{cpu.get('l2_cache_size', 'N/A')} / {cpu.get('l3_cache_size', 'N/A')}"),
    ("RAM", "Physical (Used/Total)", f"{to_gb(vmem.used)} / {to_gb(vmem.total)} ({vmem.percent}%)"),
    ("RAM", "Available / Free", f"{to_gb(vmem.available)} / {to_gb(vmem.free)}"),
    ("RAM", "Swap (Used/Total)", f"{to_gb(swap.used)} / {to_gb(swap.total)} ({swap.percent}%)"),
]

if gpus:
    for idx, gpu in enumerate(gpus, 1):
        rows.extend([
            (f"GPU {idx}", "Model / Driver", f"{gpu.name} (v{gpu.driver})"),
            (f"GPU {idx}", "VRAM (Used/Total)", f"{gpu.memoryUsed:.0f} MB / {gpu.memoryTotal:.0f} MB ({gpu.memoryUtil * 100:.1f}%)"),
            (f"GPU {idx}", "Load / Temp", f"{gpu.load * 100:.1f}% / {gpu.temperature} °C"),
        ])
else:
    rows.append(("GPU", "Status", "No NVIDIA GPU detected via GPUtil"))




# 6. Render Table
print(f"{'Component':<10} | {'Metric':<22} | {'Value'}")
print("-" * 65)
for comp, metric, val in rows:
    print(f"{comp:<10} | {metric:<22} | {val}")
