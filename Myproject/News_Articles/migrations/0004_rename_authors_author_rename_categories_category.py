# Generated by Django 5.0.4 on 2024-05-05 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('News_Articles', '0003_authors_categories'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Authors',
            new_name='Author',
        ),
        migrations.RenameModel(
            old_name='Categories',
            new_name='Category',
        ),
    ]
