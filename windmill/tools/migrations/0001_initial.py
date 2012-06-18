# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tournament'
        db.create_table('tools_tournament', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('l_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lv_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('tools', ['Tournament'])

        # Adding model 'Team'
        db.create_table('tools_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('l_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lv_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tools.Tournament'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('seed', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('team_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('sec_contact_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('sec_contact_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('mobile1', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('mobile2', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('mobile3', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('mobile4', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('mobile5', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal('tools', ['Team'])


    def backwards(self, orm):
        # Deleting model 'Tournament'
        db.delete_table('tools_tournament')

        # Deleting model 'Team'
        db.delete_table('tools_team')


    models = {
        'tools.team': {
            'Meta': {'object_name': 'Team'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lv_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mobile1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'mobile2': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'mobile3': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'mobile4': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'mobile5': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sec_contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'sec_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'seed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'team_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tools.Tournament']", 'null': 'True', 'blank': 'True'})
        },
        'tools.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lv_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['tools']