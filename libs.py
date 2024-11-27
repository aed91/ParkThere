import os
import subprocess
import sys
import logging
from YOLO.setup_YOLO import check_python_version, install_pytorch, setup_yolov5

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Mapping for special imports to PyPI package names
SPECIAL_CASES = {
    "cv2": "opencv-python",
    "cvzone": "cvzone",
}

def find_imports_in_scripts(folder_path):
    """Scan all Python files in the given folder for imported libraries."""
    libraries = set()
    local_modules = set(file[:-3] for file in os.listdir(folder_path) if file.endswith(".py"))

    for file in os.listdir(folder_path):
        if file.endswith(".py"):  # Only process Python files
            file_path = os.path.join(folder_path, file)
            with open(file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("import ") or line.startswith("from "):
                        parts = line.split()
                        imported_module = parts[1].split(".")[0]
                        if imported_module not in local_modules:
                            libraries.add(imported_module)
    return libraries

def resolve_library_names(libraries):
    #Resolve special cases and map library names to PyPI package names.
    return {SPECIAL_CASES.get(lib, lib) for lib in libraries}

def install_and_update_requirements(libraries, requirements_file):
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
    os.makedirs(os.path.dirname(requirements_file), exist_ok=True)
    with open(requirements_file, "w") as f:
        for library in sorted(installed_libraries):
            f.write(f"{library}\n")
    logging.info("Requirements file updated successfully!")

def resolve_library_names(libraries):
    #Resolves special cases and maps library names to PyPI package names.
    resolved_libraries = set()
    for lib in libraries:
        # Map special cases or use the original name
        resolved_libraries.add(SPECIAL_CASES.get(lib, lib))
    return resolved_libraries


def setup_environment():
    """Set up the Python environment for the project."""
    # Step 1: Check Python Version
    check_python_version()

    # Step 2: Install PyTorch
    install_pytorch()

    # Step 3: Clone and Set Up YOLOv5
    setup_yolov5()

    # Step 4: Install Other Dependencies
    folder_path = os.path.dirname(__file__)  # Path to 'src'
    requirements_file = os.path.join(folder_path, "..", "logs", "requirements.txt")

    print(f"Scanning Python scripts in {folder_path}...")
    libraries = find_imports_in_scripts(folder_path)
    if libraries:
        resolved_libraries = resolve_library_names(libraries)
        install_and_update_requirements(resolved_libraries, requirements_file)
    else:
        print("No libraries found to install.")

    print("Environment setup completed successfully!")


if __name__ == "__main__":
    setup_environment()