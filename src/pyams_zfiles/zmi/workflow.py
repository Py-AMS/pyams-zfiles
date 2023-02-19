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

"""PyAMS_zfiles.zmi.workflow module

This module defines ZFiles workflow management views.
"""

from pyams_form.ajax import ajax_form_config
from pyams_layer.interfaces import IPyAMSLayer
from pyams_utils.registry import get_utility
from pyams_workflow.zmi.transition import WorkflowContentTransitionForm
from pyams_zfiles.interfaces import IDocumentContainer, IDocumentVersion, \
    MANAGE_DOCUMENT_PERMISSION

__docformat__ = 'restructuredtext'

from pyams_zmi.form import BaseFormMixin


class BaseWorkflowForm(WorkflowContentTransitionForm):
    """Base workflow form"""

    @property
    def title(self):
        """Title getter"""
        return super(WorkflowContentTransitionForm, self).title


@ajax_form_config(name='wf-publish.html',  # pylint: disable=abstract-method
                  context=IDocumentVersion, layer=IPyAMSLayer,
                  permission=MANAGE_DOCUMENT_PERMISSION)
class DocumentVersionPublishForm(BaseWorkflowForm):
    """Document version publish form"""


@ajax_form_config(name='wf-archive.html',  # pylint: disable=abstract-method
                  context=IDocumentVersion, layer=IPyAMSLayer,
                  permission=MANAGE_DOCUMENT_PERMISSION)
class DocumentVersionArchiveForm(BaseWorkflowForm):
    """Document version archive form"""


@ajax_form_config(name='wf-clone.html',  # pylint: disable=abstract-method
                  context=IDocumentVersion, layer=IPyAMSLayer,
                  permission=MANAGE_DOCUMENT_PERMISSION)
class DocumentVersionCloneForm(BaseWorkflowForm):
    """Document version clone form"""


@ajax_form_config(name='wf-delete.html',  # pylint: disable=abstract-method
                  context=IDocumentVersion, layer=IPyAMSLayer,
                  permission=MANAGE_DOCUMENT_PERMISSION)
class DocumentVersionDeleteForm(BaseWorkflowForm):
    """Document version delete form"""

    @property
    def deleted_target(self):
        """Redirect target when current content is deleted"""
        return get_utility(IDocumentContainer)
