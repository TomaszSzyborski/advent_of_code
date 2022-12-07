"""
--- Part Two ---
Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is 70000000.
To run the update, you need unused space of at least 30000000.
You need to find a directory you can delete that will free up enough space to run the update.

In the example above, the total size of the outermost directory
(and thus the total amount of used space) is 48381165;
this means that the size of the unused space must currently be 21618835,
which isn't quite the 30000000 required by the update.
Therefore, the update still requires a directory with total size of at least 8381165 to be deleted before it can run.

To achieve this, you have the following options:

Delete directory e, which would increase unused space by 584.
Delete directory a, which would increase unused space by 94853.
Delete directory d, which would increase unused space by 24933642.
Delete directory /, which would increase unused space by 48381165.
Directories e and a are both too small; deleting them would not free up enough space.
However, directories d and / are both big enough!
Between these, choose the smallest: d, increasing unused space by 24933642.

Find the smallest directory that, if deleted,
would free up enough space on the filesystem to run the update. What is the total size of that directory?
"""
import logging
import os
from dataclasses import dataclass

log_level = {
    "debug": logging.DEBUG,
    "info": logging.INFO
}.get(os.environ.get('LOG_LEVEL'), logging.INFO)

logging.basicConfig(level=log_level)
log = logging.getLogger()

@dataclass
class File:
    size: int
    name: str
    path: str

    def __repr__(self):
        return f"{self.path}{self.name} {self.size}B"


if __name__ == '__main__':
    puzzle_input_file_path = "puzzle_input.txt"

    with open(puzzle_input_file_path, 'r') as f:
        terminal = f.read().splitlines()

    log.info(terminal)
    path = "/"
    files_list = []
    folder_list = [path]
    for line in terminal[1:]:
        match line.split():
            case ["$", "ls"]:
                pass
            case ["$", "cd", ".."]:
                path = "/".join(path.strip("/").split("/")[:-1])
                path = f"/{path}"
            case ["$", "cd", name]:
                if not path.endswith("/"):
                    path += "/"
                path += f"{name}/"
                folder_list.append(path)
                print(path)
            case ["dir", name]:
                print(f"Directory of {name=} in {path}")
            case [size, name]:
                print(f"File called {name} of size {size=} in {path}")
                print(f"{File(size=int(size), name=name, path=path)}")
                files_list.append(File(size=int(size), name=name, path=path))
    print(files_list)
    print(folder_list)

    folder_weight = {}
    for folder in folder_list:
        folder_weight[folder] = []
        for file in files_list:
            if file.path.startswith(folder):
                folder_weight[folder].append(file.size)

    print(f"Weight per folder: {folder_weight}")

    total_disk_available = 70_000_000
    free_space_needed = 30_000_000
    total_folder_weights = []
    size_used = sum(folder_weight["/"])
    for folder_to_delete, files_weight_list in folder_weight.items():
        total_folder_weights.append(sum(files_weight_list))

    print(f"Total folder weights: {sorted(total_folder_weights)}")
    print(f"Disk used: {size_used}")
    print(f"Disk available: {total_disk_available - size_used}")
    for folder in sorted(total_folder_weights):
        if total_disk_available - size_used + folder >= free_space_needed:
            print(f"Single folder to delete has weight {folder}")
            break

