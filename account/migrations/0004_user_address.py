# Generated by Django 4.2.2 on 2023-08-20 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_user_gender_user_marketing_user_personal'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.TextField(blank=True, verbose_name='address'),
        ),
    ]
