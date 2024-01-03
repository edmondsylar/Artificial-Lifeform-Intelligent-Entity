import platform
import psutil


def get_system_info():
    my_system = platform.uname()
    memory = psutil.virtual_memory()

    markdown_text = f"System Information:\n\n"
    markdown_text += f"- System: {my_system.system}\n"
    markdown_text += f"- Node Name: {my_system.node}\n"
    markdown_text += f"- Release: {my_system.release}\n"
    markdown_text += f"- Version: {my_system.version}\n"
    markdown_text += f"- Machine: {my_system.machine}\n"
    markdown_text += f"- Processor: {my_system.processor}\n\n"
    markdown_text += f"Memory Information:\n\n"
    markdown_text += f"- Total Memory: {memory.total}\n"
    markdown_text += f"- Available Memory: {memory.available}\n"
    markdown_text += f"- Used Memory: {memory.used}\n"
    markdown_text += f"- Memory Percentage: {memory.percent}%\n"

    return markdown_text