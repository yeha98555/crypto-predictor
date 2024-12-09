# Technical Indicators

This service is responsible for calculating technical indicators for a given stock.


## Tools
- [TA-Lib](https://github.com/mrjbq7/ta-lib)

### Installation (on Linux)
Download
[ta-lib-0.4.0-src.tar.gz](https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz/download)
and:

```
$ tar -xzf ta-lib-0.4.0-src.tar.gz
$ cd ta-lib/
$ ./configure --prefix=/usr
$ make
$ sudo make install
```
and then install the Python package:
```
uv add ta-lib
```
