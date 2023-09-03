## Install

Use `pip` to install it to your `$PATH` as a runnable script:
```
pip install .
```

## Usage
```
usage: mktorrent-py [-h] [-c COMMENT] [-ps {256,512,1024}] tracker filename

Create torrent files

positional arguments:
  tracker               tracker url (e.g: http://tracker.com:6969/announce)
  filename              absolute or relative path to file

options:
  -h, --help            show this help message and exit
  -c COMMENT, --comment COMMENT
                        author comment for the torrent file
  -ps {256,512,1024}, --piece-size {256,512,1024}
                        piece size in KiB (default: 512)
```