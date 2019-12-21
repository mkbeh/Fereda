from setuptools import setup, find_packages
from src import __version__


setup(
    name='Fereda',
    version=__version__,
    description='Cyber security tool for Android images restoring.',
    author='mkbeh',
    platform='linux',
    install_requires=[
        'pillow',
        'python-magic',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fereda = src.fereda:cli'
        ]
    }
)
