import os
import subprocess
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Mapping for special imports to PyPI package names
SPECIAL_CASES = {
    "cv2": "opencv-python",
    "cvzone": "cvzone",
}

def find_imports_in_scripts():
    """Scan all Python files in the given folder for imported libraries."""
    libraries = set()

    for file in os.listdir('.'):
        if file.endswith(".py"):  # Only process Python files
            try:
                with open(file,"r") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("import ") or line.startswith("from "):
                            parts = line.split()
                            imported_module = parts[1].split(".")[0]
                            libraries.add(imported_module)
            except Exception as e:
                logging.error(f"Error reading file {file}: {e}")
    return libraries

def resolve_library_names(libraries):
    """Resolve special cases and map library names to PyPI package names."""
    return {SPECIAL_CASES.get(lib, lib) for lib in libraries}

def install_and_update_requirements(libraries, requirements_file="requirements.txt"):
    #Install libraries and update the requirements.txt file.
    installed_libraries = set()
    for library in libraries:
        try:
            __import__(library.split("==")[0])  # Check if library is installed
            installed_libraries.add(library)
        except ImportError:
            logging.info(f"{library} not found. Installing...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", library])
                installed_libraries.add(library)
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to install {library}: {e}")

# Update requirements.txt
    with open(requirements_file, "w") as f:
        for library in sorted(installed_libraries):
            f.write(f"{library}\n")
    logging.info("Requirements file updated successfully!")

if __name__ == "__main__":
    libraries = find_imports_in_scripts()
    if libraries:
        resolved_libraries = resolve_library_names(libraries)
        install_and_update_requirements(resolved_libraries)
    else:
            print("No libraries found to install.")

    print("Environment setup completed successfully!")