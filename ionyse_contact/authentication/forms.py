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

from django.contrib.auth.models import User
from django.contrib import auth
from django.utils.translation import ugettext_lazy as _

import floppyforms as forms

from ionyse_contact.widgets import AutofocusInput


class UserCreationForm(forms.ModelForm):
    
    username = forms.CharField(label=_(u'Login'), 
                               widget=forms.TextInput({"placeholder": _(u"Entrez un nom d'utilisateur")}))
    password1 = forms.CharField(label=_(u'Mot de passe'), 
                                widget=forms.PasswordInput({"placeholder": _(u"Entrez un mot de passe")}))
    email = forms.EmailField(label='Email', 
                             widget=forms.TextInput({"placeholder": _(u"Enter une adresse email")}))
    is_staff = forms.BooleanField(label=_(u'est administrateur'), required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'email', 'is_staff')

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        else:
            raise forms.ValidationError(_(u"Ce nom d'utilisateur n'est pas disponible"))
        
    def clean_email(self):
        "Check the email domain for MX DNS record"
        email = self.cleaned_data['email']
        user, domain = email.split('@')
        # # Checking if the domain contains a MX record
        # try:
        #     answers = dns.resolver.query(domain, 'MX')
        # except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        #     raise forms.ValidationError(_(u"Emails from this domain are not "
        #                                   u"accepted"))
        # else:
        return email

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        if self.cleaned_data["password1"].strip() != '':
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class UserForm(UserCreationForm):

    password1 = forms.CharField(label=_(u'Mot de passe'),
                                required=False,
                                widget=forms.PasswordInput({ "placeholder": _(u"Entrez un mot de passe")}))
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'email', 'is_staff')

    def clean_username(self):
        username = self.cleaned_data['username']

        if username != self.instance.username:
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                return username
            else:
                raise forms.ValidationError(_(u"Ce nom d'utilisateur n'est pas disponible"))
        else:
            return username


class AuthenticationForm(auth.forms.AuthenticationForm):

    username = forms.CharField(label=_("Username"),
                               max_length=30,
                               widget=AutofocusInput({"placeholder": _(u"Entrez votre nom d'utilisateur")}))
    password = forms.CharField(label=_(u"Password"),
                               widget=forms.PasswordInput({"placeholder": _(u"Entrez votre mot de passe")}))
