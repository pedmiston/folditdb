from setuptools import setup

setup(
    name='folditdb',
    version='0.0.3',
    packages=['folditdb'],
    install_requires=[
     'SQLAlchemy==1.2.0',
     'PyMySQL==0.8.0',
    ],
    entry_points={
        'console_scripts': [
            'folditdb=folditdb.main:main',
        ],
    },
)
