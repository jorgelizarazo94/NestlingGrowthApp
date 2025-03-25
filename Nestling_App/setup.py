# setup
from setuptools import setup, find_packages

setup(
    name='nestling_app',
    version='0.1.0',
    packages=find_packages(),
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
        ]
    },
)