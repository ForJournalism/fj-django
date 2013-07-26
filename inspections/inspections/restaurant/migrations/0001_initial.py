# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Restaurant'
        db.create_table(u'restaurant_restaurant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('permit_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('quadrant', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True)),
            ('ward', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('restaurant_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('inspection_url', self.gf('django.db.models.fields.TextField')(null=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
        ))
        db.send_create_signal(u'restaurant', ['Restaurant'])


    def backwards(self, orm):
        # Deleting model 'Restaurant'
        db.delete_table(u'restaurant_restaurant')


    models = {
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

    complete_apps = ['restaurant']