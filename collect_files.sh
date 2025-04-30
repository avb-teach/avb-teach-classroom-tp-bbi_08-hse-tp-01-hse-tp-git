#!/bin/bash
if [[ $# -ne 2 ]]; then
  echo "Usage: $0 input_dir output_dir"
  exit 1
fi
python3 collect_files.py "$1" "$2"