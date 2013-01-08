# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Round.round_number'
        db.add_column('powerrank_round', 'round_number',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Game.tournament'
        db.delete_column('powerrank_game', 'tournament_id')

        # Adding field 'Game.round'
        db.add_column('powerrank_game', 'round',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['powerrank.Round'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Round.round_number'
        db.delete_column('powerrank_round', 'round_number')

        # Adding field 'Game.tournament'
        db.add_column('powerrank_game', 'tournament',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['powerrank.Tournament'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Game.round'
        db.delete_column('powerrank_game', 'round_id')


    models = {
        'powerrank.game': {
            'Meta': {'object_name': 'Game'},
            'field': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lv_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['powerrank.Round']", 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'team_1_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'team_1_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'team_1_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'team_2_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'team_2_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'team_2_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'powerrank.round': {
            'Meta': {'object_name': 'Round'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lv_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'round_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['powerrank.Tournament']", 'null': 'True', 'blank': 'True'})
        },
        'powerrank.standing': {
            'Meta': {'object_name': 'Standing'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'losses': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'power_rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['powerrank.Round']"}),
            'strength': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '4', 'blank': 'True'}),
            'swiss_rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'swiss_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['powerrank.Team']"}),
            'wins': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'powerrank.team': {
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
            'rounds': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['powerrank.Round']", 'through': "orm['powerrank.Standing']", 'symmetrical': 'False'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['powerrank.Tournament']", 'null': 'True', 'blank': 'True'})
        },
        'powerrank.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lv_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['powerrank']