'''Pypi packaging setup'''

from setuptools import setup, find_packages
from tkviews import __version__ as tkviews_version

def setup_package():
    '''Package setup'''
    setup(
        name='tkviews',
        version=tkviews_version,
        description='Package for creating tkinter applications in declarative way.',
        url='https://github.com/eumis/tkviews',
        author='eumis(Eugen Misievich)',
        author_email='misievich@gmail.com',
        license='MIT',
        classifiers=[
            #   2 - Pre-Alpha
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6'
        ],
        python_requires='>=3.6',
        install_requires=['pyviews>=2.0.0'],
        keywords='binding tkinter tk tkviews pyviews python mvvm views',
        packages=find_packages(exclude=['sandbox']))

if __name__ == '__main__':
    setup_package()
