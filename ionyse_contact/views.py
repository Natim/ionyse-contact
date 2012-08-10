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

import os.path

from django.core.urlresolvers import reverse, NoReverseMatch
from django.views.generic import (TemplateView, ListView, 
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)

# --------------------------
# TOOLS
# --------------------------

def get_default_list_view(model):
    try:
        # Try to reverse the default url, like 'model-list'
        cancel_url = model._meta.module_name + '-list'
        return reverse(cancel_url)
    except NoReverseMatch:
        pass
    return reverse('dashboard')


def get_global_context_data(model=None, app_label=None):
    infos = {}
    if model:
        app_label = model._meta.app_label
        infos['verbose_name'] = model._meta.verbose_name
        infos['verbose_name_plural'] = model._meta.verbose_name_plural
    if app_label:
        infos['app_menu_file'] = os.path.join(app_label, 'menu.html')
        infos['app_label'] = app_label
    return infos


# --------------------------
# CT MIXINS
# --------------------------

class CTTemplateMixin(object):

    def get_template_names(self):
        module_name = self.model._meta.module_name
        app_label = self.model._meta.app_label
        base_template_name = u'model%s.html' % self.template_name_suffix
        template_list = []

        if self.template_name:
            template_list.append(template_name)
        # Module template list
        template_list.append(os.path.join(app_label, module_name, base_template_name))
        # App template list
        template_list.append(os.path.join(app_label, base_template_name))
        # Default template list
        template_list.append(base_template_name)
        return template_list


# --------------------------
# CT GENERIC VIEWS
# --------------------------

class CTDashboardView(TemplateView):
    
    app_label = None

    def get_template_names(self):
        template_list = []
        if self.template_name:
            template_list.append(self.template_name)
        if self.app_label:
            template_list.append(os.path.join(self.app_label, 'dashboard.html'))
            template_list.append('base_dashboard.html')
        template_list.append('dashboard.html')
        return template_list

    def get_context_data(self, **kwargs):
        context = super(CTDashboardView, self).get_context_data(**kwargs)
        # Add global template data
        global_data = get_global_context_data(app_label=self.app_label)
        context.update(global_data)
        return context


class CTListView(CTTemplateMixin, ListView):
    template_name = None

    def get_context_data(self, **kwargs):
        context = super(CTListView, self).get_context_data(**kwargs)
        # Add global template data
        global_data = get_global_context_data(self.model)
        context.update(global_data)
        return context


class CTDetailView(CTTemplateMixin, DetailView):
    
    url_edit_action = None
    url_delete_action = None
    edit_action = True
    delete_action = True

    def get_extra_actions(self):
        return None

    def get_url_edit_action(self):
        if self.url_edit_action:
            return self.url_edit_action
        else:
            if self.edit_action:
                module_name = self.model._meta.module_name
                return reverse('%s-edit' % module_name, args=[self.object.pk])
        return None

    def get_url_delete_action(self):
        if self.url_delete_action:
            return self.url_delete_action
        else:
            if self.delete_action:
                module_name = self.model._meta.module_name
                return reverse('%s-delete' % module_name, args=[self.object.pk])
        return None
                
                
    def get_context_data(self, **kwargs):
        context = super(CTDetailView, self)\
            .get_context_data(**kwargs)
        # Add the objects list
        context['object_list'] = self.model.objects.all()
        # Add global template data
        global_data = get_global_context_data(self.model)
        context.update(global_data)
        # Add url actions
        context['url_edit_action'] = self.get_url_edit_action()
        context['url_delete_action'] = self.get_url_delete_action()
        context['extra_actions'] = self.get_extra_actions()
        return context


class CTCreationView(CTTemplateMixin, CreateView):

    cancel_url = None

    def get_cancel_url(self):
        if self.cancel_url:
            return reverse(self.cancel_url)
        return get_default_list_view(self.model)

    def get_context_data(self, **kwargs):
        context = super(CTCreationView, self)\
            .get_context_data(**kwargs)
        # Add the default cancel url for the form
        context['cancel_url'] = self.get_cancel_url()
        # Add global template data
        global_data = get_global_context_data(self.model)
        context.update(global_data)
        return context


class CTUpdateView(CTTemplateMixin, UpdateView):

    def get_context_data(self, **kwargs):
        context = super(CTUpdateView, self)\
            .get_context_data(**kwargs)
        # Add global template data
        global_data = get_global_context_data(self.model)
        context.update(global_data)
        return context


class CTDeleteView(CTTemplateMixin, DeleteView):
    
    def get_success_url(self):
        if self.success_url:
            return reverse(self.success_url)
        return get_default_list_view(self.model)

    def get_context_data(self, **kwargs):
        context = super(CTDeleteView, self)\
            .get_context_data(**kwargs)
        # Add global template data
        global_data = get_global_context_data(self.model)
        context.update(global_data)
        return context
