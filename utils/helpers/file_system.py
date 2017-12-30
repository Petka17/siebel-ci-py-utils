import os


def create_dir(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            print 'Error occur while creating folders'
            print e
            return False

    if not os.access(path, os.W_OK):
        print 'Working is read only'
        return False

    return True


def get_file_name_wo_ext(file_name):
    os.path.splitext(os.path.basename(file_name))[0]
