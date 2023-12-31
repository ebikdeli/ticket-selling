# Generated by Django 4.2.2 on 2023-08-28 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(editable=False, max_length=10, unique=True, verbose_name='order_id')),
                ('discounts', models.DecimalField(decimal_places=0, default=0, max_digits=10, verbose_name='discounts')),
                ('is_paid', models.BooleanField(default=False, verbose_name='is_paid')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('slug', models.SlugField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_cart', to='cart.cart', verbose_name='cart')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Order',
                'ordering': ['-updated'],
            },
        ),
    ]
