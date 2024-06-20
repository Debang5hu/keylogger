#!/bin/bash

# to rename the file from [.19062024132058.log] to [19062024132058.log]


cd ./File  # to rename the file of the target dir


shopt -s nullglob dotglob # Enable nullglob and dotglob to match hidden files and avoid errors if no match
files=(.[^.]*)



if [ ${#files[@]} -eq 0 ]; then
    echo "[+] No hidden files found!"
else
    for file in "${files[@]}"; do
        echo "[+] Renamed!"
        mv -- "$file" "${file#.}"
    done
fi
