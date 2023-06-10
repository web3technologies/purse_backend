# Generated by Django 4.2.1 on 2023-06-10 23:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import purse_finance.mixins.plaid_exception


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('purse_catalog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=255, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Item is active'), ('LOGIN_REQUIRED', 'The item must be re linked with plaid'), ('INTERNAL_ERROR', 'The system is not able to handle the error')], default='ACTIVE', max_length=255)),
                ('plaid_item_id', models.CharField(default=None, max_length=255, null=True)),
                ('institution', models.CharField(max_length=255, null=True)),
                ('plaid_internal_status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='purse_catalog.plaidapierror')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, purse_finance.mixins.plaid_exception.PlaidUtilityMixin),
        ),
        migrations.CreateModel(
            name='PlaidAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('CRYPTO', 'CRYPTO'), ('PLAID', 'PLAID')], default='', max_length=255)),
                ('account_type', models.CharField(choices=[('INVESTMENT', 'INVESTMENT'), ('ASSET', 'ASSET'), ('DEPOSITORY', 'DEPOSITORY'), ('LOAN', 'LOAN'), ('CREDIT', 'CREDIT')], default='', max_length=255)),
                ('plaid_account_id', models.CharField(max_length=255, unique=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Item linked to account is active'), ('LOGIN_REQUIRED', 'Item linked to account needs to be re linked')], max_length=255)),
                ('available_balance', models.FloatField(default=None, null=True)),
                ('current_balance', models.FloatField(default=None, null=True)),
                ('last_update', models.DateTimeField(default=django.utils.timezone.now)),
                ('item', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='purse_finance.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, purse_finance.mixins.plaid_exception.PlaidUtilityMixin),
        ),
        migrations.CreateModel(
            name='NetWorth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('networth', models.CharField(max_length=255)),
                ('cash', models.CharField(default=None, max_length=255, null=True)),
                ('assets', models.CharField(default=None, max_length=255, null=True)),
                ('debt', models.CharField(default=None, max_length=255, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CryptoAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('CRYPTO', 'CRYPTO'), ('PLAID', 'PLAID')], default='', max_length=255)),
                ('ticker', models.CharField(default=None, max_length=255, null=True)),
                ('amount', models.CharField(max_length=255)),
                ('value', models.FloatField(default=0)),
                ('last_update', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.BigIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
