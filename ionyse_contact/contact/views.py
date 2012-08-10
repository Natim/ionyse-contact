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

import re
import os.path

from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from ionyse_contact.views import get_global_context_data

from ionyse_contact.contact.models import Group, Contact
from ionyse_contact.contact.utils import export_sieve_configuration

EMAIL_REGEX = re.compile("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$")
PREFIXED_EMAIL_REGEX = re.compile("^(.*) <([a-zA-Z0-9._%+-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6})>$")

def validate_email(email):
    if EMAIL_REGEX.match(email) != None:
        return True
    return False

def add_contact_in_group(request, group_id, contact_id):
    group = get_object_or_404(Group, id=group_id)
    contact = get_object_or_404(Contact, id=contact_id)

    contact.group.add(group)
    messages.success(request, _(u'%(contact)s added to %(group)s' % 
                                {'contact': contact,
                                 'group': group}))

    return HttpResponseRedirect(reverse("group-detail", args=[group.pk]))


def add_contacts_in_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)


    if request.method == 'POST':
        emails = request.POST['emails'].replace(',', '\n').split('\n')
        emails = filter(None, [x.strip() for x in emails])
        valid_emails = []
        invalid_emails = []
        for email in emails:
            if validate_email(email):
                valid_emails.append(email)
            else:
                invalid_emails.append(email)

        for email in valid_emails:
            contact, create = Contact.objects.get_or_create(email=email)
            contact.group.add(group)

            messages.success(request, _(u'%(contact)s added to %(group)s' % 
                                        {'contact': contact,
                                         'group': group}))
        for email in invalid_emails:
            m = PREFIXED_EMAIL_REGEX.match(email)
            if m:
                name = m.group(1)
                email = m.group(2)

                contact, create = Contact.objects.get_or_create(email=email, defaults={'name': name})
                contact.group.add(group)

                messages.success(request, _(u'%(contact)s added to %(group)s' % 
                                            {'contact': contact,
                                             'group': group}))
            else:
                print email

        return HttpResponseRedirect(reverse("group-detail", args=[group.pk]))
    else:
        context = get_global_context_data(Group, Group._meta.app_label)
        context['object_list'] = Group.objects.all()
        context['object'] = group
        return render_to_response('contact/contact-batch.html',
                                  context,
                                  context_instance=RequestContext(request))

def remove_contact_from_group(request, group_id, contact_id):
    group = get_object_or_404(Group, id=group_id)
    contact = get_object_or_404(Contact, id=contact_id)

    contact.group.remove(group)
    messages.success(request, _(u'%(contact)s removed from %(group)s' % 
                                {'contact': contact,
                                 'group': group}))

    return HttpResponseRedirect(reverse("group-detail", args=[group.pk]))

def generate_script_sieve(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        if group.always_data_id:
            # There is always_data mail id
            from mechanize import ParseResponse, urlopen, urljoin
            response = urlopen("https://admin.alwaysdata.com/login/")
            forms = ParseResponse(response, backwards_compat=False)
            login_form = forms[0]

            if settings.DEBUG:
                print login_form

            login_form["email"] = settings.ALWAYS_DATA_ID
            login_form["password"] = settings.ALWAYS_DATA_PASSWORD
            
            response = urlopen(login_form.click())
            url = 'https://admin.alwaysdata.com/email/%d/' % group.always_data_id
            response = urlopen(url)

            forms = ParseResponse(response, backwards_compat=False)

            if settings.DEBUG:
                for form in forms:
                    print form
            try:
                email_form = forms[1]
            except IndexError:
                messages.warning(request, _(u'%(group)s is not bind to alwaysdata yet (wrong password)' % 
                                          {'group': group}))
                
                return HttpResponseRedirect(reverse("group-detail", args=[group.pk]))

            email_form['sieve_filter'] = request.POST['filter_sieve'].encode('utf-8')

            req = email_form.click()
            req.add_header("Referer", url)
            response = urlopen(req)

            messages.success(request, _(u'Alwaysdata has been updated'))

        else:
            messages.warning(request, _(u'%(group)s is not bind to alwaysdata yet' % 
                                        {'group': group}))

        return HttpResponseRedirect(reverse("group-detail", args=[group.pk]))
            
    else:
        filter_sieve = export_sieve_configuration(group.contacts.all())
        
        context = get_global_context_data(Group, Group._meta.app_label)
        context['object_list'] = Group.objects.all()
        context['object'] = group
        context['filter_sieve'] = filter_sieve
        
        return render_to_response('contact/contact-sieve.html',
                                  context,
                                  context_instance=RequestContext(request))
