# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Inspection'
        db.create_table(u'inspection_inspection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('inspection_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('inspection_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('risk_category', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('inspection_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('inspection_url', self.gf('django.db.models.fields.TextField')()),
            ('critical', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('noncritical', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('critical_corrected_on_site', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('noncritical_corrected_on_site', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('restaurant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['restaurant.Restaurant'], null=True, blank=True)),
        ))
        db.send_create_signal(u'inspection', ['Inspection'])

        # Adding model 'Observation'
        db.create_table(u'inspection_observation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('correction', self.gf('django.db.models.fields.TextField')()),
            ('observation', self.gf('django.db.models.fields.TextField')()),
            ('dcmr', self.gf('django.db.models.fields.TextField')()),
            ('inspection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inspection.Inspection'], null=True, blank=True)),
        ))
        db.send_create_signal(u'inspection', ['Observation'])


    def backwards(self, orm):
        # Deleting model 'Inspection'
        db.delete_table(u'inspection_inspection')

        # Deleting model 'Observation'
        db.delete_table(u'inspection_observation')


    models = {
        u'inspection.inspection': {
            'Meta': {'object_name': 'Inspection'},
            'critical': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'critical_corrected_on_site': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inspection_date': ('django.db.models.fields.DateTimeField', [], {}),
            'inspection_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'inspection_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'inspection_url': ('django.db.models.fields.TextField', [], {}),
            'noncritical': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'noncritical_corrected_on_site': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['restaurant.Restaurant']", 'null': 'True', 'blank': 'True'}),
            'risk_category': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'inspection.observation': {
            'Meta': {'object_name': 'Observation'},
            'correction': ('django.db.models.fields.TextField', [], {}),
            'dcmr': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inspection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inspection.Inspection']", 'null': 'True', 'blank': 'True'}),
            'observation': ('django.db.models.fields.TextField', [], {})
        },
        u'restaurant.restaurant': {
            'Meta': {'object_name': 'Restaurant'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inspection_url': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'permit_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'quadrant': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'restaurant_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ward': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        }
    }

    complete_apps = ['inspection']