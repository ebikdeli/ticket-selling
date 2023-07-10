# Generated by Django 4.2.2 on 2023-07-10 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ticket', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='ticket',
            field=models.ManyToManyField(related_name='cart_tickets', to='ticket.ticket', verbose_name='ticket'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_user', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
