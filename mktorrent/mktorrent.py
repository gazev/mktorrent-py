import os
import argparse
import time
import bencode
import hashlib

FILE_DOESNT_EXIST_ERR = 'File doesn\'t exist: '

def mktorrent(file_path: str, announce_url: str, comment: str, piece_size: int):
    """Creates a torrent file

    :param announce_url: The HTTP Tracker of the torrent we are creating
    :param file_path:    Relative or absolute path to the file we wish to create
        a torrent for
    :param comment: Comment to include in the torrent file
    :param piece_size: Size in Bytes of the pieces in the torrent file, default
        512 KiB == 512*2**10 B
    """
    if not os.path.isfile(file_path):
        print(FILE_DOESNT_EXIST_ERR + f'"{file_path}"')
        os.sys.exit(1)
    
    file_name = os.path.basename(file_path)

    meta_info = {}
    meta_info['announce']      = announce_url
    if comment:
        meta_info['comment'] = comment
    meta_info['created by']    = 'mktorrent-vug 0.1'
    meta_info['creation date'] = int(time.time())

    info = {}
    info['length']       = os.stat(file_path).st_size
    info['name']         = file_name
    info['piece length'] = piece_size
    info['pieces']       = build_pieces_str(file_path, piece_size) 

    meta_info['info'] = info

    write_to_torrent_file(meta_info)

def write_to_torrent_file(meta_info: dict):
    with open(f'{meta_info["info"]["name"]}.torrent', 'wb') as fp:
        bencode.dump(meta_info, fp)

def build_pieces_str(file_path: str, piece_size: int):
    piece_str = b""
    for piece in read_piece(file_path, piece_size):
        piece_str += hashlib.sha1(piece).digest()
    
    return piece_str

def read_piece(file_path: str, piece_size: int):
    with open(file_path, 'rb') as fp:
        while True:
            data = fp.read(piece_size)
            yield data

            if len(data) != piece_size:
                break


def entry_point():
    parser = argparse.ArgumentParser(
                        prog = 'mktorrent-py',
                        description ='Create torrent files'
                    )

    parser.add_argument('tracker', help='tracker url (e.g: http://tracker.com:6969/announce)')
    parser.add_argument('filename', help='absolute or relative path to file')
    parser.add_argument('-c', '--comment', help='author comment for the torrent file')
    parser.add_argument('-ps', '--piece-size', 
                            choices=[256, 512, 1024], 
                            default=512, 
                            help='piece size in KiB (default: %(default)s)'
                        )
    

    args = parser.parse_args()
    mktorrent(args.filename, args.tracker, args.comment, args.piece_size * 2**10)


if __name__ == '__main__':
    entry_point()