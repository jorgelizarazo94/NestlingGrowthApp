# setup
from setuptools import setup, find_packages

setup(
    name='nestling-growth-app',
    version='0.1.5',
    description='Dash app for analyzing nestling growth with logistic and non-linear models.',
    author='Jorge Lizarazo',
    packages=find_packages(include=['api', 'models', 'components']),
    include_package_data=True,
    install_requires=[
        'dash',
        'pandas',
        'numpy',
        'matplotlib',
        'plotly',
        'scipy',
        'fastapi',
        'uvicorn',
        'kaleido',
        'gunicorn'
    ],
    entry_points={
        'console_scripts': [
            'nestling-app=api.app:main'
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Dash',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)