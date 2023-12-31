# Generated by Django 4.2.2 on 2023-06-12 22:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_newsletter_alter_post_publish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 12, 22, 38, 39, 845080, tzinfo=datetime.timezone.utc), verbose_name='Дата публикации'),
        ),
    ]
