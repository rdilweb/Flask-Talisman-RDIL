# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools

long_description = open('README.md', 'r', encoding='utf-8').read()


setuptools.setup(
    name='flask-talisman-rdil',
    version='0.9.7',
    description='HTTP security headers for Flask. (UNOFFICIAL, UNSUPPORTED FORK)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/RDIL/Flask-Talisman-RDIL',
    author='Thea Flowers',
    author_email='theaflowers@google.com',
    maintainer="Reece Dunham",
    maintainer_email="me@rdil.rocks",
    license='Apache 2.0',
    keywords='fork unsupported',
    packages=setuptools.find_packages(),
    python_requires=">3.3",
    package_data={
        "flask_talisman": "py.typed"
    }
)
