# Generated by Django 4.0.4 on 2022-05-03 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='lesson',
            constraint=models.UniqueConstraint(fields=('module_id', 'order_number'), name='unique_module_order'),
        ),
    ]
