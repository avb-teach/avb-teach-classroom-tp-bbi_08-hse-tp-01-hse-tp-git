import os
import sys
import shutil

def collect_file_dirrs(in_dirr, out_dirr):
    if not os.path.isdir(in_dirr):
        print(f"Input directory does not exist: {in_dirr}")
        sys.exit(1)

    os.makedirs(out_dirr, exist_ok=True)

    for root, dirs, file_dirrs in os.walk(in_dirr):
        for file_dirr in file_dirrs:
            full_path = os.path.join(root, file_dirr)
            target_path = os.path.join(out_dirr, file_dirr)
            shutil.copy2(full_path, target_path)

if name == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)
    in_dirr = sys.argv[1]
    out_dirr = sys.argv[2]
    collect_file_dirrs(in_dirr, out_dirr)