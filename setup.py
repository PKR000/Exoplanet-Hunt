from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line and not line.startswith('#')]

setup(
    name='exoplanet_hunt',
    version='0.1.0',
    packages=find_packages(where='src'),  # Finds packages in the 'src' directory
    package_dir={'': 'src'},  # Root package is located in 'src'
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'exoplanet-hunt=src.main:main',  # Entry point for the command line script
        ],
    },
)
