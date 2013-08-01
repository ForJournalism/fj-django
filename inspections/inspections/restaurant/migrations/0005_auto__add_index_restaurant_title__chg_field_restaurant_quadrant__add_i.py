# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Restaurant', fields ['title']
        db.create_index(u'restaurant_restaurant', ['title'])


        # Changing field 'Restaurant.quadrant'
        db.alter_column(u'restaurant_restaurant', 'quadrant', self.gf('django.db.models.fields.CharField')(default=None, max_length=2))
        # Adding index on 'Restaurant', fields ['quadrant']
        db.create_index(u'restaurant_restaurant', ['quadrant'])


    def backwards(self, orm):
        # Removing index on 'Restaurant', fields ['quadrant']
        db.delete_index(u'restaurant_restaurant', ['quadrant'])

        # Removing index on 'Restaurant', fields ['title']
        db.delete_index(u'restaurant_restaurant', ['title'])


        # Changing field 'Restaurant.quadrant'
        db.alter_column(u'restaurant_restaurant', 'quadrant', self.gf('django.db.models.fields.CharField')(max_length=2, null=True))

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
            'quadrant': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'restaurant_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'ward': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        }
    }

    complete_apps = ['restaurant']