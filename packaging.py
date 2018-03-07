'''Script to prepare package'''

from shutil import rmtree
from os.path import abspath
from setup import setup_package

def clean():
    '''Removes temporary files and folders'''
    try:
        directories = ['build', 'dist', 'tkviews.egg-info']
        for directory in directories:
            path = abspath(directory)
            rmtree(path)
    except FileNotFoundError:
        pass

if __name__ == '__main__':
    clean()
    setup_package()
