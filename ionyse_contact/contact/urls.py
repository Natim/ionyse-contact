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
from django.contrib.auth.decorators import login_required

from ionyse_contact.contact.models import Group, Contact
from ionyse_contact.utils import (get_default_model_url,
                                  get_default_app_url)

from ionyse_contact.contact.views import (add_contact_in_group, 
                                          add_contacts_in_group, 
                                          remove_contact_from_group,
                                          generate_script_sieve)


urlpatterns = get_default_app_url('contact')
urlpatterns += get_default_model_url(Group)
urlpatterns += get_default_model_url(Contact)
urlpatterns += patterns('',
                        # Add in group
                        url(r'^contact-group/add/(?P<group_id>\d+)/(?P<contact_id>\d+)/$',
                            login_required(add_contact_in_group),
                            name="contact-group-add"),
                        # Remove from group
                        url(r'^contact-group/delete/(?P<group_id>\d+)/(?P<contact_id>\d+)/$',
                            login_required(remove_contact_from_group),
                            name="contact-group-delete"),

                        # Add contacts in group
                        url(r'^contact-group/add/(?P<group_id>\d+)/$',
                            login_required(add_contacts_in_group),
                            name="contact-batch"),

                        # Add contacts in group
                        url(r'^contact-group/sieve/(?P<group_id>\d+)/$',
                            login_required(generate_script_sieve),
                            name="contact-sieve"),
                        )
