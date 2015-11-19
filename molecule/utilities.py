#  Copyright (c) 2015 Cisco Systems
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

import copy


def merge_dicts(a, b, raise_conflicts=False, path=None):
    """
    Merges the values of B into A.
    If the raise_conflicts flag is set to True, a LookupError will be raised if the keys are conflicting.
    :param a: the target dictionary
    :param b: the dictionary to import
    :param raise_conflicts: flag to raise an exception if two keys are colliding
    :param path: the dictionary path. Used to show where the keys are conflicting when an exception is raised.
    :return: The dictionary A with the values of the dictionary B merged into it.
    """
    # Set path.
    if path is None:
        path = []

    # Go through the keys of the 2 dictionaries.
    for key in b:
        # If the key exist in both dictionary, check whether we must update or not.
        if key in a:
            # Dig deeper for keys that have dictionary values.
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dicts(a[key], b[key], raise_conflicts=raise_conflicts, path=(path + [str(key)]))

            # Skip the identical values.
            elif a[key] == b[key]:
                pass
            else:
                # Otherwise raise an error if the same keys have different values.
                if raise_conflicts:
                    raise LookupError("Conflict at '{path}'".format(path='.'.join(path + [str(key)])))

                # Or replace the value of A with the value of B.
                a[key] = b[key]
        else:
            # If the key does not exist in A, import it.
            a[key] = copy.deepcopy(b[key]) if isinstance(b[key], dict) else b[key]

    return a