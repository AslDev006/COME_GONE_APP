# core/management/commands/auto_checkout_users.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from django.conf import settings
from core.models import UserModel, ComeGoneTimeModel
from core.bot import send_auto_checkout_message


class Command(BaseCommand):
    help = 'Tizimda "ishda" statusida qolib ketgan xodimlarni kun yakunida avtomatik ravishda tizimdan chiqaradi.'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(f'[{timezone.now():%Y-%m-%d %H:%M:%S}] Avtomatik chiqishni tekshirish boshlandi...'))

        users_who_forgot_to_checkout = UserModel.objects.filter(status=True)

        if not users_who_forgot_to_checkout.exists():
            self.stdout.write(
                self.style.WARNING('Hozirda "ishda" deb belgilangan xodimlar topilmadi. Jarayon yakunlandi.'))
            return

        for user in users_who_forgot_to_checkout:
            self.stdout.write(
                f'"{user.full_name}" (ID: {user.user}) tizimdan chiqishni unutgan. Avtomatik chiqarilmoqda...')

            try:
                with transaction.atomic():
                    local_now = timezone.localtime(timezone.now())
                    auto_checkout_time = local_now.replace(hour=12, minute=0, second=0, microsecond=0)

                    auto_checkout_instance = ComeGoneTimeModel.objects.create(
                        user=user,
                        status=False,
                        time=auto_checkout_time
                    )

                    user.status = False
                    user.save()

                send_auto_checkout_message(auto_checkout_instance)

                self.stdout.write(self.style.SUCCESS(
                    f'"{user.full_name}" muvaffaqiyatli avtomatik tizimdan chiqarildi.'
                ))

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'"{user.full_name}" ni avtomatik chiqarishda xatolik yuz berdi: {e}'
                ))

        self.stdout.write(self.style.SUCCESS('Tekshirish jarayoni muvaffaqiyatli tugallandi.'))