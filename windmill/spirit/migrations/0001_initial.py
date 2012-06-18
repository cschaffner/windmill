# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tournament'
        db.create_table('spirit_tournament', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('l_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lv_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('spirit', ['Tournament'])

        # Adding model 'Game'
        db.create_table('spirit_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('l_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lv_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('team_1_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('team_2_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('team_1_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('team_2_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spirit.Tournament'], null=True, blank=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('team_1_spirit', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('team_2_spirit', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('spirit', ['Game'])

        # Adding model 'Team'
        db.create_table('spirit_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('l_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lv_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spirit.Tournament'], null=True, blank=True)),
            ('received', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=30)),
            ('given', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=30)),
            ('avg_received', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('avg_given', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('nr_received', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('nr_given', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('spirit', ['Team'])


    def backwards(self, orm):
        # Deleting model 'Tournament'
        db.delete_table('spirit_tournament')

        # Deleting model 'Game'
        db.delete_table('spirit_game')

        # Deleting model 'Team'
        db.delete_table('spirit_team')


    models = {
        'spirit.game': {
            'Meta': {'object_name': 'Game'},
            'field': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lv_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'team_1_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'team_1_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'team_1_spirit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'team_2_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'team_2_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'team_2_spirit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spirit.Tournament']", 'null': 'True', 'blank': 'True'})
        },
        'spirit.team': {
            'Meta': {'object_name': 'Team'},
            'avg_given': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'avg_received': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'given': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lv_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nr_given': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nr_received': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'received': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '30'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spirit.Tournament']", 'null': 'True', 'blank': 'True'})
        },
        'spirit.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lv_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['spirit']