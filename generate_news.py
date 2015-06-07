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
    fe = fg.add_entry()
    fe.id('urn:uuid:1225c695-cfb8-4ebb-aaaa-7805333efa6a')
    fe.title('0.9.20 Released')
    fe.summary(u'0.9.20 released with performance improvements and bug fixes.')
    fe.link( href='http://i2p-projekt.i2p/en/blog/post/2015/06/02/0.9.20-Release' )
    fe.author( name='zzz' )
    fe.content('''<p>
0.9.20 contains many important bug fixes, and several changes to increase floodfill capacity in the network.
</p><p>
Routers configured for 32-64 KB of shared bandwidth may now become floodfill,
and routers configured for 512 KB or more of shared bandwidth will have higher connection limits.
These changes may cause your router to use more resources.
If the router becomes too busy, the best way to reduce usage is to reduce the <a href="/config">bandwidth settings</a>.
If that doesn't help, you may now disable automatic floodfill on the <a href="/configadvanced">advanced configuration page</a>.
</p><p>
We're hopeful that these changes will increase network capacity and performance,
and reduce the congestion that's been affecting the network the last three months.
</p><p>
As usual, we recommend that you update to this release. The best way to
maintain security and help the network is to run the latest release.
</p>''', type='xhtml')

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
