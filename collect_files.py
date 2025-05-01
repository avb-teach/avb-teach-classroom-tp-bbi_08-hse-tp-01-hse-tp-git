import os
import sys
import shutil

def glubb(base, path):
    rel_path = os.path.relpath(path, base)
    return rel_path.count(os.sep)

def collect_file_dirrs(in_dirr, out_dirr, max_depth=None):
    if not os.path.isdir(in_dirr):
        sys.exit(0)

    os.makedirs(out_dirr, exist_ok=True)

    for root, dirs, files in os.walk(in_dirr):
        depth = glubb(in_dirr, root)
        
        if max_depth is not None and depth >= max_depth:
            continue

        rel_path = os.path.relpath(root, in_dirr)
        
        if max_depth is None:
            target_dir = out_dirr
        else:
            path_parts = rel_path.split(os.sep)
            preserved_parts = path_parts[:max_depth-1] if max_depth > 1 else []
            target_dir = os.path.join(out_dirr, *preserved_parts)
            os.makedirs(target_dir, exist_ok=True)

        for file in files:
            src = os.path.join(root, file)
            dst = os.path.join(target_dir, file)
            
            if max_depth is None:
                name, ext = os.path.splitext(file)
                count = 1
                while os.path.exists(dst):
                    dst = os.path.join(target_dir, f"{name}_{count}{ext}")
                    count += 1

            shutil.copy2(src, dst)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    in_dirr = sys.argv[1]
    out_dirr = sys.argv[2]
    max_depth = None

    if "--max_depth" in sys.argv:
        try:
            idx = sys.argv.index("--max_depth")
            if idx + 1 < len(sys.argv):
                max_depth = int(sys.argv[idx + 1])
        except:
            pass

    collect_file_dirrs(in_dirr, out_dirr, max_depth)