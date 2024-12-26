# Generated by Django 5.0.4 on 2024-12-17 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_system_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_text', models.TextField()),
                ('translated_text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('english_word', models.CharField(max_length=50, unique=True)),
                ('german_translation', models.CharField(max_length=50)),
                ('pos_tag', models.CharField(max_length=50)),
            ],
            options={
                'indexes': [models.Index(fields=['english_word'], name='search_syst_english_f6c35f_idx')],
            },
        ),
        migrations.CreateModel(
            name='WordDictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_word', models.CharField(max_length=100)),
                ('translated_word', models.CharField(max_length=100)),
                ('pos_tag', models.CharField(max_length=50)),
                ('frequency', models.IntegerField(default=1)),
                ('grammar_info', models.TextField()),
            ],
            options={
                'unique_together': {('source_word', 'translated_word')},
            },
        ),
    ]
