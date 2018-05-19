
import os

def sizeof_fmt(num):
    """
    Format file sizes for a humans beings.
    http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    """
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')


def file_ext(file_name):
    """
    Get only file extention with '.'
    """
    name, extension = os.path.splitext(file_name)

    if extension in ['.avi', '.mp4', '.wmv', '.mov', '.mkv', '.flv']:
        valid_ext = True
    else:
        valid_ext = False

    return valid_ext
