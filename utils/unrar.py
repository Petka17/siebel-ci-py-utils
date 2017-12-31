import argparse
import os
import rarfile


def __main__():
    parser = argparse.ArgumentParser(prog='unzip archive')
    parser.add_argument('archive', help='Path to file')
    parser.add_argument('dest_dir',
                        help='Destination folder',
                        nargs='?',
                        default='.')
    args = parser.parse_args()

    execute(args.archive, args.dest_dir)


def execute(archive, dest_dir='.'):
    file_full_path = os.path.abspath(archive)
    folder_name = os.path.splitext(os.path.basename(file_full_path))[0]
    dest_dir = os.path.abspath(os.path.join(dest_dir, folder_name))

    with rarfile.RarFile(file_full_path, 'r') as zf:
        zf.extractall(dest_dir)


if __name__ == '__main__':
    __main__()
