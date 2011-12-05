# -*- coding: utf-8; -*-
# from distutils.core import setup
from setuptools import setup, find_packages
setup(name='simplefmf',
    description="An easy way to write fmf files",
    long_description="""The Full Meta-Data Format is specified in
    
    http://arxiv.org/abs/0904.1299 
    
    This module gives a hackish way to write it.""",
    version='0.1.1',
    author="Rolf Würdemann",
    author_email="Rolf.Wuerdemann@fmf.uni-freiburg.de",
    maintainer="Rolf Würdemann",
    maintainer_email="Rolf.Wuerdemann@fmf.uni-freiburg.de",
    license = "BSD",
    url="http://arxiv.org/abs/0904.1299",
    py_modules=['simplefmf'],
    packages = find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Environment :: Console",
        "License :: OSI Approved :: BSD License",
     ],
    zip_safe=True,

)


