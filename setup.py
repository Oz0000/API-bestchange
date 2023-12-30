from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='best-change-myapi',
    version='0.0.1',
    description='BestChange API',
    Long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='pvalsduo',
    author_email='pvalsduo@gmail.com',
    License='MIT',
    classifiers=classifiers,
    keywords='API',
    packages=find_packages(),
    install_requires=['requests', 'bs4', 'lxml', 'fake-useragent']
)

