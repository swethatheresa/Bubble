# Generated by Django 4.1.2 on 2022-12-17 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_room_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]