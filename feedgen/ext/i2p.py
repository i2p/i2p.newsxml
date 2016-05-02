from feedgen.ext.base import BaseExtension
from lxml import etree

I2P_NS = 'http://geti2p.net/en/docs/spec/updates'

class I2pExtension(BaseExtension):
    def __init__(self):
        self.__i2p_releases = []
        self.__i2p_revocations = None

    def extend_ns(self):
        return {'i2p': I2P_NS}

    def extend_atom(self, atom_feed):
        for release in self.__i2p_releases:
            release = release.to_atom()
            atom_feed.append(release)
        if self.__i2p_revocations is not None:
            revocations = self.__i2p_revocations.to_atom()
            atom_feed.append(revocations)
        return atom_feed

    def add_release(self, release=None):
        if release is None:
            release = Release()
        self.__i2p_releases.append(release)
        return release

    def add_revocations(self, revocations=None):
        if revocations is None:
            revocations = Revocations()
        self.__i2p_revocations = revocations
        return revocations

class I2pEntryExtension():
    def extend_atom(self, atom_feed):
        return atom_feed

class Release(object):
    def __init__(self):
        # required
        self.__release_date = None
        self.__release_version = None
        self.__release_updates = {}

        # recommended
        self.__release_min_version = None
        self.__release_min_java_version = None

    def to_atom(self):
        if not (self.__release_date and self.__release_version and self.__release_updates):
            raise ValueError('Required fields not set')

        release = etree.Element('{%s}release' % I2P_NS)
        release.attrib['date'] = self.__release_date
        version = etree.SubElement(release, '{%s}version' % I2P_NS)
        version.text = self.__release_version
        if self.__release_min_version is not None:
            release.attrib['minVersion'] = self.__release_min_version
        if self.__release_min_java_version is not None:
            release.attrib['minJavaVersion'] = self.__release_min_java_version

        for update_type, update in self.__release_updates.iteritems():
            update_node = etree.SubElement(release, '{%s}update' % I2P_NS)
            update_node.attrib['type'] = update_type

            for href in update.clearnet():
                clearnet = etree.SubElement(update_node, '{%s}clearnet' % I2P_NS)
                clearnet.attrib['href'] = href

            for href in update.clearnetssl():
                clearnetssl = etree.SubElement(update_node, '{%s}clearnetssl' % I2P_NS)
                clearnetssl.attrib['href'] = href

            if update.torrent() is not None:
                torrent = etree.SubElement(update_node, '{%s}torrent' % I2P_NS)
                torrent.attrib['href'] = update.torrent()

            for href in update.url():
                url = etree.SubElement(update_node, '{%s}url' % I2P_NS)
                url.attrib['href'] = href

        return release

    def date(self, date=None):
        if date is not None:
            self.__release_date = date
        return self.__release_date

    def version(self, version=None):
        if version is not None:
            self.__release_version = version
        return self.__release_version

    def min_version(self, min_version=None):
        if min_version is not None:
            self.__release_min_version = min_version
        return self.__release_min_version

    def min_java_version(self, min_java_version=None):
        if min_java_version is not None:
            self.__release_min_java_version = min_java_version
        return self.__release_min_java_version

    def add_update(self, update_type, update=None, replace=False):
        if update_type not in ['sud', 'su2', 'su3']:
            raise ValueError('update_type must be one of sud, su2 or su3')
        if update is None:
            update = Update()
        if self.__release_updates.has_key(update_type) and not replace:
            raise ValueError('Update type %s is already defined' % update_type)
        self.__release_updates[update_type] = update
        return update

class Update(object):
    def __init__(self):
        self.__update_clearnet    = []
        self.__update_clearnetssl = []
        self.__update_torrent     = None
        self.__update_url         = []

    def clearnet(self, clearnet=None):
        if clearnet is not None:
            self.__update_clearnet.append(clearnet)
        return self.__update_clearnet

    def clearnetssl(self, clearnetssl=None):
        if clearnetssl is not None:
            self.__update_clearnetssl.append(clearnetssl)
        return self.__update_clearnetssl

    def torrent(self, torrent=None):
        if torrent is not None:
            self.__update_torrent = torrent
        return self.__update_torrent

    def url(self, url=None):
        if url is not None:
            self.__update_url.append(url)
        return self.__update_url

class Revocations(object):
    def __init__(self):
        # required
        self.__revocations_crls = {}

    def to_atom(self):
        if not self.__revocations_crls:
            raise ValueError('Required fields not set')

        revocations = etree.Element('{%s}revocations' % I2P_NS)

        for crl_id, crl in self.__revocations_crls.iteritems():
            crl_node = etree.SubElement(revocations, '{%s}crl' % I2P_NS)
            crl_node.attrib['id'] = crl_id
            crl_node.attrib['updated'] = crl.updated().isoformat()
            crl_node.text = crl.content()

        return revocations

    def add_crl(self, crl_id, crl=None, replace=False):
        if crl is None:
            crl = Crl()
        if self.__revocations_crls.has_key(crl_id) and not replace:
            raise ValueError('CRL ID %s is already defined' % crl_id)
        self.__revocations_crls[crl_id] = crl
        return crl

class Crl(object):
    def __init__(self):
        # required
        self.__crl_updated = None
        self.__crl_content = None

    def updated(self, updated=None):
        if updated is not None:
            self.__crl_updated = updated
        return self.__crl_updated

    def content(self, content=None):
        if content is not None:
            self.__crl_content = content
        return self.__crl_content
