# Generated by Django 4.2.2 on 2023-08-29 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0003_alter_ticket_prize_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_number',
            field=models.CharField(blank=True, max_length=20, verbose_name='ticket_number'),
        ),
    ]
