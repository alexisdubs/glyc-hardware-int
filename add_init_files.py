import os

def add_init_files(base_path):
    # List of folder names to ignore
    ignored_folders = {'.git', '.vscode', '.idea', '__pycache__'}
    init_filename = '__init__.py'

    for root, dirs, files in os.walk(base_path):
        # Skip ignored folders
        dirs[:] = [d for d in dirs if d not in ignored_folders]
        
        # Check if the folder already has an __init__.py file
        if init_filename not in files:
            init_path = os.path.join(root, init_filename)
            # Create an empty __init__.py file
            with open(init_path, 'w') as f:
                pass
            print(f"Added {init_filename} to {root}")

# Replace 'your_project_path' with the absolute or relative path to your project
your_project_path = 'glycosylation_python'
add_init_files(your_project_path)
