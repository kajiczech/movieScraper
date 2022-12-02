# Generated by Django 4.1.3 on 2022-12-02 20:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('unicode_name', models.CharField(help_text='Unaccented lowercase word for searching', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('unicode_name', models.CharField(help_text='Unaccented lowercase word for searching', max_length=255)),
                ('actors', models.ManyToManyField(related_name='movies', to='movies.actor')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
