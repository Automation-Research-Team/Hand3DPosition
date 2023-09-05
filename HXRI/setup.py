from setuptools import setup

setup(

    name = 'hxri', 
    version='0.0.0.3',
    description = 'Enrique Coronado',
    packages=["hxri"],
    package_dir = {'':'src'},
    author='Enrique Coronado',
    author_email='enriquecoronadozu@gmail.com',
    url='http://enriquecoronadozu.github.io',
    include_package_data=True,
    long_description = open('README.md').read(),
    long_description_content_type = "text/markdown",
    classifiers  = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "License :: OSI Approved :: BSD License",
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Topic :: Text Processing',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: OS Independent',
    ],
    install_requires=[
          'nep'
    ],
    keywords = ['Technology'],
)
