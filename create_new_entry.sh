#!/bin/sh

ENTRIES=data/$I2POS/$I2PBRANCH/entries.html
UUIDGEN="`which uuidgen || which uuid`"

sed -i "3i <article\n  id=\"urn:uuid:`$UUIDGEN`\"\n  title=\"\"\n  href=\"\"\n  author=\"\"\n  published=\"\"\n  updated=\"\">\n<details>\n<summary></summary>\n</details>\n<p>\n\n</p>\n</article>\n\n\n" $ENTRIES

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
