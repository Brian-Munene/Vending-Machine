"""
Create Permission Groups
"""

import logging
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

logger = logging.getLogger('accounts-logger')

GROUPS = {
    "Maintainer": {
        # general permissions
        "log entry": ["add","delete","change","view"],
        "group": ["add","delete","change","view"],
        "permission": ["add","delete","change","view"],
        "user": ["add","delete","change","view"],
        "content type": ["add","delete","change","view"],
        "session": ["add","delete","change","view"],

        # django app model specific permissions
        "products": ["add","delete","change","view"],
        "coins": ["add","delete","change","view"],
        "customuser": ["add","delete","change","view"],
    },

    "Customer": {
        # django app model specific permissions
        "products": ["view"],
        "coins": ["view", "add"],
        # "staff time sheet" : ["add","delete","change","view"],
    },
}


class Command(BaseCommand):
    help = 'Creates default permissions for the user groups'

    def handle(self, *args, **options):
        for group_name in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group_name)

            for app_model in GROUPS[group_name]:
                for permission_name in GROUPS[group_name][app_model]:
                    name = f'Can {permission_name} {app_model}'
                    logger.info(f'Creating {name}')

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Exception as e:
                        logger.warning(f"Error {str(e)} was raised")
                        continue
                    new_group.permissions.add(model_add_perm)
        print("Created default groups and permissions.")

