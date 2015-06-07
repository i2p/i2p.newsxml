#!/bin/sh
sed -i "1i <article\n  id=\"urn:uuid:`uuidgen`\"\n  title=\"\"\n  href=\"\"\n  author=\"\"\n  published=\"\"\n  updated=\"\">\n<details>\n<summary></summary>\n</details>\n<p>\n</p>\n</article>" entries.html
