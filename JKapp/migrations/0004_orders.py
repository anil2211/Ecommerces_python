# Generated by Django 2.2 on 2020-03-10 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JKapp', '0003_auto_20200112_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('items_json', models.CharField(max_length=2500)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=150)),
                ('address', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=150)),
                ('state', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=10)),
            ],
        ),
    ]
