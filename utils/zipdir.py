import shutil


def zipdir(path):
    shutil.make_archive(path, "zip", path)
