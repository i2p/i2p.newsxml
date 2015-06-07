# -*- coding: utf-8 -*-
from feedgen.feed import FeedGenerator
import sys

if __name__ == '__main__':
    fg = FeedGenerator()
    fg.id('urn:uuid:60a76c80-d399-11d9-b91C-543213999af6')
    fg.title('I2P News')
    fg.subtitle('News feed, and router updates')
    fg.link( href='http://i2p-projekt.i2p/' )
    fg.link( href='http://echelon.i2p/news/news.atom.xml', rel='self' )
    fg.link( href='http://psi.i2p/news/news.xml', rel='alternate' )
    fg.language('en')

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

    fg.load_extension('i2p')
    r = fg.i2p.add_release()
    r.date('2015-06-02')
    r.version('0.9.20')
    r.min_version('0.6.1.10')
    r.min_java_version('1.6')
    u = r.add_update('su3')
    u.torrent('magnet:?xt=urn:btih:4b8b4c161f1829004627963b930d45f67f523b2e&amp;dn=i2pupdate-0.9.20.su3&amp;tr=http://tracker2.postman.i2p/announce.php')
    u.url('http://stats.i2p/i2p/0.9.20/i2pupdate.su3')
    u = r.add_update('su2')
    u.torrent('magnet:?xt=urn:btih:3aba5739b585f5d7a46aec6095b0c6f8471f93cc&amp;dn=i2pupdate-0.9.20.su2&amp;tr=http://tracker2.postman.i2p/announce.php')
    u.url('http://stats.i2p/i2p/0.9.20/i2pupdate.su2')
    u = r.add_update('sud')
    u.url('http://stats.i2p/i2p/0.9.20/i2pupdate.sud')

    fg.atom_file('news.atom.xml', pretty=True)
