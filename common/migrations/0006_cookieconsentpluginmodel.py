# Generated by Django 3.1.12 on 2021-09-29 12:56

from django.db import migrations, models
import django.db.models.deletion
import djangocms_bootstrap4.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('common', '0005_embedpluginmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='CookieConsentPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='common_cookieconsentpluginmodel', serialize=False, to='cms.cmsplugin')),
                ('tag_type', djangocms_bootstrap4.fields.TagTypeField(choices=[('div', 'div'), ('section', 'section'), ('article', 'article'), ('header', 'header'), ('footer', 'footer'), ('aside', 'aside')], default='div', help_text='Select the HTML tag to be used.', max_length=255, verbose_name='Tag type')),
                ('attributes', djangocms_bootstrap4.fields.AttributesField(blank=True, default=dict, verbose_name='attributes')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
