if [ "$#" -ne 2 ]; then
  echo "Usage: $0 input_dir output_dir"
  exit 1
fi

input_dir="$1"
output_dir="$2"

if [ ! -d "$input_dir" ]; then
  echo "Input directory does not exist."
  exit 1
fi

mkdir -p "$output_dir"

find "$input_dir" -type f | while read -r file; do
  filename=$(basename "$file")
  cp "$file" "$output_dir/$filename"
done