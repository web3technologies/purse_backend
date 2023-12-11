# Generated by Django 4.2.1 on 2023-12-11 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purse_catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaidTransactionSubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlaidTransactionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plaid_category_id', models.IntegerField(unique=True)),
                ('group', models.CharField(max_length=255)),
                ('subcategories', models.ManyToManyField(to='purse_catalog.plaidtransactionsubcategory')),
            ],
        ),
    ]
