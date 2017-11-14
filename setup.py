from setuptools import setup

setup(
    name='folditdb',
    packages=['folditdb'],
    entry_points={
        'console_scripts': [
            'folditdb=folditdb:main',
        ],
    },
)
