# Generated by Django 5.0.4 on 2024-05-06 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('News_Articles', '0006_alter_category_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='author',
            new_name='Uni_author',
        ),
    ]
