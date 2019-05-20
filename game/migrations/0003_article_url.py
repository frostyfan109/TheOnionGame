# Generated by Django 2.2.1 on 2019-05-17 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20190517_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='url',
            field=models.URLField(default='', help_text='URL of the article (may be left empty to signify that it lacks one)'),
        ),
    ]
