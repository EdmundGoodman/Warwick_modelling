from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'tiered_antibiotic_resistance_model',
    packages=find_packages(),
    version = '4.0.0',
    license='MIT',
    description = 'A validated computational model of the spread of an antibiotic resistant pathogens in a hospital, with and without our diagnostic tool for quickly identifying it',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'Edmund Goodman',
    author_email = 'egoodman3141@gmail.com',
    url = 'https://github.com/EdmundGoodman/Warwick_modelling',
    download_url = 'https://github.com/EdmundGoodman/Warwick_modelling/archive/refs/tags/v4.0.0.tar.gz',
    keywords = ['iGEM', 'synthetic biology', 'model'],
    install_requires = [
        'matplotlib',
        'pandas',
        'seaborn'
    ],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
