import pathlib
from setuptools import setup

CURRENT_DIR = pathlib.Path(__file__).parent
README = (CURRENT_DIR / 'README.md').read_text()

setup(
    name='aeliant-ssh-metrics',
    version='0.1.0',
    description='Gather SSH metrics from syslog files',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/aeliant/ssh-metrics',
    author='Hamza ESSAYEGH',
    author_email='hamza.essayegh@protonmail.com',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=['ssh_metrics'],
    include_package_data=True,
    install_requires=[
        'click',
        'inflection',
        'tabulate'
    ],
    entry_points={
        'console_scripts': [
            'ssh-metrics=ssh_metrics.__init__:cli'
        ]
    }
)