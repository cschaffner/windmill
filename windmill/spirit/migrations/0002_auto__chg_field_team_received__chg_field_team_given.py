# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Team.received'
        db.alter_column('spirit_team', 'received', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100))

        # Changing field 'Team.given'
        db.alter_column('spirit_team', 'given', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100))

    def backwards(self, orm):

        # Changing field 'Team.received'
        db.alter_column('spirit_team', 'received', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=30))

        # Changing field 'Team.given'
        db.alter_column('spirit_team', 'given', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=30))

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
            'given': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lv_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nr_given': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nr_received': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'received': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
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