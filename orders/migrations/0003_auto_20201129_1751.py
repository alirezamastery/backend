# Generated by Django 3.1.3 on 2020-11-29 14:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0006_auto_20201119_1815'),
        ('orders', '0002_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='ordered_date',
            new_name='order_date',
        ),
        migrations.AddField(
            model_name='order',
            name='checkout',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='user',
            field=models.ForeignKey(default=18, on_delete=django.db.models.deletion.PROTECT, to='users.customuser'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.product'),
        ),
    ]
