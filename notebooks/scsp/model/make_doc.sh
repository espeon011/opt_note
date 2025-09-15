#! /usr/bin/env sh

# Function to remove docstring header and following empty lines from python file
clean_python_file() {
    # Remove fixed docstring pattern and following empty lines
    sed '1,3d; /./,$!d' "$1"
}

# Function to merge markdown and python files
merge_md_py() {
    {
        cat "$1"
        if [ "$(tail -c 1 "$1" | wc -l)" -eq 0 ]; then
            echo ""
        fi
        echo ""
        echo "## Python Code"
        echo ""
        echo "\`\`\`python"
        clean_python_file "$2"
        echo "\`\`\`"
    } > "$3"
}

# Main processing
SOURCE_DIR="../../../src/opt_note/scsp/model"

# Search for directories under SOURCE_DIR (excluding __pycache__)
for dir in "$SOURCE_DIR"/*; do
    if [ -d "$dir" ]; then
        dir_name=$(basename "$dir")
        
        # Skip __pycache__ directory
        if [ "$dir_name" = "__pycache__" ]; then
            continue
        fi
        
        # Create directory in current directory (no error if exists)
        mkdir -p "$dir_name"
        
        # Merge README.md and __init__.py
        readme_file="$dir/README.md"
        init_file="$dir/__init__.py"
        output_file="./$dir_name/README.md"
        
        merge_md_py "$readme_file" "$init_file" "$output_file"
        
        echo "Created: $output_file"
    fi
done
