#!/bin/bash

TARGET_DIR="${1:-$HOME/Downloads}" 
ORGANIZED_DIR="$TARGET_DIR/Organized" 

create_folders() {
    mkdir -p "$ORGANIZED_DIR"
    mkdir -p "$ORGANIZED_DIR/Images" "$ORGANIZED_DIR/Documents" "$ORGANIZED_DIR/Archives" \
             "$ORGANIZED_DIR/Videos" "$ORGANIZED_DIR/Music" "$ORGANIZED_DIR/Programs" "$ORGANIZED_DIR/Others"
}

move_files() {
    shopt -s nocaseglob

    mv "$TARGET_DIR"/*.{jpg,jpeg,png,gif,bmp,tiff} "$ORGANIZED_DIR/Images/" 2>/dev/null
    mv "$TARGET_DIR"/*.{pdf,doc,docx,xls,xlsx,ppt,pptx,txt,odt} "$ORGANIZED_DIR/Documents/" 2>/dev/null
    mv "$TARGET_DIR"/*.{zip,rar,tar.gz,gz,7z} "$ORGANIZED_DIR/Archives/" 2>/dev/null
    mv "$TARGET_DIR"/*.{mp4,mkv,avi,mov} "$ORGANIZED_DIR/Videos/" 2>/dev/null
    mv "$TARGET_DIR"/*.{mp3,wav,flac,m4a} "$ORGANIZED_DIR/Music/" 2>/dev/null
    mv "$TARGET_DIR"/*.{dmg,pkg} "$ORGANIZED_DIR/Programs/" 2>/dev/null
    mv "$TARGET_DIR"/* "$ORGANIZED_DIR/Others/" 2>/dev/null

    shopt -u nocaseglob
}

main() {
    if [[ ! -d "$TARGET_DIR" ]]; then
        printf "Path does not exist.\n" >&2
        return 1
    fi
    
    create_folders
    move_files
    printf "Files organized successfully.\n"
}

main "$@"
