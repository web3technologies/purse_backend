from decouple import config
from django.db import transaction
from django import setup
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'purse_backend.settings.{config("DJANGO_SETTINGS_ENV")}')
setup()


from purse_catalog.models import PlaidTransactionCategory, PlaidTransactionSubCategory
from purse_core.client import plaid_client


def main():
    categories = plaid_client.categories_get({}).get("categories")
    sub_category_mapping = {}
    
    for category in categories:
        for h_item in category.get("hierarchy"):
            sub_category_mapping[h_item] = True

    with transaction.atomic():
        sub_categories_to_create = []
        for label in sub_category_mapping:
            sub_categories_to_create.append(
                PlaidTransactionSubCategory(
                    label=label
                )
            )
        created_sub_categories = PlaidTransactionSubCategory.objects.bulk_create(sub_categories_to_create, ignore_conflicts=True)
        print(f"{len(created_sub_categories)} Sub Categories created.")

    with transaction.atomic():
        created_categories = []
        for category in categories:
            obj, created = PlaidTransactionCategory.objects.get_or_create(
                plaid_category_id=int(category.get("category_id")),
                group=category.get("group"),
            )
            obj.subcategories.set(PlaidTransactionSubCategory.objects.filter(label__in=category.get("hierarchy")))
            if created:
                created_categories.append(created)
        print(f"{len(created_categories)} Categories created.")

if __name__ == "__main__":
    main()