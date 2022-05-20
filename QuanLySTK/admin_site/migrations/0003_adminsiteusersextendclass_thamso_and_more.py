# Generated by Django 4.0.4 on 2022-05-20 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_site', '0002_usersextendclass'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminSiteUsersextendclass',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('manv', models.CharField(max_length=12)),
            ],
            options={
                'db_table': 'admin_site_usersextendclass',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Thamso',
            fields=[
                ('tenthamso', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('giatri', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'thamso',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='UsersExtendClass',
        ),
    ]
