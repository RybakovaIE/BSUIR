# Generated by Django 4.2.6 on 2023-11-08 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='male',
            field=models.CharField(choices=[('0', 'М'), ('1', 'Ж')], max_length=50),
        ),
    ]
