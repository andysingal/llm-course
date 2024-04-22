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
"""Functions that are used on array like variables/objects"""

import numpy as np
import warnings


def pad_array(variable_length_array, fixed_length=None, axis=1, pad_value=0.0):
    r"""
    Pad variable length array to a fixed numpy array.
    It can handle single arrays [1,2,3] or nested arrays [[1,2],[3]].

    Arguments:

        variable_length_array (:obj:`list / np.ndarray`):
            Single arrays [1,2,3] or nested arrays [[1,2],[3]].

        fixed_length (:obj:`int`, `optional`):
            Max length of rows for numpy. This argument is optional and it will have a `None` value attributed
            inside the function.

        axis (:obj:`int`, `optional`, defaults to :obj:`1`):
            Directions along rows: 1 or columns: 0. This argument is optional and it has a default value attributed
            inside the function.

        pad_value (:obj:`float`, `optional`, defaults to :obj:`0.0`):
            What value to use as padding, default is 0. This argument is optional and it has a default value attributed
            inside the function.=0.0

    Returns:

        :obj:`np.ndarray`:  axis=1: fixed numpy array shape [len of array, fixed_length].
                            axis=0: fixed numpy array shape [fixed_length, len of array].

    Raises:
        ValueError: If `axis` does not have 0 or 1 value.

        ValueError: If `variable_length_array` does not have same row length for column padding `axis=0`.

        ValueError: If `variable_length_array` is not valid format.

    """

    # padded array in numpy format
    numpy_array = None

    # Make sure axis is right value.
    if axis not in [1, 0]:
        # axis value is wrong
        raise ValueError("`axis` value needs to be 1 for row padding \
                    or 0 for column padding!")

    # find fixed_length if no value given
    fixed_length = max([len(row) for row in variable_length_array]) if fixed_length is None else fixed_length

    # array of arrays
    if isinstance(variable_length_array[0], list) or isinstance(
            variable_length_array[0], np.ndarray):

        if axis == 1:
            # perform padding on rows
            numpy_array = np.ones((len(variable_length_array), fixed_length)) * pad_value
            # verify each row
            for numpy_row, array_row in zip(numpy_array, variable_length_array):
                # concatenate array row if it is longer
                array_row = array_row[:fixed_length]
                numpy_row[:len(array_row)] = array_row

        elif axis == 0:
            # make sure all rows have same length
            if not all([len(row) == len(variable_length_array[0])
                        for row in variable_length_array]):
                raise ValueError("`variable_length_array` need to have same row length for column padding `axis=0`!")
            # padding on columns
            if fixed_length >= len(variable_length_array):
                # need to pad
                numpy_array = np.ones((fixed_length, len(variable_length_array[0]))) * pad_value
                numpy_array[:len(variable_length_array)] = variable_length_array
            else:
                # need to cut array
                numpy_array = np.array(variable_length_array[:fixed_length])

        return numpy_array

    # array of values
    elif isinstance(variable_length_array, list) or isinstance(
            variable_length_array, np.ndarray):

        if axis == 1:
            # perform padding on rows
            numpy_array = np.ones(fixed_length) * pad_value
            variable_length_array = variable_length_array[:fixed_length]
            numpy_array[:len(variable_length_array)] = variable_length_array

        elif axis == 0:
            # padding on columns
            numpy_array = np.ones((fixed_length, len(variable_length_array))) * pad_value
            numpy_array[0] = variable_length_array

        return numpy_array

    else:
        # array is not a valid format
        raise ValueError("`variable_length_array` is not a valid format.")


def batch_array(list_values, batch_size):
    r"""
    Split a list into batches/chunks. Last batch size is remaining of list values.

    Note:

      This is also called chunking. I call it batches since I use it more in ML.

    Arguments:

        list_values (:obj:`list / np.ndarray`):
            Can be any kind of list/array.

        batch_size (:obj:`int`):
            Value of the batch length.

    Returns:

        :obj:`np.ndarray`: List of batches from list_values.

    Raises:

        UserWarning: If `batch_size` is greater than length of `list_values`.

        ValueError: If `list_values` is not valid format.

    """

    if isinstance(list_values, list) or isinstance(list_values, np.ndarray):
        # make sure to warn user if `list_value` has correct type

        if len(list_values) < batch_size:
            # make sure batch size is not greater than length of list
            warnings.warn("`batch_size` is greater than length of `list_values`!", UserWarning)

            return [list_values]

        # create new list of batches
        batched_list = [list_values[i * batch_size:(i + 1) * batch_size] for i in
                        range((len(list_values) + batch_size - 1) // batch_size)]

        return batched_list

    else:
        # raise error if `list_values` is not of type array
        raise ValueError("`list_values` must be of type list!")
