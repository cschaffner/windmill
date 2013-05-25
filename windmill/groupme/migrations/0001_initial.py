# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Message'
        db.create_table('groupme_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('msg_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('group_id', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('groupme', ['Message'])


    def backwards(self, orm):
        # Deleting model 'Message'
        db.delete_table('groupme_message')


    models = {
        'groupme.message': {
            'Meta': {'object_name': 'Message'},
            'created_at': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'group_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'msg_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['groupme']