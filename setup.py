from setuptools import setup, find_packages

setup(
    name = "partaidetza",
    version = "1.0",
    url = '',
    license = 'BSD',
    description = "Partaidetza plataforma",
    author = 'Elhuyar Fundazioa',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)
