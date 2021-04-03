from setuptools import setup

setup(
    name='skynet',
    version='1.0',
    packages=['skynet'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': ['setup-func=skynet.hello:fly'],
    }
)
