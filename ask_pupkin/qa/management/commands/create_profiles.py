from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from qa.models import Profile

class Command(BaseCommand):
    help = 'Создает профили для всех пользователей, у которых их нет'
    
    def handle(self, *args, **options):
        self.stdout.write('Проверяю пользователей без профилей...')
        
        users_without_profiles = []
        for user in User.objects.all():
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                users_without_profiles.append(user)
        
        if users_without_profiles:
            self.stdout.write(f'Найдено {len(users_without_profiles)} пользователей без профилей:')
            
            for user in users_without_profiles:
                Profile.objects.create(user=user)
                self.stdout.write(f'  ✓ Создан профиль для: {user.username}')
            
            self.stdout.write(self.style.SUCCESS(f'✅ Создано профилей: {len(users_without_profiles)}'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ У всех пользователей есть профили!'))
        
        # Показываем статистику
        total_users = User.objects.count()
        total_profiles = Profile.objects.count()
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(f'👥 Всего пользователей: {total_users}')
        self.stdout.write(f'📋 Всего профилей: {total_profiles}')
        if total_users == total_profiles:
            self.stdout.write(self.style.SUCCESS('✅ Соответствие: 100%'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️  Несоответствие: {total_users - total_profiles}'))