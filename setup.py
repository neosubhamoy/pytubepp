from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf8') as file:
    readme = file.read()


setup(
    name='pytubepp',
    version='1.1.0',
    description='A Simple CLI Tool to Download Your Favorite YouTube Videos Effortlessly!',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Subhamoy Biswas',
    author_email='hey@neosubhamoy.com',
    license='MIT',
    packages=find_packages(),
    python_requires=">=3.8",
    url="https://github.com/neosubhamoy/pytubepp",
    entry_points={
        'console_scripts': [
            'pytubepp=pytubepp.main:main',
        ],
    },
    install_requires=[
        'pytubefix',
        'requests',
        'ffmpy',
        'mutagen',
        'tabulate',
        'tqdm',
        'appdirs',
        'setuptools',
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python",
        "Topic :: Internet",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
        "Topic :: Multimedia :: Video :: Conversion",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Terminals",
        "Topic :: Utilities",
    ],
    keywords=["youtube", "download", "video", "pytube", "cli"],
    project_urls={
        "Bug Reports": "https://github.com/neosubhamoy/pytubepp/issues",
    },
)