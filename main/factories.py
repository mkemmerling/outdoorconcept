"""User factories."""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

import factory


class SuperUserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = get_user_model()

    username = 'admin'
    password = 'admin'
    email = ''  # required by create_superuser()
    first_name = 'outdoorconcept'
    last_name = 'AdminstratorIn'

    # See http://factoryboy.readthedocs.org/en/latest/recipes.html#custom-manager-methods  # noqa
    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        manager = cls._get_manager(target_class)
        return manager.create_superuser(*args, **kwargs)


def create_superuser():
    SuperUserFactory.create()


class StaffUserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = get_user_model()

    username = 'editor'
    password = 'editor'
    first_name = 'outdoorconcept'
    last_name = 'VerwalterIn'

    _permissions = (
        'change_config',
        'add_kind', 'change_kind', 'delete_kind',
        'add_element', 'change_element', 'delete_element'
    )

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        manager = cls._get_manager(target_class)
        user = manager.create_user(*args, **kwargs)
        user.is_staff = True
        for perm in Permission.objects.filter(codename__in=cls._permissions):
            user.user_permissions.add(perm)
        user.save()


def create_staff():
    StaffUserFactory.create()
