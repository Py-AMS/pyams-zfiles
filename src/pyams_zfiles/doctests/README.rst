====================
PyAMS ZFiles package
====================


Introduction
------------

This package is composed of a set of utility functions, usable into any Pyramid application.

    >>> import tempfile
    >>> temp_dir = tempfile.mkdtemp()

    >>> from pyramid.testing import setUp, tearDown, DummyRequest
    >>> config = setUp(hook_zca=True)
    >>> config.registry.settings['zodbconn.uri'] = 'file://{dir}/Data.fs?blobstorage_dir={dir}/blobs'.format(
    ...     dir=temp_dir)

    >>> import transaction
    >>> from pyramid_zodbconn import includeme as include_zodbconn
    >>> include_zodbconn(config)
    >>> from pyramid_rpc.xmlrpc import includeme as include_xmlrpc
    >>> include_xmlrpc(config)
    >>> from pyramid_rpc.jsonrpc import includeme as include_jsonrpc
    >>> include_jsonrpc(config)
    >>> from cornice import includeme as include_cornice
    >>> include_cornice(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)
    >>> from pyams_site import includeme as include_site
    >>> include_site(config)
    >>> from pyams_i18n import includeme as include_i18n
    >>> include_i18n(config)
    >>> from pyams_catalog import includeme as include_catalog
    >>> include_catalog(config)
    >>> from pyams_file import includeme as include_file
    >>> include_file(config)
    >>> from pyams_security import includeme as include_security
    >>> include_security(config)
    >>> from pyams_workflow import includeme as include_workflow
    >>> include_workflow(config)
    >>> from pyams_zfiles import includeme as include_zfiles
    >>> include_zfiles(config)

    >>> from pyams_site.generations import upgrade_site
    >>> request = DummyRequest()
    >>> app = upgrade_site(request)
    Upgrading PyAMS timezone to generation 1...
    Upgrading PyAMS I18n to generation 1...
    Upgrading PyAMS catalog to generation 1...
    Upgrading PyAMS file to generation 3...

    >>> from zope.annotation.interfaces import IAttributeAnnotatable
    >>> from zope.dublincore.interfaces import IZopeDublinCore
    >>> from zope.dublincore.annotatableadapter import ZDCAnnotatableAdapter
    >>> config.registry.registerAdapter(ZDCAnnotatableAdapter, (IAttributeAnnotatable, ), IZopeDublinCore)


Adding new documents
--------------------

    >>> from pyams_utils.registry import set_local_registry
    >>> set_local_registry(app.getSiteManager())

    >>> from pyams_utils.registry import get_utility
    >>> from pyams_zfiles.interfaces import IDocumentContainer

    >>> utility = get_utility(IDocumentContainer)
    >>> utility
    <pyams_zfiles.utility.DocumentContainer object at 0x...>

    >>> utility.oid_prefix = 'ZF:'

    >>> import base64
    >>> from pyams_security.principal import PrincipalInfo
    >>> encoded = base64.encodebytes(b'admin:admin').decode()
    >>> request = DummyRequest(headers={'Authorization': 'Basic {}'.format(encoded)})
    >>> request.principal = PrincipalInfo(id='system:admin')

    >>> from pyramid.threadlocal import manager
    >>> manager.push({'request': request, 'registry': config.registry})

    >>> data = b"This is my document content"
    >>> properties = {
    ...     'application_name': 'PyAMS test application',
    ...     'title': 'Test document',
    ...     'owner': 'admin:admin',
    ...     'filename': 'test.txt',
    ...     'tags': ['Tag 1', 'Tag 2'],
    ...     'Custom 1': "Value 1",
    ...     'Custom 2': "Value 2"
    ... }
    >>> document = utility.add_document(data, properties, request)
    >>> transaction.commit()

    >>> document
    <pyams_zfiles.document.DocumentVersion object at 0x...>

    >>> oid = document.oid

    >>> from pprint import pprint
    >>> pprint(document.to_json())
    {'access_mode': 'private',
     'api': 'http://example.com/api/zfiles/rest/ZF:...',
     'application_name': 'PyAMS test application',
     'content_type': 'text/plain',
     'created_time': None,
     'creator': 'system:admin',
     'filename': 'test.txt',
     'filesize': 27,
     'hash': '04b251e9e34e6d58efde44ebafd7c769a630cdcf633c134af1e8b247100b6e774d3dccfe236e2b7ef96fbe829b3896128b201e0aa1079f99bc7ef532d58860aa',
     'href': 'http://example.com/++etc++site/ZFiles/.../.../ZF:.../++versions++/1/++attr++data',
     'managers': [],
     'oid': 'ZF:...',
     'owner': 'admin:admin',
     'properties': {'Custom 1': 'Value 1', 'Custom 2': 'Value 2'},
     'readers': [],
     'status': 'draft',
     'status_update_time': '...T...',
     'status_updater': 'system:admin',
     'tags': ['Tag 1', 'Tag 2'],
     'title': 'Test document',
     'update_mode': 'private',
     'updated_time': None,
     'updater': 'system:admin',
     'version': 1}

    >>> from pyams_utils.traversing import get_parent
    >>> from pyams_zfiles.interfaces import IDocumentFolder
    >>> folder = get_parent(document, IDocumentFolder)
    >>> folder
    <pyams_zfiles.folder.DocumentFolder object at 0x...>


