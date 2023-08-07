# Generated by Django 4.0.4 on 2022-05-20 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin_site', '0004_usersextendclass_delete_adminsiteusersextendclass'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersextendclass',
            name='id',
        ),
        migrations.AlterField(
            model_name='usersextendclass',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
