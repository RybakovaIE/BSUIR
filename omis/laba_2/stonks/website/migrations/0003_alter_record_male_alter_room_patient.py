# Generated by Django 4.2.6 on 2023-11-08 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_alter_record_male'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='male',
            field=models.CharField(choices=[('Мужской', 'Мужской'), ('Женский', 'Женский')], max_length=50),
        ),
        migrations.AlterField(
            model_name='room',
            name='patient',
            field=models.CharField(max_length=15),
        ),
    ]