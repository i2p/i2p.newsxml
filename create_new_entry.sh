#!/bin/sh
ENTRIES=entries.html

sed -i "1i <article\n  id=\"urn:uuid:`uuidgen`\"\n  title=\"\"\n  href=\"\"\n  author=\"\"\n  published=\"\"\n  updated=\"\">\n<details>\n<summary></summary>\n</details>\n<p>\n\n</p>\n</article>" $ENTRIES

if [ ! -z "$EDITOR" ]; then
    case "$EDITOR" in
        "nano" | "vim")
            $EDITOR +12 $ENTRIES
            ;;
        *)
            $EDITOR $ENTRIES
            ;;
    esac
fi
