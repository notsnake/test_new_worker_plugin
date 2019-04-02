"""Setuptools script."""

from setuptools import setup, find_packages

setup(
    name='tfw_myworker',
    version='0.1',
    description='Finder recent github and pastebin posts by regular expressions',
    long_description="Finder recent github and pastebin posts by regular expressions",
    classifiers=[
        "Programming Language :: Python"
    ],
    author='SMYT',
    author_email='mail@smyt.ru',
    url='https://www.smyt.ru/',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='tfw_myworker',
    install_requires=[
        'tf-workers==0.3',
        'requests==2.21.0',
        'lxml==4.3.3',
    ],
)
