# coding=utf-8
# Copyright 2024 AAAASTARK.
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
"""Functions related to web applications"""

import os
import requests
import warnings


def download_from(url, path):
    r"""
    Download file from url. If invalid URL is detected it will print message and it will return empty string for file downloaded path.

    Arguments:

        url (:obj:`str`):
            Web path of file.

        path (:obj:`str`):
            Path to save the file.

    Returns:

        :obj:`str`: Path where file was saved.

    Note:

        It will not work with .zip urls from Dropbox. Need to fix it!

    """

    # get file name from url
    file_name = os.path.basename(url)
    if file_name[-4:] == '.zip':
        # Warning - it mights not download the actual zip. It will not work with Dropbox.
        warnings.warn(f'File name {file_name} is a zip. It might not download it properly!',
                      UserWarning)

    # create directory frm path if it doesn't exist
    os.makedirs(path) if not os.path.isdir(path) else None
    # find path where file will be saved
    file_path = os.path.join(path, file_name)

    # if files does not exist - download
    response = requests.get(url)
    # Chekc if url is valid or not.
    if response.status_code != 200:
        # Invalid or not responsive url.
        print(f'Invalid url! Return code: {response.status_code}')
        # Return empty string for file_path

        return ''

    # check if file already exists
    elif not os.path.isfile(file_path):
        # Download file.
        file_size = open(file_path, 'wb').write(response.content)
        file_size = '{0:.2f}MB'.format(file_size / 1024)
        # print file details
        print("%s %s" % (file_path, file_size))

    return file_path
