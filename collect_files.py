import os
import sys
import shutil

def glubb(base, path):
    rel_path = os.path.relpath(path, base)
    return rel_path.count(os.sep) + 1

def collect_file_dirrs(in_dirr, out_dirr, max_depth=None):
    if not os.path.isdir(in_dirr):
        sys.exit(0)

    for root, dirrs, file_dirrs in os.walk(in_dirr):
        depth = glubb(in_dirr, root)
        if max_depth is not None and depth > max_depth:
            continue
        rel_path = os.path.relpath(root, in_dirr)
        aim_dir = os.path.join(out_dirr, rel_path)
        os.makedirs(aim_dir, exist_ok=True)

        for file_dirr in file_dirrs:
            src = os.path.join(root, file_dirr)
            if max_depth is not None:
                dst = os.path.join(aim_dir, file_dirr)
            else:
                dst = os.path.join(aim_dir, file_dirr)
                count = 1
                name, ext = os.path.splitext(file_dirr)
                while os.path.exists(dst):
                    dst = os.path.join(aim_dir, f"{name}_{count}{ext}")
                    count += 1

            shutil.copy(src, dst)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    in_dirr = sys.argv[1]
    out_dirr = sys.argv[2]
    max_depth = None

    if "--max_depth" in sys.argv:
        try:
            max_depth = int(sys.argv[i + 1])
        except:
            max_depth = None
    collect_file_dirrs(in_dirr, out_dirr, max_depth)