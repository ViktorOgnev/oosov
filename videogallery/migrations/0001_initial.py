# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Video'
        db.create_table(u'videogallery_video', (
            ('excerpt_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('embed_url', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('description_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('excerpt', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('thumb_url', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'videogallery', ['Video'])

        # Adding M2M table for field locations on 'Video'
        db.create_table(u'videogallery_video_locations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('video', models.ForeignKey(orm[u'videogallery.video'], null=False)),
            ('location', models.ForeignKey(orm[u'coltrane.location'], null=False))
        ))
        db.create_unique(u'videogallery_video_locations', ['video_id', 'location_id'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Video'
        db.delete_table(u'videogallery_video')

        # Removing M2M table for field locations on 'Video'
        db.delete_table('videogallery_video_locations')
    
    
    models = {
        u'coltrane.location': {
            'Meta': {'object_name': 'Location'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'videogallery.video': {
            'Meta': {'object_name': 'Video'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'embed_url': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'excerpt': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'excerpt_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'locations': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['coltrane.Location']", 'symmetrical': 'False'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'thumb_url': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }
    
    complete_apps = ['videogallery']
