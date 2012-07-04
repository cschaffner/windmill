# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Game.team_2_name'
        db.delete_column('powerrank_game', 'team_2_name')

        # Deleting field 'Game.team_1_id'
        db.delete_column('powerrank_game', 'team_1_id')

        # Deleting field 'Game.team_2_id'
        db.delete_column('powerrank_game', 'team_2_id')

        # Deleting field 'Game.team_1_name'
        db.delete_column('powerrank_game', 'team_1_name')

        # Adding field 'Game.team_1'
        db.add_column('powerrank_game', 'team_1',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='game_team1', null=True, to=orm['powerrank.Team']),
                      keep_default=False)

        # Adding field 'Game.team_2'
        db.add_column('powerrank_game', 'team_2',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='game_team2', null=True, to=orm['powerrank.Team']),
                      keep_default=False)

        # Deleting field 'Team.tournament'
        db.delete_column('powerrank_team', 'tournament_id')

        # Deleting field 'Team.nr_received'
        db.delete_column('powerrank_team', 'nr_received')

        # Deleting field 'Team.nr_given'
        db.delete_column('powerrank_team', 'nr_given')

        # Deleting field 'Team.received'
        db.delete_column('powerrank_team', 'received')

        # Deleting field 'Team.given'
        db.delete_column('powerrank_team', 'given')

        # Deleting field 'Team.avg_received'
        db.delete_column('powerrank_team', 'avg_received')

        # Deleting field 'Team.avg_given'
        db.delete_column('powerrank_team', 'avg_given')


    def backwards(self, orm):
        # Adding field 'Game.team_2_name'
        db.add_column('powerrank_game', 'team_2_name',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Game.team_1_id'
        db.add_column('powerrank_game', 'team_1_id',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Game.team_2_id'
        db.add_column('powerrank_game', 'team_2_id',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Game.team_1_name'
        db.add_column('powerrank_game', 'team_1_name',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Game.team_1'
        db.delete_column('powerrank_game', 'team_1_id')

        # Deleting field 'Game.team_2'
        db.delete_column('powerrank_game', 'team_2_id')

        # Adding field 'Team.tournament'
        db.add_column('powerrank_team', 'tournament',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['powerrank.Tournament'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Team.nr_received'
        db.add_column('powerrank_team', 'nr_received',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Team.nr_given'
        db.add_column('powerrank_team', 'nr_given',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Team.received'
        db.add_column('powerrank_team', 'received',
                      self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default=0, max_length=100),
                      keep_default=False)

        # Adding field 'Team.given'
        db.add_column('powerrank_team', 'given',
                      self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default=0, max_length=100),
                      keep_default=False)

        # Adding field 'Team.avg_received'
        db.add_column('powerrank_team', 'avg_received',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True),
                      keep_default=False)

        # Adding field 'Team.avg_given'
        db.add_column('powerrank_team', 'avg_given',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True),
                      keep_default=False)


    models = {
        'powerrank.game': {
            'Meta': {'object_name': 'Game'},
            'field': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lv_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['powerrank.Round']", 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'team_1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'game_team1'", 'null': 'True', 'to': "orm['powerrank.Team']"}),
            'team_1_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'team_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'game_team2'", 'null': 'True', 'to': "orm['powerrank.Team']"}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lv_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rounds': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['powerrank.Round']", 'through': "orm['powerrank.Standing']", 'symmetrical': 'False'})
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