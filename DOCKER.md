Signing News and Hosting a News Server with Docker
==================================================

i2p.newsxml has two containers, one for hosting the news itself, and one which
is used for running `news.sh` and `generate_news.py` in a container on Linux
distributions where Python2 support is limited or unavailable. It's also useful
if you simply prefer to manage Docker containers using Docker's or related
project's tooling(Portainer or sen for instance).

## To build the signing container, use:

``` sh
docker build --no-cache -t i2p.newsxml.signing -f Dockerfile.signing .
```

To run news.sh in the container, prepare your etc/su3.vars.custom file as if your
signing keys directory were mounted at `/.i2p-plugin-keys`. No other differences
should be required between a Docker and non-docker `news.sh` run

``` sh
docker run -it \
  -u $(id -u):$(id -g) \
  --name i2p.newsxml.signing \
  -v $HOME/.i2p-plugin-keys/:/.i2p-plugin-keys/:ro \
  -v $HOME/i2p/:/i2p/:ro \
  i2p.newsxml.signing
```

Then, extract the built feeds from the container:

``` sh
docker cp i2p.newsxml.signing:/opt/i2p.newsxml/build build
```

``` sh
docker build --no-cache -t i2p.newsxml.signing -f Dockerfile.signing .
docker rm -f i2p.newsxml.signing
docker run -it \
  -u $(id -u):$(id -g) \
  --name i2p.newsxml.signing \
  -v $HOME/.i2p-plugin-keys/:/.i2p-plugin-keys/:ro \
  -v $HOME/i2p/:/i2p/:ro \
  i2p.newsxml.signing
docker cp i2p.newsxml.signing:/opt/i2p.newsxml/build build
```


## Now, you're ready to build the hosting container:

With the feeds in `build` from the previous step, run:

``` sh
docker build -t i2p.newsxml .
```

then, to serve the files on a local port:

``` sh
docker run -d --restart=always --name newsxml -p 127.0.0.1:3000:3000 i2p.newsxml
```

``` sh
docker build -t i2p.newsxml .
docker rm -f i2p.newsxml
docker run -d --restart=always --name newsxml -p 127.0.0.1:3000:3000 i2p.newsxml
```