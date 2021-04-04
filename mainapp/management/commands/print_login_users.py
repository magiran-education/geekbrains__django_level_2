from django.core.management.base import BaseCommand
from authapp.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.all()
        for u in users:
            print(f'Логин: {u.username}, последний вход: {u.last_login}')
