#! /usr/bin/env sh

# 与えられた名文字列の末尾を .ipynb から .md にしたものを返す
change_ext_ipynb_to_md() {
    arg_filename="$1"

    case "$arg_filename" in
        *.ipynb)
            echo "${arg_filename%.ipynb}.md"
            ;;
        *)
            echo "Error: The file does not have a .ipynb extension." >&2
            return 1
            ;;
    esac
}

# `**/__marimo__/<ノートブック名>.ipynb` に対し, `**/<ノートブック名>.md` を返す. 
make_output_path() {
    input_filename="$1"
    dir=$(dirname $(dirname $input_filename))
    file=$(change_ext_ipynb_to_md $(basename $input_filename))
    output_filename="$dir/$file"

    echo $output_filename
}

my_nbconvert() {
    input_filename="$1"
    output_filename=$(make_output_path $input_filename)
    cat "$input_filename" \
        | jaq '.metadata.kernelspec = { "display_name": ".venv", "language": "python", "name": "python3" } | .metadata.language_info = { "name": "python" }' \
        | uvx --from nbconvert jupyter-nbconvert --to markdown --stdin --output $output_filename --HighlightMagicsPreprocessor.enabled=True --template=./with_prompt_and_quote.tpl
}

for file in $(fd --extension ipynb); do
    my_nbconvert "$file" || {
        break
    }
done

