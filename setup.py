#!/usr/bin/env python
#
# Copyright 2011 Masayoshi Sekimura
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from setuptools import setup

setup(
    name='fbconsole',
    version='0.1',
    description='A simple TypePad api client for writing command line scripts.',
    author='Masayoshi Sekimura, SAY Media, Inc',
    author_email='msekimura@saymedia.com',
    url='http://github.com/saymedia/tpconsole',
    package_dir={'': 'src'},
    py_modules=[
        'tpconsole',
    ],
    license="Apache 2.0",
    install_requires=['typepad'],
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        ],
    entry_points = """
      [console_scripts]
      tpconsole = tpconsole:shell
    """,

    )
