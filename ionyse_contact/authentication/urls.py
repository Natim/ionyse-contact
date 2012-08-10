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

from django.conf.urls.defaults import *
from ionyse_contact.authentication.forms import AuthenticationForm


urlpatterns = patterns('',
                       url(r'^login/$',
                           'django.contrib.auth.views.login', 
                           {'template_name': 'authentication/login_form.html', 
                            'authentication_form': AuthenticationForm}, 
                           name="auth_login"),

                       url(r'^logout/$', 
                           'django.contrib.auth.views.logout_then_login', 
                           name="auth_logout"),

                       url(r'^password/change/$', 
                           'django.contrib.auth.views.password_change', 
                           {'template_name': 'authentication/password_form.html'}, 
                           name="auth_password_change"),

                       url(r'^password/changed/$', 
                           'django.contrib.auth.views.password_change_done', 
                           {'template_name': 'authentication/password_changed.html'}, 
                           name="auth_password_changed"),

                       url(r'^password/reinit/$', 
                           'django.contrib.auth.views.password_reset',
                           {'template_name': 'authentication/password_reset_form.html'}),
                       )
