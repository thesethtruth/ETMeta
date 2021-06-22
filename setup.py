from setuptools import setup, find_packages
setup(
    name='ETM-API-plus',
    version='1.0.0',
    description='A Python API connection to the ETM by QI, with as bonus integration to Excel and EMA.',
    url='https://github.com/thesethtruth/ETM-EMA-API',
    author='Seth van Wieringen',
    author_email='seth@uu-engineering.nl',
    license='MIT',

    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers :: Energy consultants',
    'Topic :: Energy Transition :: Parametric Experiments :: API :: ETM',

    # Pick your license as you wish (should match "license" above)
    'License :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
],
    packages=find_packages("src"),  # include all packages under src
    package_dir={"": "src"},   # tell distutils packages are under src
    package_data={
        # And include any *.pkl files found in the "data" subdirectory
        # of the "ETM-EMA-API" package, also:
        "ETM-EMA-API": ["data/*.pkl"],
    },
    install_requires=[
        'pandas',
        'numpy',
        'requests',
        'beautifulsoup4', # @seth perhaps remove this dependency by fixing the get_ID with requests?
        'openpyxl',
        'seaborn', # @seth only used for static colorschemes, could be hard coded
    ],
    python_requires='>=3.6',
)