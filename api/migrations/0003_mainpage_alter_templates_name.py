# Generated by Django 5.0.6 on 2024-06-21 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_scripts_templates'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=56)),
                ('text', models.TextField(default=None)),
            ],
        ),
        migrations.AlterField(
            model_name='templates',
            name='name',
            field=models.CharField(max_length=56),
        ),
    ]
