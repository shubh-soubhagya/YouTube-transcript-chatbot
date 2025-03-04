import os
import pkg_resources
import re
import sys

# Set project root directory
project_dir = os.path.dirname(os.path.abspath(__file__))

# Step 1: Extract all imported libraries from .py files (including subdirectories)
imported_libs = set()
built_in_modules = set(sys.builtin_module_names)  # Get Python built-in modules

for root, _, files in os.walk(project_dir):
    for file in files:
        if file.endswith(".py"):
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                for line in f:
                    match = re.match(r"^\s*(?:import|from) (\w+)", line)
                    if match:
                        lib = match.group(1)
                        if lib not in built_in_modules:  # Exclude built-in modules
                            imported_libs.add(lib)

# Step 2: Find installed versions of the used libraries
installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
used_packages = {lib: installed_packages.get(lib.lower(), "") for lib in imported_libs if lib.lower() in installed_packages}

# Step 3: Write to requirements.txt
with open("requirements.txt", "w") as req_file:
    for lib, version in used_packages.items():
        if version:
            req_file.write(f"{lib}=={version}\n")
        else:
            req_file.write(f"{lib}\n")  # Some modules may not have versions

print("✅ requirements.txt generated successfully with all dependencies!")
