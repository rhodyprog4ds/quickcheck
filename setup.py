from setuptools import setup

setup(
    name='syscourseutils',
    version='0.2.0',
    py_modules=['style',
    install_requires=[
        'Click', 'pandas', 'lxml', 'numpy','requests','html5lib'
    ],
    entry_points={
        'console_scripts': [
            'dsstylecheck = style:checknarrative',
        ],
    },
)
