# Generated by Django 5.1.6 on 2025-02-13 00:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0007_rename_save_saveitem_saves'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='saveitem',
            unique_together={('post', 'saves')},
        ),
    ]
