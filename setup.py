from setuptools import setup, find_packages

setup(
    name='ifc_metadata_extractor',
    version='0.1',
    description='A tool for extracting metadata from IFC files and saving it as JSON',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tim Ebben',
    url='https://github.com/sogelink-research/ifc-meta-extractor',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'ifcopenshell==0.7.10',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',  # Minimum Python version required
    entry_points={
        'console_scripts': [
            'ifc-meta-extractor=scripts.process_ifc:main',
        ],
    },
)
