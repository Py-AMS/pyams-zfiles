#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_zfiles.search module

This module defines helper functions to search documents.
"""

from datetime import date

from dateutil import parser
from hypatia.query import All, Any, Comparator, Eq, Ge, Le, NotEq

from pyams_catalog.query import and_
from pyams_utils.date import date_to_datetime
from pyams_utils.timezone import gmtime


__docformat__ = 'restructuredtext'


def get_list(value):
    """Check and convert given value to a set, if required"""
    if isinstance(value, str):
        value = list(map(str.strip, value.split(';')))
    return value


def get_version(value):
    """Check given version index"""
    if value is not None:
        value = int(value)
    if value == -1:
        return None
    return value


def get_date(value):
    """Check and convert given value to a date, if required"""
    if value and isinstance(value, str):
        value = parser.parse(value)
    if value:
        if isinstance(value, date):
            value = date_to_datetime(value)
        value = gmtime(value)
    return value or None


def get_range(value):
    """Convert given value to datetime range"""
    return tuple(map(get_date, value))


class EqOrNotNull:
    """Check for not-null request"""

    def __call__(self, params, catalog, index, value):
        if value is None:
            params = and_(params,
                          NotEq(catalog[index], value))
        else:
            params = and_(params,
                          Eq(catalog[index], value))
        return params


class Range:
    """Combine dates to create a ranged request"""

    def __call__(self, params, catalog, index, value):
        if not isinstance(value, (list, tuple)):
            return params
        after, before = value
        if after:
            params = and_(params,
                          Ge(catalog[index], after))
        if before:
            params = and_(params,
                          Le(catalog[index], before))
        return params


INDEX_ARGS = {
    'oid': (get_list, Any, 'zfile_oid'),
    'version': (get_version, Eq, 'workflow_version'),
    'title': (str.strip, Eq, 'zfile_title'),
    'application_name': (str.strip, Eq, 'zfile_application'),
    'hash': (str.strip, Eq, 'zfile_hash'),
    'tags': (get_list, All, 'zfile_tags'),
    'status': (get_list, Any, 'workflow_state'),
    'creator': (get_list, Any, 'zfile_creator'),
    'created_date': (get_range, Range, 'created_date'),
    'owner': (get_list, Any, 'zfile_owner'),
    'updater': (get_list, Any, 'zfile_updater'),
    'updated_date': (get_range, Range, 'modified_date'),
    'status_updater': (get_list, Any, 'workflow_principal'),
    'status_update_date': (get_range, Range, 'workflow_date')
}


def make_query(catalog, params):
    """Make query from input parameters"""
    query = None
    for key, value in params.items():
        args = INDEX_ARGS.get(key)
        if args is None:
            continue
        if value == {'--NOVALUE--'}:
            continue
        converter, operator, index = args
        if (value is not None) and (converter is not None):
            value = converter(value)
        if issubclass(operator, Comparator):
            if value is not None:
                query = and_(query, operator(catalog[index], value))  # pylint: disable=not-callable
        else:
            query = operator()(query, catalog, index, value)  # pylint: disable=not-callable
    return query
