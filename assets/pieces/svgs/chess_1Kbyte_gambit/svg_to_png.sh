#!/bin/bash

# Loop over all SVG files in the current directory
for file in *.svg; do
    # Get the file name without extension
    name="${file%.*}"
    # Convert the SVG file to PNG
    inkscape "$file" --export-filename="../../pngs/chess_1Kbyte_gambit/$name.png" --export-type=png --export-width=135 --export-height=135
done
