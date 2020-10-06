from setuptools import setup

#This is only needed when reqs.txt has more than one line.
#with open('etc/reqs.txt', 'rb') as infile:
#    install_requires = infile.read().split()

setup(
    name='feedgen-i2p',
    description='I2P Atom extension for feedgen',
    author='str4d',

    install_requires="feedgen==0.3.1",
    packages=['feedgen.ext'],
)
