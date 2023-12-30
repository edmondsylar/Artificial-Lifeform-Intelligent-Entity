"""
class Structure Summary Script

This script analyzes the structure of a project directory, providing information about files and folders,
including size, last modification time, and optional file content. It generates a JSON summary of the project.

Usage:
1. Specify the project directory path, included file types, and excluded file types in the 'if __name__ == "__main__":' section.
2. Run the script to display the project structure and generate a JSON summary.

Dependencies:
- Install the 'colorama' package: pip install colorama
- Install the 'hurry.filesize' package: pip install hurry.filesize

"""

import os
from datetime import datetime
from hurry.filesize import size
from colorama import init, Fore  
import json

init(autoreset=True)  

class ProjectStructure:

    """
    class Structure class analyzes the structure of a project directory and provides various functionalities.

        Attributes:
        - base_path (str): The base path of the project directory.
        - include_file_types (list): List of file types to include in the analysis (optional).
        - exclude_file_types (list): List of file types to exclude from the analysis (optional).
        - structure (dict): The hierarchical structure of the project.
        - show_file_content (bool): Flag to indicate whether to display file content.

        Methods:
        - _is_valid_file(file_name): Check if a file is valid based on included and excluded file types.
        - _build_structure(current_path, node): Recursively build the project structure.
        - _calculate_folder_size(node): Calculate the total size of a folder in bytes.
        - _calculate_total_size(): Calculate the total size of the entire project.
        - _draw_file_content(file_name, indent): Read and return the content of a file.
        - read_project_structure(): Build and store the project structure.
        - draw_project_structure(node=None, indent=0): Display the project structure.
        - create_project_summary_json(output_file="project_summary.json"): Generate a JSON summary of the project.
        - filter_files_by_size(min_size=0, max_size=float('inf')): Filter files based on size.
        - display_file_count(): Display the count of files and folders.
        - search_file(file_name): Search for a specific file in the project.
        - view_file_content(file_name): Display the content of a specific file.

        """
    def __init__(self, base_path, include_file_types=None, exclude_file_types=None):
        self.base_path = base_path
        self.include_file_types = include_file_types
        self.exclude_file_types = exclude_file_types
        self.structure = {}
        self.show_file_content = False  

    def _is_valid_file(self, file_name):
        """
        checking the validity of the file basing on its extension
        """
        if self.include_file_types and not any(file_name.lower().endswith(ext) for ext in self.include_file_types):
            return False
        if self.exclude_file_types and any(file_name.lower().endswith(ext) for ext in self.exclude_file_types):
            return False
        return True

    def _build_structure(self, current_path, node):
        """building the system structure"""
        for entry in os.listdir(current_path):
            entry_path = os.path.join(current_path, entry)
            if os.path.isdir(entry_path):
                node[entry] = {"type": "folder", "size": None, "modified": None, "content": {}}
                self._build_structure(entry_path, node[entry]["content"])
            elif os.path.isfile(entry_path) and self._is_valid_file(entry):
                size_in_bytes = os.path.getsize(entry_path)
                modified_time = datetime.fromtimestamp(os.path.getmtime(entry_path))
                node[entry] = {
                    "type": "file",
                    "size": size(size_in_bytes),
                    "modified": modified_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "content": None
                }
                if self.show_file_content:
                    node[entry]["content"] = self._draw_file_content(entry, 0)

    def _calculate_folder_size(self, node):
        total_size = 0
        for name, info in node.items():
            if info["type"] == "folder":
                total_size += self._calculate_folder_size(info["content"])
            elif info["type"] == "file":
                file_path = os.path.join(self.base_path, name)
                if os.path.exists(file_path):
                    total_size += os.path.getsize(file_path)
                else:
                    pass
        return total_size

    def _calculate_total_size(self):
        return self._calculate_folder_size(self.structure)

    def _draw_file_content(self, file_name, indent):
        file_path = os.path.join(self.base_path, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                return content
        except Exception as e:
            return f"{Fore.RED}Error reading content of {file_name}: {str(e)}"

    def read_project_structure(self):
        self._build_structure(self.base_path, self.structure)

    def draw_project_structure(self, node=None, indent=0):
        if node is None:
            node = self.structure

        for name, info in node.items():
            if info["type"] == "folder":
                print(f"{Fore.BLUE}  " * indent + f"- {name} (Folder)")
                if info["size"] is not None:
                    print(f"{Fore.CYAN}  " * (indent + 1) + f"{Fore.CYAN}Size: {info['size']}")
                if info["modified"] is not None:
                    print(f"{Fore.CYAN}  " * (indent + 1) + f"{Fore.CYAN}Last Modified: {info['modified']}")
                self.draw_project_structure(info["content"], indent + 1)
            elif info["type"] == "file":
                print(f"{Fore.GREEN}  " * indent + f"- {name} (File)")
                print(f"{Fore.CYAN}  " * (indent + 1) + f"{Fore.CYAN}Size: {info['size']}")
                print(f"{Fore.CYAN}  " * (indent + 1) + f"{Fore.CYAN}Last Modified: {info['modified']}")
                if self.show_file_content:
                    content = self._draw_file_content(name, indent + 1)
                    if content:
                        print(f"{Fore.CYAN}  " * (indent + 1) + f"{Fore.CYAN}Content:")
                        print(content)

        if indent == 0:
            total_size = self._calculate_total_size()
            print(f"\nTotal Project Size: {Fore.CYAN}{size(total_size)}")

    def create_project_summary_json(self, output_file="system_summary.json"):
        with open(output_file, "w") as json_file:
            json.dump(self.structure, json_file, indent=4)

    def _filter_files_by_size(self, node, filtered_files, min_size, max_size):
        for name, info in node.items():
            if info["type"] == "folder":
                self._filter_files_by_size(info["content"], filtered_files, min_size, max_size)
            elif info["type"] == "file":
                file_size_str = info["size"].split()[0]
                file_size_numeric = int(file_size_str) if file_size_str.isdigit() else 0
                if min_size <= file_size_numeric <= max_size:
                    filtered_files.append(os.path.join(self.base_path, name))

        return filtered_files

    def filter_files_by_size(self, min_size=None, max_size=None):
        filtered_files = {}
        self._filter_files_by_size(self.structure, filtered_files, min_size, max_size)
        return filtered_files

    def _filter_files_by_size(self, node, result, min_size, max_size):
        for name, info in node.items():
            if info["type"] == "folder":
                self._filter_files_by_size(info["content"], result, min_size, max_size)
            elif info["type"] == "file":
                file_size = self._parse_size(info["size"])
                if (min_size is None or file_size >= min_size) and (max_size is None or file_size <= max_size):
                    result[name] = info

    def _parse_size(self, size_str):
        size_parts = size_str.split()
        if len(size_parts) == 2:
            value, unit = size_parts
            return int(value)
        return 0

    def display_file_count(self):
        total_files, total_folders = self._count_files_and_folders(self.structure)
        print(f"Total Files: {Fore.CYAN}{total_files}")
        print(f"Total Folders: {Fore.CYAN}{total_folders}")

    def _count_files_and_folders(self, node):
        total_files = 0
        total_folders = 0
        for _, info in node.items():
            if info["type"] == "folder":
                total_folders += 1
                files, folders = self._count_files_and_folders(info["content"])
                total_files += files
                total_folders += folders
            elif info["type"] == "file":
                total_files += 1
        return total_files, total_folders

    def search_file(self, file_name):
        file_info = self._search_file(self.structure, file_name)
        return file_info

    def _search_file(self, node, file_name):
        for name, info in node.items():
            if info["type"] == "folder":
                file_info = self._search_file(info["content"], file_name)
                if file_info:
                    return file_info
            elif info["type"] == "file" and name == file_name:
                return info
        return None

    def view_file_content(self, file_name):
        file_path = os.path.join(self.base_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                print(content)
        else:
            print(f"{Fore.RED}File not found: {file_path}")

if __name__ == "__main__":

    # setting the project directory
    # testing section for the functionality
    # can be modified

    system_project_path = r"C:\Users\ADAN COMPUTER\Desktop\PROJECTS\ubuntu co-pilot"
    
    project_structure = ProjectStructure(
        base_path=system_project_path,
        include_file_types=[
            ".py", ".yaml", ".txt", ".cff", ".json", ".sh", ".env", ".template", ".dockerignore", ".toml",
            ".h264", ".mkv", ".flv", ".wmv", ".3gp",  ".flac", ".aac", ".wma",".bmp", ".tiff", ".ico",                  
            ".psd", ".ai", ".eps",".indd", ".cdr", ".svg",".avi", ".mpeg", ".mpg", ".mov",".ogg", ".webm",                          
            ".rpm", ".deb",".bat", ".cmd", ".sh", ".bash", ".ico", ".cur",                           
            ".webp", ".jp2", ".jxr", ".bpg",          
            ".ac3", ".mka",".blend", ".obj", ".fbx", ".stl", ".pdb", ".obj", ".pyc", ".pyd",".bak", ".old", ".swp", ".swo",           
            ".ps1", ".psm1", ".psd1",".html", ".htm", ".php",                 
            ".css", ".scss", ".less",".js", ".jsx", ".ts", ".tsx", ".vue",".java", ".class", ".jar",                
            ".py", ".pyc", ".pyd",".rb", ".rhtml", ".erb",".pl", ".pm",".cpp", ".c", ".h", 
            ".hpp", ".swift", ".m", ".mm",".go", ".dart",".lua",                               
            ".rust",".scala",".kotlin",".groovy", ".bat", ".cmd",".ps1", ".psm1",".json", ".yaml", ".yml",            
            ".xml", ".json", ".yaml", ".yml",".sql", ".db", ".sqlite",".conf", ".config", ".ini",".ini",".md", ".markdown",                      
            ".tex", ".bib",".pdf", ".doc", ".docx", ".ppt", ".pptx", ".csv",                                 
            ".rtf",".txt",".log",".bak", ".swp", ".swo",".url", ".webloc", ".desktop",       
            ".dll", ".lib", ".so", ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".zip", ".rar", ".tar", ".gz",           
            ".exe", ".msi", ".apk",".mp3", ".wav", ".ogg",".mp4", ".avi", ".mov", ".mkv",        
            ".jpeg", ".jpg", ".png", ".gif", ".svg", ".eps", ".ai",                 
            ".torrent", ".dwg", ".ppt", ".pptx",".key", ".accdb",".msg",".eml",".ics", ".apk",                                  
            ".rpm",".dmg",".iso", ".ova",".vdi", ".bak", ".backup",".conf", ".config",".ics",                                  
            ".idx", ".sub",".iso",".ova",".vdi",".bak", ".backup",                      
            ".conf", ".config", ".dll", ".sys", ".idx", ".sub", ".bat", ".com", ".cmd",                 
            ".eps", ".ps", ".gz", ".bz2", ".tar", ".xz",".dmg",".bin", ".cue",".arj", ".lzh", ".tar.gz", ".tar.bz2",   
            ".xml", ".xsl", ".xsd",".url", ".webloc", ".desktop", ".bmp", ".gif", ".png", ".tiff", ".jpg", 
            ".txt", ".ini", ".conf", ".log", ".wav", ".mp3", ".flac", ".aac",         
            ".avi", ".mp4", ".mkv", ".mov",".ttf", ".otf", ".fon", ".csv", ".tsv",                          
            ".json", ".yaml", ".yml",".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".md", ".markdown",".php", ".jsp", ".asp", ".aspx",".html", ".htm", ".css", ".js",          
            ".py", ".java", ".cpp", ".c", ".swift",   ".dll", ".lib", ".so",".exe", ".msi", ".app",                 
            ".pkg", ".deb", ".rpm", ".db", ".sqlite",".psd", ".ai", ".cdr",".wmv", ".mov", ".mkv", ".flv",         
            ".ogg", ".mp3", ".wav", ".flac", ".jpeg", ".jpg", ".png", ".gif",         
            ".ppt", ".pptx", ".key",".eml", ".msg",".log", ".txt",".tmp", ".temp", ".swp",".bak", ".old",                          
            ".srt", ".sub",".rar", ".zip", ".7z", ".tar", ".gz",    ".bak", ".backup",".conf", ".config", ".ini",".ics",".dll", ".sys",                          
            ".idx", ".sub",".m3u", ".pls",".bak",".swf",".ics", ".idx", ".sub",".in" 
        ],
        exclude_file_types=[".log"]
    )
    project_structure.read_project_structure()
    project_structure.draw_project_structure()
    project_structure.create_project_summary_json()
    filtered_files = project_structure.filter_files_by_size(min_size=0, max_size=2048) 
    print("\nFiltered Files by Size:")
    print(filtered_files)
    project_structure.display_file_count()
    search_result = project_structure.search_file("file_test.txt")  
    if search_result:
        print("\nSearch Result:")
        print(search_result)
        if project_structure.show_file_content:
            print("\nFile Content:")
            project_structure.view_file_content("file_test.txt") 
    else:
        print(f"{Fore.RED}File not found.")
