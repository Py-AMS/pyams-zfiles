====================
PyAMS ZFiles package
====================


Introduction
------------

This package is composed of a set of utility functions, usable into any Pyramid application.

    >>> from pyramid.testing import setUp, tearDown
    >>> config = setUp(hook_zca=True)

    >>> from pyramid_rpc.xmlrpc import includeme as include_xmlrpc
    >>> include_xmlrpc(config)
    >>> from pyramid_rpc.jsonrpc import includeme as include_jsonrpc
    >>> include_jsonrpc(config)
    >>> from cornice import includeme as include_cornice
    >>> include_cornice(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)
    >>> from pyams_security import includeme as include_security
    >>> include_security(config)
    >>> from pyams_zfiles import includeme as include_zfiles
    >>> include_zfiles(config)

    >>> tearDown()
