# -*- coding: utf-8 -*-
# Copyright (c) 2012 HUBSCHER Rémy
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.auth.decorators import login_required

from ionyse_contact.views import (CTDashboardView, CTListView, CTDetailView,
                                  CTCreationView, CTUpdateView, CTDeleteView)

def get_default_app_url(app_label):
    
    urlpatterns = patterns('',
                           url('^$',
                               login_required(CTDashboardView.as_view(app_label=app_label)),
                               name='%s-dashboard' % app_label))
    return urlpatterns


def get_default_model_url(model, form_class=None,
                          url_name=None,
                          prefix_pattern='',
                          list_view=CTListView,
                          detail_view=CTDetailView,
                          creation_view=CTCreationView,
                          update_view=CTUpdateView,
                          delete_view=CTDeleteView):

    module_name = model._meta.module_name

    # Get default FormClass for model
    # e.g. : CityForm for model City.
    if not form_class:
        package = ('.').join(model.__module__.split('.')[:-1])
        forms = __import__('%s.forms' % package, fromlist=[''])
        form_class = getattr(forms, '%sForm' % model.__name__)

    # Get default URL name
    if not url_name:
        url_name = model._meta.module_name

    # Generation of urlpatterns
    urlpatterns = patterns('')
    if list_view:
        urlpatterns += patterns('',
                               # List View
                               url(r'^%s%s/$' % (prefix_pattern, module_name),
                                   login_required(list_view.as_view(model=model)),
                                   name='%s-list' % module_name))
    if detail_view:
        urlpatterns += patterns('',
                               # Detail View
                               url(r'^%s%s/(?P<pk>\d+)/$' % (prefix_pattern, module_name),
                                   login_required(detail_view.as_view(model=model)),
                                   name="%s-detail" % module_name))
    if creation_view:
        urlpatterns += patterns('',
                               # Add View
                               url(r'^%s%s/add/$' % (prefix_pattern, module_name),
                                   login_required(creation_view.as_view(model=model,
                                                                        form_class=form_class)),
                                   name="%s-add" % module_name))
    if update_view:
        urlpatterns += patterns('',
                               # Edit View
                               url(r'^%s%s/(?P<pk>\d+)/edit/$' % (prefix_pattern, module_name),
                                   login_required(update_view.as_view(model=model,
                                                                      form_class=form_class)),
                                   name="%s-edit" % module_name))
    if delete_view:
        urlpatterns += patterns('',
                               # Delete View
                               url(r'^%s%s/(?P<pk>\d+)/delete/$' % (prefix_pattern, module_name),
                                   login_required(delete_view.as_view(model=model)),
                                   name="%s-delete" % module_name))

    return urlpatterns
