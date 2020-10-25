from setuptools import setup, find_packages
import sys

if not sys.version_info[0] == 3:
    sys.exit("ERROR: The FITHINATOR requires at least Python 3.6")
else:
    if sys.version_info[1] < 6:
        sys.exit("ERROR: The FITHINATOR requires at least Python 3.6")

setup(
    name='fithinator',
    version='0.0.1',
    description='The FITHINATOR: A status monitor for FITH TF2 servers',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=['python-a2s', 'pyyaml', 'luma.core', 'luma.emulator'],
    package_dir={'fithinator': 'fithinator/'},
    package_data={'fithinator': ['conf/*.conf']}
)
