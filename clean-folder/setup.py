from setuptools import setup, find_namespace_packages

setup(
    name='clean-folder',
    version='1',
    description='clean folder',
    url='https://github.com/korickij/Tutorial/blob/main/proga.py',
    author='Ivan Korickij',
    author_email='kitmobi@gmail.com',
    license='GoIT',
    install_requires=["pathlib", "shutil"],
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean_folder = clean_folder.clean:main']}
)
