from setuptools import setup

with open('etc/reqs.txt', 'rb') as infile:
    install_requires = infile.read().split()

setup(
    name='feedgen-i2p',
    description='I2P Atom extension for feedgen',
    author='str4d',

    install_requires=install_requires,
    packages=['feedgen.ext'],
)
