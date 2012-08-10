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

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

class Group(models.Model):
    name = models.CharField(_(u"name"), max_length=100)
    email = models.EmailField(_(u"email"), blank=True)
    always_data_id = models.PositiveIntegerField(_(u'Email id on AlwaysData'), null=True)

    def __unicode__(self):
        return u'"%s" <%s>' % (self.name, self.email)

    def get_absolute_url(self):
        return reverse('group-detail', args=[self.pk])

    class Meta:
        verbose_name = _(u"group")
        verbose_name_plural = _(u"groups")
        ordering = ['name']


class Contact(models.Model):
    name = models.CharField(_(u"name"), max_length=100, blank=True)
    email = models.EmailField(_(u"email"), unique=True)
    group = models.ManyToManyField(Group, related_name="contacts")

    def __unicode__(self):
        if self.name:
            return u'"%s" <%s>' % (self.name, self.email)
        else:
            return '%s' % self.email

    def get_absolute_url(self):
        return reverse('contact-detail', args=[self.pk])

    class Meta:
        verbose_name = _(u"contact")
        verbose_name_plural = _(u"contacts")
        ordering = ['email']
