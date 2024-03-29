# Generated by Django 4.1.4 on 2023-01-04 22:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('video_id', models.CharField(max_length=255, unique=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('contents', models.BinaryField()),
            ],
        ),
    ]
