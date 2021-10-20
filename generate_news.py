#!./env/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from feedgen.feed import FeedGenerator
import glob
import json
from lxml import etree
import re
import os.path

I2P_OS = os.getenv("I2POS", "")
I2P_BRANCH = os.getenv("I2PBRANCH", "")
DATA_DIR = os.path.join('data')
RELEASE_DIR = os.path.join(DATA_DIR, I2P_OS, I2P_BRANCH)
ENTRIES_FILE = os.path.join(DATA_DIR, 'entries.html')
TRANSLATED_ENTRIES_FILES = os.path.join(DATA_DIR, 'translations/entries.*.html')
RELEASES_FILE = os.path.join(RELEASE_DIR, 'releases.json')
CRL_FILES = os.path.join(DATA_DIR, 'crls/*.crl')
BLOCKLIST_FILE = os.path.join(DATA_DIR, 'blocklist.xml')

BUILD_DIR = os.path.join('build', I2P_OS, I2P_BRANCH)
NEWS_FILE = os.path.join(BUILD_DIR, 'news.atom.xml')
TRANSLATED_NEWS_FILE = os.path.join(BUILD_DIR, 'news_%s.atom.xml')

def load_feed_metadata(fg):
    fg.id('urn:uuid:60a76c80-d399-11d9-b91C-543213999af6')
    fg.link( href='http://i2p-projekt.i2p/' )
    fg.link( href='http://echelon.i2p/news/news.atom.xml', rel='self' )
    fg.link( href='http://psi.i2p/news/news.atom.xml', rel='alternate' )

def load_entries(fg, entries_file):
    with open(entries_file) as f:
        entries_data = f.read().strip('\n')
        # Replace HTML non-breaking space with unicode
        entries_data = entries_data.replace('&nbsp;', '\u00a0')
        # Strip the leading <div> from translations
        if entries_data.startswith('<div>'):
            entries_data = entries_data[5:]

        entries_parts = entries_data.split('</header>')
        fg.title(re.findall(r'title="(.*?)"', entries_parts[0])[0])
        fg.subtitle(entries_parts[0].split('>')[1])

        entries = entries_parts[1].split('</article>')
        # split() creates a junk final element with trailing </div>
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
    with open(RELEASES_FILE) as json_data:
        d = json.load(json_data)
        for release in d:
            r = fg.i2p.add_release()
            r.date(release['date'])
            r.version(release['version'])
            if 'minVersion' in release:
                r.min_version(release['minVersion'])
            if 'minJavaVersion' in release:
                r.min_java_version(release['minJavaVersion'])

            for update_type, update in release['updates'].items():
                u = r.add_update(update_type)
                if 'clearnet' in update:
                    for url in update['clearnet']:
                        u.clearnet(url)
                if 'clearnetssl' in update:
                    for url in update['clearnetssl']:
                        u.clearnetssl(url)
                if 'torrent' in update:
                    u.torrent(update['torrent'])
                if 'url' in update:
                    for url in update['url']:
                        u.url(url)

def load_revocations(fg):
    # Only add a revocations element if there are CRLs
    r = None
    for crl in glob.glob(CRL_FILES):
        if r is None:
            r = fg.i2p.add_revocations()
        crl_id = os.path.splitext(os.path.basename(crl))[0]
        c = r.add_crl(crl_id)
        c.updated(datetime.fromtimestamp(os.path.getmtime(crl)))
        with open(crl) as f:
            crl_content = f.read().decode('utf8').strip()
            c.content('\n%s\n' % crl_content)


def load_blocklist(fg):
    # Only add a blocklist element if there is content
    b = None
    if os.path.isfile(BLOCKLIST_FILE):
        with open(BLOCKLIST_FILE) as f:
            content = '<xml xmlns:i2p="http://geti2p.net/en/docs/spec/updates">%s</xml>' % f.read()
            root = etree.fromstring(content)
            b = fg.i2p.add_blocklist()
            b.from_xml(root.getchildren()[0])


def generate_feed(entries_file=None):
    language = entries_file and entries_file.split('.')[1] or 'en'

    fg = FeedGenerator()
    fg.load_extension('i2p')
    fg.language(language)
    load_feed_metadata(fg)
    load_entries(fg, entries_file and entries_file or ENTRIES_FILE)
    load_releases(fg)
    load_revocations(fg)
    load_blocklist(fg)

    if not os.path.exists(BUILD_DIR):
        os.mkdir(BUILD_DIR)
    fg.atom_file(entries_file and TRANSLATED_NEWS_FILE % language or NEWS_FILE, pretty=True)

if __name__ == '__main__':
    # Standard feed
    generate_feed()
    # Translated feeds
    for entries_file in glob.glob(TRANSLATED_ENTRIES_FILES):
        generate_feed(entries_file)
