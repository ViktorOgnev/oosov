# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'MainPageControl'
        db.create_table(u'importanciator_mainpagecontrol', (
            ('manual_mode', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sites.Site'], unique=True)),
        ))
        db.send_create_signal(u'importanciator', ['MainPageControl'])

        # Adding model 'ImportantContent'
        db.create_table(u'importanciator_importantcontent', (
            ('primary_database_identifier', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal(u'importanciator', ['ImportantContent'])

        # Adding M2M table for field locations on 'ImportantContent'
        db.create_table(u'importanciator_importantcontent_locations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('importantcontent', models.ForeignKey(orm[u'importanciator.importantcontent'], null=False)),
            ('location', models.ForeignKey(orm[u'coltrane.location'], null=False))
        ))
        db.create_unique(u'importanciator_importantcontent_locations', ['importantcontent_id', 'location_id'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'MainPageControl'
        db.delete_table(u'importanciator_mainpagecontrol')

        # Deleting model 'ImportantContent'
        db.delete_table(u'importanciator_importantcontent')

        # Removing M2M table for field locations on 'ImportantContent'
        db.delete_table('importanciator_importantcontent_locations')
    
    
    models = {
        u'coltrane.location': {
            'Meta': {'object_name': 'Location'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'importanciator.importantcontent': {
            'Meta': {'object_name': 'ImportantContent'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locations': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['coltrane.Location']", 'symmetrical': 'False'}),
            'primary_database_identifier': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'importanciator.mainpagecontrol': {
            'Meta': {'object_name': 'MainPageControl'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manual_mode': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sites.Site']", 'unique': 'True'})
        },
        u'sites.site': {
            'Meta': {'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    
    complete_apps = ['importanciator']
