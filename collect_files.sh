#!/bin/bash

if [[ $# -lt 2 ]]; then
  echo "Использование: $0 <input_dir> <output_dir> [--max_depth <N>]"
  exit 1
fi

input_directory=$1
output_directory=$2

if [[ ! -d "$input_directory" ]]; then
  echo "Error: Входная директория '$input_directory' не существует"
  exit 1
fi

if [[ -d "$output_directory" ]]; then
  if [[ $(ls -A "$output_directory") ]]; then
    echo "Error: Выходная директория '$output_directory' не пуста"
    exit 1
  fi
fi

shift 2

max_depth=""

while [[ $# -gt 0 ]]; do
  if [[ "$1" == "--max_depth" ]]; then
    if [[ -n "${2-}" && "$2" =~ ^[0-9]+$ ]]; then
      max_depth=$2
      shift 2
    else
      echo "Error: --max_depth должен быть не негативным целочисленным аргументом"
      exit 1
    fi
  else
    echo "Error: Неизвестный параметр: $1"
    exit 1
  fi
done

if command -v python3 &> /dev/null; then
  PYTHON=python3
elif command -v python &> /dev/null; then
  PYTHON=python
else
  echo "Python не найден. Устанавливаем..."
  if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt update && sudo apt install -y python3
    PYTHON=python3
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    if command -v brew &> /dev/null; then
      brew install python
      PYTHON=python3
    else
      echo "Error: Homebrew не установлен. Установите Homebrew или Python вручную."
      exit 1
    fi
  else
    echo "Error: Неподдерживаемая ОС. Установите Python вручную."
    exit 1
  fi
fi

$PYTHON - "$input_directory" "$output_directory" "$max_depth" << 'EOF'
import os, shutil, sys

input_directory = sys.argv[1]
input_directory = os.path.abspath(input_directory)

output_directory = sys.argv[2]
output_directory = os.path.abspath(output_directory)

max_depth = None
if len(sys.argv) > 3 and sys.argv[3]:
    max_depth = int(sys.argv[3])

for root, dirs, files in os.walk(input_directory):
    depth = root[len(input_directory):].count(os.sep)

    rel_path = os.path.relpath(root, input_directory)
    rel_parts = rel_path.split(os.sep) if rel_path != '.' else []

    trimmed_parts = rel_parts
    if max_depth is not None:
        trimmed_parts = rel_parts[-(max_depth - 1):]

    dest_dir = os.path.join(output_directory, *trimmed_parts)
    dest_dir = os.path.normpath(dest_dir)

    os.makedirs(dest_dir, exist_ok=True)
    for file in files:
        src_file = os.path.join(root, file)
        dest_file = os.path.join(dest_dir, file)
        shutil.copy2(src_file, dest_file)
EOF

