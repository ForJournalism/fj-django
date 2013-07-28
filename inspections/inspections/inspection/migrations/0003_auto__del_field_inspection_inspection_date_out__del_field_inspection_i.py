# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Inspection.inspection_date_out'
        db.delete_column(u'inspection_inspection', 'inspection_date_out')

        # Deleting field 'Inspection.inspection_date_in'
        db.delete_column(u'inspection_inspection', 'inspection_date_in')

        # Adding field 'Inspection.time_in'
        db.add_column(u'inspection_inspection', 'time_in',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'Inspection.time_out'
        db.add_column(u'inspection_inspection', 'time_out',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Inspection.inspection_date_out'
        db.add_column(u'inspection_inspection', 'inspection_date_out',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'Inspection.inspection_date_in'
        db.add_column(u'inspection_inspection', 'inspection_date_in',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Deleting field 'Inspection.time_in'
        db.delete_column(u'inspection_inspection', 'time_in')

        # Deleting field 'Inspection.time_out'
        db.delete_column(u'inspection_inspection', 'time_out')


    models = {
        u'inspection.inspection': {
            'Meta': {'object_name': 'Inspection'},
            'critical': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'critical_corrected_on_site': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inspection_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'inspection_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'inspection_url': ('django.db.models.fields.TextField', [], {}),
            'noncritical': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'noncritical_corrected_on_site': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['restaurant.Restaurant']", 'null': 'True', 'blank': 'True'}),
            'risk_category': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'time_in': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'time_out': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
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
            'Meta': {'ordering': "['title']", 'object_name': 'Restaurant'},
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