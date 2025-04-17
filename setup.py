from setuptools import setup, find_packages
from pathlib import Path

# Leer el contenido del README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='nestling_growth_app',
    version='0.1.8',
    packages=find_packages(include=['nestling_app', 'nestling_app.*']),
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
            'nestling-app = nestling_app.api.app:main'
        ]
    },
    author='Jorge Lizarazo, Juan Camilo Guerra & Gustavo A Londoño',
    author_email='jorge.lizarazo.b@gmail.com',
    description='An interactive Dash app to analyze nestling growth using biological models',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jorgelizarazo94/NestlingGrowthApp',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Framework :: Dash',
    ],
    python_requires='>=3.7',
)