#!/bin/sh
ENTRIES=data/entries.html

sed -i "2i <article\n  id=\"urn:uuid:`uuidgen`\"\n  title=\"\"\n  href=\"\"\n  author=\"\"\n  published=\"\"\n  updated=\"\">\n<details>\n<summary></summary>\n</details>\n<p>\n\n</p>\n</article>\n\n\n" $ENTRIES

if [ ! -z "$EDITOR" ]; then
    case "$EDITOR" in
        "nano" | "vim")
            $EDITOR +13 $ENTRIES
            ;;
        *)
            $EDITOR $ENTRIES
            ;;
    esac
fi
