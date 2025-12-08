"""Code pulled from future python versions, here for compatibility"""

try:
    from collections.abc import MutableMapping, KeysView, ValuesView, ItemsView
except ImportError:
    from collections import MutableMapping, KeysView, ValuesView, ItemsView
from collections import OrderedDict
from functools import total_ordering


