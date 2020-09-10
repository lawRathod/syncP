from setuptools import setup, find_packages
from io import open
from os import path

import pathlib
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# automatically captured required modules for install_requires in requirements.txt
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
  all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
  not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs \
                    if 'git+' not in x]
setup (
  name = 'syncP',
  description = 'A mpv syncing tool among clients and host for local media files',
  version = '1.0.0.1',
  packages = find_packages(), # list of all packages
  install_requires = install_requires,
  python_requires='>=3.4',
  include_package_data=True,
  entry_points='''
        [console_scripts]
        syncp=syncP.__main__:run
  ''',
  author="Prateek Rathod",
  keyword="sync, mpv, watchtogether",
  long_description=README,
  long_description_content_type="text/markdown",
  license='MIT',
  url='https://github.com/lawRathod/syncP',
  download_url='https://github.com/lawRathod/syncP',
  dependency_links=dependency_links,
  author_email='prateekrathod.dev@gmail.com',
  classifiers=[
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
  ]
)
