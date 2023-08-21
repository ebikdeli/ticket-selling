# Generated by Django 4.2.2 on 2023-07-10 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(blank=True, max_length=30, verbose_name='session key')),
                ('is_paid', models.BooleanField(default=False, verbose_name='is paid')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('slug', models.SlugField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Cart',
                'ordering': ['-updated'],
            },
        ),
    ]