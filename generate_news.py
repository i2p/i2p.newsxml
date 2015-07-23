#!./env/bin/python
# -*- coding: utf-8 -*-
from feedgen.feed import FeedGenerator
import glob
import json
import re
import os.path

DATA_DIR = 'data'
ENTRIES_FILE = os.path.join(DATA_DIR, 'entries.html')
TRANSLATED_ENTRIES_FILES = os.path.join(DATA_DIR, 'translations/entries.*.html')
RELEASES_FILE = os.path.join(DATA_DIR, 'releases.json')

BUILD_DIR = 'build'
NEWS_FILE = os.path.join(BUILD_DIR, 'news.atom.xml')
TRANSLATED_NEWS_FILE = os.path.join(BUILD_DIR, 'news_%s.atom.xml')

def load_feed_metadata(fg):
    fg.id('urn:uuid:60a76c80-d399-11d9-b91C-543213999af6')
    fg.link( href='http://i2p-projekt.i2p/' )
    fg.link( href='http://echelon.i2p/news/news.atom.xml', rel='self' )
    fg.link( href='http://psi.i2p/news/news.atom.xml', rel='alternate' )

def load_entries(fg, entries_file):
    with open(entries_file) as f:
        entries_data = f.read().decode('utf8').strip('\n')
        # Replace HTML non-breaking space with unicode
        entries_data = entries_data.replace('&nbsp;', u'\u00a0')
        # Strip the leading <div> from translations
        if entries_data.startswith('<div>'):
            entries_data = entries_data[5:]

        entries_parts = entries_data.split('</header>')
        fg.title(re.findall(r'title="(.*?)"', entries_parts[0])[0])
        fg.subtitle(entries_parts[0].split('>')[1])

        entries = entries_parts[1].split('</article>')
        # split() creates an empty final element for source,
        # and a junk final element for translations
        for entry_str in entries[:-1]:
            entry_parts = entry_str.split('</details>', 1)
            metadata = extract_entry_metadata(entry_parts[0])

            fe = fg.add_entry()
            fe.id(metadata['id'])
            fe.title(metadata['title'])
            fe.summary(metadata['summary'])
            fe.link( href=metadata['href'] )
            fe.author( name=metadata['author'] )
            fe.published(metadata['published'])
            fe.updated(metadata['updated'])
            fe.content(entry_parts[1], type='xhtml')

def extract_entry_metadata(s):
    m = {k:v.strip('"') for k,v in re.findall(r'(\S+)=(".*?"|\S+)', s)}
    m['summary'] = re.findall(r'<summary>(.*)</summary>', s)[0]
    return m

def load_releases(fg):
    fg.load_extension('i2p')
    with open(RELEASES_FILE) as json_data:
        d = json.load(json_data)
        for release in d:
            r = fg.i2p.add_release()
            r.date(release['date'])
            r.version(release['version'])
            if release.has_key('minVersion'):
                r.min_version(release['minVersion'])
            if release.has_key('minJavaVersion'):
                r.min_java_version(release['minJavaVersion'])

            for update_type, update in release['updates'].iteritems():
                u = r.add_update(update_type)
                if update.has_key('clearnet'):
                    for url in update['clearnet']:
                        u.clearnet(url)
                if update.has_key('clearnetssl'):
                    for url in update['clearnetssl']:
                        u.clearnetssl(url)
                if update.has_key('torrent'):
                    u.torrent(update['torrent'])
                if update.has_key('url'):
                    for url in update['url']:
                        u.url(url)

def generate_feed(entries_file=None):
    language = entries_file and entries_file.split('.')[1] or 'en'

    fg = FeedGenerator()
    fg.language(language)
    load_feed_metadata(fg)
    load_entries(fg, entries_file and entries_file or ENTRIES_FILE)
    load_releases(fg)

    if not os.path.exists(BUILD_DIR):
        os.mkdir(BUILD_DIR)
    fg.atom_file(entries_file and TRANSLATED_NEWS_FILE % language or NEWS_FILE, pretty=True)

if __name__ == '__main__':
    # Standard feed
    generate_feed()
    # Translated feeds
    for entries_file in glob.glob(TRANSLATED_ENTRIES_FILES):
        generate_feed(entries_file)
