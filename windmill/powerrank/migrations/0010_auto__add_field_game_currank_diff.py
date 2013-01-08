# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Game.currank_diff'
        db.add_column('powerrank_game', 'currank_diff',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Game.currank_diff'
        db.delete_column('powerrank_game', 'currank_diff')


    models = {
        'powerrank.game': {
            'Meta': {'object_name': 'Game'},
            'currank_diff': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lv_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pred_margin_current': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '4', 'blank': 'True'}),
            'pred_margin_overall': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '4', 'blank': 'True'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['powerrank.Round']", 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'team_1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'game_team1'", 'null': 'True', 'to': "orm['powerrank.Team']"}),
            'team_1_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'team_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'game_team2'", 'null': 'True', 'to': "orm['powerrank.Team']"}),
            'team_2_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'upset_current': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '4', 'blank': 'True'}),
            'upset_overall': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '4', 'blank': 'True'})
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
            'chris_rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'losses': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mark_rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'power_rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['powerrank.Round']"}),
            'strength': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '4', 'blank': 'True'}),
            'swiss_opponent_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'swiss_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['powerrank.Team']"}),
            'wins': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'powerrank.team': {
            'Meta': {'object_name': 'Team'},
            'final_rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lv_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rounds': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['powerrank.Round']", 'through': "orm['powerrank.Standing']", 'symmetrical': 'False'}),
            'seed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
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