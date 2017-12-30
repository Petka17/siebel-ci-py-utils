import argparse
import os
from helpers import Ftp
from helpers import fs

# Usage:
# python download_archives.py \
# -s ftp.dlptest.com \
# -l dlpuser@dlptest.com \
# -p fwRhzAnR1vgig8s \
# -b '/base/path/on/server' \
# -w './path/to/work/dir' \
# 'file1' 'file2'


def __main__():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(prog='get files from server')

    parser.add_argument('-s',
                        '--server',
                        help='Host IP or Name',
                        required=True)
    parser.add_argument('-t',
                        '--port',
                        help='Port',
                        default='21')
    parser.add_argument('-l',
                        '--login',
                        help='Login',
                        required=True)
    parser.add_argument('-p',
                        '--password',
                        help='Password',
                        required=True)
    parser.add_argument('-b',
                        '--base-path',
                        help='Base Path',
                        default='/')
    parser.add_argument('-w',
                        '--working-dir',
                        help='Working Directory',
                        default=current_dir)
    parser.add_argument('files',
                        help='File List',
                        nargs='+')

    args = parser.parse_args()

    # Create working if it is not exist
    working_dir = os.path.abspath(args.working_dir)

    if not fs.create_dir(working_dir):
        exit(1)

    # Get files
    files = Ftp(args.server,
                args.port,
                args.login,
                args.password,
                args.base_path
                ).get_file(working_dir,
                           *args.files)

    # Write file list disk
    with open('downloaded_files.txt', 'w') as f:
        for file_name in files:
            f.write('%s\n' % file_name)


if __name__ == '__main__':
    __main__()
