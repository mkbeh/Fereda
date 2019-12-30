from setuptools import setup, find_packages
from fereda import __version__


setup(
    name='Fereda',
    version=__version__,
    description='Cyber security tool for Android images (removed or hide) restoring.',
    author='mkbeh',
    platforms='linux',
    install_requires=[
        'python-magic==0.4.15',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fereda = fereda.__main__:cli'
        ]
    }
)
