# -*- coding: utf-8 -*-
from feedgen.feed import FeedGenerator
import json

def load_feed_metadata(fg):
    fg.id('urn:uuid:60a76c80-d399-11d9-b91C-543213999af6')
    fg.title('I2P News')
    fg.subtitle('News feed, and router updates')
    fg.link( href='http://i2p-projekt.i2p/' )
    fg.link( href='http://echelon.i2p/news/news.atom.xml', rel='self' )
    fg.link( href='http://psi.i2p/news/news.xml', rel='alternate' )
    fg.language('en')

def load_entries(fg):
    with open('entries.html') as f:
        entries_data = f.read().strip('\n')
        entries = entries_data.split('</article>')
        # split() creates an empty final element
        for entry_str in entries[:-1]:
            entry_parts = entry_str.split('>', 1)

            fe = fg.add_entry()
            fe.id('urn:uuid:1225c695-cfb8-4ebb-aaaa-7805333efa6a')
            fe.title('0.9.20 Released')
            fe.summary(u'0.9.20 released with performance improvements and bug fixes.')
            fe.link( href='http://i2p-projekt.i2p/en/blog/post/2015/06/02/0.9.20-Release' )
            fe.author( name='zzz' )
            fe.content(entry_parts[1], type='xhtml')

def load_releases(fg):
    fg.load_extension('i2p')
    with open('releases.json') as json_data:
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

if __name__ == '__main__':
    fg = FeedGenerator()
    load_feed_metadata(fg)
    load_entries(fg)
    load_releases(fg
    fg.atom_file('news.atom.xml', pretty=True)
