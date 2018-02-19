# Generated by Django 2.0.1 on 2018-02-13 06:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0008_remove_club_position'),
    ]

    operations = [
        migrations.RenameField(
            model_name='club',
            old_name='club_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='club',
            old_name='club_image',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='club',
            old_name='club_name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='applylist',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.Club'),
        ),
        migrations.AlterField(
            model_name='applylist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='clubrule',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.Club'),
        ),
    ]