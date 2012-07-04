# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tournament'
        db.create_table('powerrank_tournament', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('l_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lv_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('powerrank', ['Tournament'])

        # Adding model 'Game'
        db.create_table('powerrank_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('l_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lv_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('team_1_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('team_2_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('team_1_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('team_2_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('team_1_score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('team_2_score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['powerrank.Tournament'], null=True, blank=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('powerrank', ['Game'])

        # Adding model 'Team'
        db.create_table('powerrank_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('l_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lv_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['powerrank.Tournament'], null=True, blank=True)),
            ('received', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('given', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('avg_received', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('avg_given', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('nr_received', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('nr_given', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('powerrank', ['Team'])

        # Adding model 'Round'
        db.create_table('powerrank_round', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('l_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lv_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['powerrank.Tournament'], null=True, blank=True)),
        ))
        db.send_create_signal('powerrank', ['Round'])

        # Adding model 'Standing'
        db.create_table('powerrank_standing', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('round', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['powerrank.Round'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['powerrank.Team'])),
            ('wins', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('losses', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('swiss_score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('swiss_rank', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('power_rank', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('strength', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=4, blank=True)),
        ))
        db.send_create_signal('powerrank', ['Standing'])


    def backwards(self, orm):
        # Deleting model 'Tournament'
        db.delete_table('powerrank_tournament')

        # Deleting model 'Game'
        db.delete_table('powerrank_game')

        # Deleting model 'Team'
        db.delete_table('powerrank_team')

        # Deleting model 'Round'
        db.delete_table('powerrank_round')

        # Deleting model 'Standing'
        db.delete_table('powerrank_standing')


    models = {
        'powerrank.game': {
            'Meta': {'object_name': 'Game'},
            'field': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lv_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'team_1_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'team_1_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'team_1_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'team_2_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'team_2_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'team_2_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['powerrank.Tournament']", 'null': 'True', 'blank': 'True'})
        },
        'powerrank.round': {
            'Meta': {'object_name': 'Round'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lv_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['powerrank.Team']", 'through': "orm['powerrank.Standing']", 'symmetrical': 'False'}),
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