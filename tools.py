import os

def create_folder(input_value):
    if isinstance(input_value, str):
        path = input_value
    elif isinstance(input_value, dict):
        path = input_value.get("path", "")
    else:
        raise ValueError("Invalid input type for create_folder")

    if not path:
        raise ValueError("Path is required")

    os.makedirs(path, exist_ok=True)
    return f"Folder '{path}' created."
def write_code_to_file(input):
    path = input.get("path")
    content = input.get("content")
    
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
        return f"✅ File written: {os.path.abspath(path)}"
    except Exception as e:
        return f"❌ Failed to write to {path}: {e}"

def append_to_file(input):
    path = input.get("path")
    content = input.get("content")
    with open(path, "a") as f:
        f.write(content)
    return f"Content appended to: {path}"

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def get_file_tree(_=None):
    tree = []
    for root, dirs, files in os.walk("."):
        for file in files:
            tree.append(os.path.join(root, file))
    return tree

def run_command(cmd):
    result = os.popen(cmd).read()
    return result

available_tools = {
    "create_folder": create_folder,
    "write_code_to_file": write_code_to_file,
    "append_to_file": append_to_file,
    "read_file": read_file,
    "get_file_tree": get_file_tree,
    "run_command": run_command,
}
