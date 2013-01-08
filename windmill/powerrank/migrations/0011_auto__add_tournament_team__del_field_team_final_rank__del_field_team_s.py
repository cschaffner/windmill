# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tournament_Team'
        db.create_table('powerrank_tournament_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['powerrank.Tournament'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['powerrank.Team'])),
            ('seed', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('final_rank', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('powerrank', ['Tournament_Team'])

        # Deleting field 'Team.final_rank'
        db.delete_column('powerrank_team', 'final_rank')

        # Deleting field 'Team.seed'
        db.delete_column('powerrank_team', 'seed')


    def backwards(self, orm):
        # Deleting model 'Tournament_Team'
        db.delete_table('powerrank_tournament_team')

        # Adding field 'Team.final_rank'
        db.add_column('powerrank_team', 'final_rank',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Team.seed'
        db.add_column('powerrank_team', 'seed',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lv_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rounds': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['powerrank.Round']", 'through': "orm['powerrank.Standing']", 'symmetrical': 'False'}),
            'tournaments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['powerrank.Tournament']", 'through': "orm['powerrank.Tournament_Team']", 'symmetrical': 'False'})
        },
        'powerrank.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lv_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'powerrank.tournament_team': {
            'Meta': {'object_name': 'Tournament_Team'},
            'final_rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['powerrank.Team']"}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['powerrank.Tournament']"})
        }
    }

    complete_apps = ['powerrank']