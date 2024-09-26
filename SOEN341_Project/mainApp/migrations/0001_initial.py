# Generated by Django 5.1.1 on 2024-09-25 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('email', models.EmailField(default='', max_length=254, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('instructor', models.BooleanField(default=False)),
            ],
        ),
    ]