Updating document
-----------------

    >>> properties = {
    ...     'status': 'published'
    ... }
    >>> document = utility.update_document(oid, properties=properties, request=request)
    >>> transaction.commit()

    >>> document.oid == oid
    True

    >>> pprint(document.to_json())
    {'access_mode': 'private',
     'api': 'http://example.com/api/zfiles/rest/ZF:...',
     'application_name': 'PyAMS test application',
     'content_type': 'text/plain',
     'created_time': None,
     'creator': 'system:admin',
     'filename': 'test.txt',
     'filesize': 27,
     'hash': '04b251e9e34e6d58efde44ebafd7c769a630cdcf633c134af1e8b247100b6e774d3dccfe236e2b7ef96fbe829b3896128b201e0aa1079f99bc7ef532d58860aa',
     'href': 'http://example.com/++etc++site/ZFiles/.../.../ZF:.../++versions++/1/++attr++data',
     'managers': [],
     'oid': 'ZF:...',
     'owner': 'admin:admin',
     'properties': {'Custom 1': 'Value 1', 'Custom 2': 'Value 2'},
     'readers': [],
     'status': 'published',
     'status_update_time': '...T...',
     'status_updater': 'system:admin',
     'tags': ['Tag 1', 'Tag 2'],
     'title': 'Test document',
     'update_mode': 'private',
     'updated_time': None,
     'updater': 'system:admin',
     'version': 1}


Updating document content
-------------------------

    >>> data = b"New file content"
    >>> properties = {
    ...     'filename': 'modified.txt'
    ... }
    >>> document = utility.update_document(oid, data=data, properties=properties, request=request)
    >>> transaction.commit()

    >>> document.oid == oid
    True

    >>> pprint(document.to_json())
    {'access_mode': 'private',
     'api': 'http://example.com/api/zfiles/rest/ZF:...',
     'application_name': 'PyAMS test application',
     'content_type': 'text/plain',
     'created_time': None,
     'creator': 'system:admin',
     'filename': 'modified.txt',
     'filesize': 16,
     'hash': 'a4cf7ce7d511c577ea9d450e11cc7fa17d571f883c0a182b308242197b784c9f5645257b6873776a3f845a5fa9d84935685de602b47faedc9f837ddb169ad678',
     'href': 'http://example.com/++etc++site/ZFiles/.../.../ZF:.../++versions++/2/++attr++data',
     'managers': [],
     'oid': 'ZF:...',
     'owner': 'admin:admin',
     'properties': {'Custom 1': 'Value 1', 'Custom 2': 'Value 2'},
     'readers': [],
     'status': 'draft',
     'status_update_time': '...T...',
     'status_updater': 'system:admin',
     'tags': ['Tag 1', 'Tag 2'],
     'title': 'Test document',
     'update_mode': 'private',
     'updated_time': None,
     'updater': 'system:admin',
     'version': 2}


Searching documents
-------------------

Except if requested explicitly, documents serach only return published documents:

    >>> documents = utility.find_documents({'application_name': 'PyAMS test application'})
    >>> pprint(list(map(lambda x: x.to_json().get('version'), documents)))
    [1]


Deleting documents
------------------

    >>> document = utility.delete_document(oid, request=None)
    >>> list(folder.keys())
    []


Tests cleanup:

    >>> set_local_registry(None)
    >>> tearDown()
