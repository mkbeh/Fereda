# -*- coding: utf-8 -*-


# This file is part of Fereda.

# Fereda is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License 3 as published by
# the Free Software Foundation.

# Fereda is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Fereda.  If not, see <https://www.gnu.org/licenses/>.


# Copyright (c) 2020 January mkbeh


from setuptools import setup, find_packages
from fereda import __version__


setup(
    name='Fereda',
    version=__version__,
    description='Cyber security tool for Android images (removed or hide) restoring.',
    author='R3N3V4L TEAM',
    platforms='linux android',
    install_requires=[
        'python-magic==0.4.15',
        'Pillow==6.2.1',
        'ImageHash==4.0',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fereda = fereda.__main__:cli'
        ]
    }
)
