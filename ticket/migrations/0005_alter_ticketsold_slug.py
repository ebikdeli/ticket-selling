# Generated by Django 4.2.2 on 2023-08-29 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0004_alter_ticket_ticket_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketsold',
            name='slug',
            field=models.SlugField(blank=True, verbose_name='slug'),
        ),
    ]