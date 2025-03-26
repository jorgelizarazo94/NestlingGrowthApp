from setuptools import setup, find_packages

setup(
    name='nestling_growth_app',
    version='0.1.0',
    description='An interactive Dash app to analyze nestling growth using biological models',
    author='Jorge Lizarazo',
    author_email='jorge.lizarazo.b@gmail.com',
    url='https://github.com/jorgelizarazo94/NestlingGrowthApp',
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
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Dash',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)