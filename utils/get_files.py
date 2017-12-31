import argparse
import os
import hashlib
import shutil
from helpers import fs


def __main__():
    parser = argparse.ArgumentParser(prog='get all files with extention')
    parser.add_argument('source_dir', help='Path to folder with files')
    parser.add_argument('working_dir',
                        help='Path to working dir',
                        nargs='?',
                        default='.')
    parser.add_argument('file_ext',
                        help='Path to folder with files',
                        nargs='?',
                        default='sif')
    args = parser.parse_args()

    execute(args.source_dir, args.working_dir, args.file_ext)


def execute(source_dir, working_dir, file_ext='sif'):
    folder_full_path = os.path.abspath(source_dir)
    working_dir = os.path.abspath(working_dir)

    if not fs.create_dir(working_dir):
        exit(1)

    for file in os.listdir(working_dir):
        file_path = os.path.join(working_dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)

    for root, dirs, files in os.walk(folder_full_path):
        for file in files:
            if file.endswith('.%s' % file_ext):
                file_full_path = os.path.join(root, file)
                file_rel_path = os.path.relpath(file_full_path,
                                                folder_full_path)
                file_wo_ext = os.path.splitext(file)[0]
                sha = hashlib.sha1(file_rel_path).hexdigest()[:5]
                new_file_name = '%s.%s.%s' % (file_wo_ext, sha, file_ext)
                new_file_full_path = os.path.join(working_dir, new_file_name)

                shutil.copyfile(file_full_path, new_file_full_path)


if __name__ == '__main__':
    __main__()
