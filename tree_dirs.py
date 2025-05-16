import os

def tree(root=".", prefix="", output=None):
    items = [d for d in sorted(os.listdir(root)) if os.path.isdir(os.path.join(root, d)) and d != "__pycache__"]
    for i, name in enumerate(items):
        connector = "└── " if i == len(items)-1 else "├── "
        output.write(prefix + connector + name + "\n")
        branch = "    " if i == len(items)-1 else "│   "
        tree(os.path.join(root, name), prefix + branch, output)

with open("structure.txt", "w", encoding="utf-8") as f:
    tree(output=f)
