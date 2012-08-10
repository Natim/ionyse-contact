# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Group.always_data_id'
        db.add_column('contact_group', 'always_data_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Group.always_data_id'
        db.delete_column('contact_group', 'always_data_id')


    models = {
        'contact.contact': {
            'Meta': {'ordering': "['email']", 'object_name': 'Contact'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'group': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'contacts'", 'symmetrical': 'False', 'to': "orm['contact.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'contact.group': {
            'Meta': {'ordering': "['name']", 'object_name': 'Group'},
            'always_data_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['contact']
