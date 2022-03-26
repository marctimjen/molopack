import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='molopack',
    version='0.0.1',
    author='Lentz, Magnus og Marc',
    author_email='--',
    description='Package for molo',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/marctimjen/molopack',
    project_urls = {
        "Bug Tracker": "https://github.com/marctimjen/molopack/issues"
    },
    license='MIT',
    packages=['molopack'],
    install_requires=['numpy', 'pandas', 'IPython'],
)
