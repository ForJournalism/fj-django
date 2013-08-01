# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Restaurant.observation_count'
        db.add_column(u'restaurant_restaurant', 'observation_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Restaurant.observation_count'
        db.delete_column(u'restaurant_restaurant', 'observation_count')


    models = {
        u'restaurant.restaurant': {
            'Meta': {'ordering': "['title']", 'object_name': 'Restaurant'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inspection_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'inspection_url': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'observation_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'permit_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'quadrant': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'restaurant_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ward': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        }
    }

    complete_apps = ['restaurant']