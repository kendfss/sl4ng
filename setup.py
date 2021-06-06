from setuptools import setup, find_packages

with open('README.md', 'r') as fob:
    long_description = fob.read()

with open('requirements.txt', 'r') as fob:
    requirements = fob.readlines()

setup(
    name='sl4ng',
    version='0.0.2',
    author='Kenneth Sabalo',
    author_email='kennethsantanasabalo@tilde.club',
    url='https://github.com/kendfss/sl4ng',
    packages=['sl4ng'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='utilities productivity',
    license='MIT',
    requires=requirements,
    python_requires='>3.9',
)