# core/tasks.py
from celery import shared_task
from django.utils import timezone
from django.db import transaction
from .models import UserModel, ComeGoneTimeModel
from .bot import send_auto_checkout_message
import logging
logger = logging.getLogger(__name__)


# @shared_task(name="auto_checkout_celery_task")
@shared_task
def run_auto_checkout_celery():
    task_start_time = timezone.now()
    logger.info(f"CELERY TASK STARTED: Auto checkout at [{task_start_time:%Y-%m-%d %H:%M:%S}]")

    users_to_checkout = UserModel.objects.filter(status=True)

    if not users_to_checkout.exists():
        logger.info("No users found to auto-checkout. Task finished.")
        return "No users found to auto-checkout."

    processed_count = 0
    for user in users_to_checkout:
        try:
            with transaction.atomic():
                local_now = timezone.localtime(task_start_time)
                checkout_time = local_now.replace(hour=15, minute=0, second=0, microsecond=0)

                checkout_instance = ComeGoneTimeModel.objects.create(
                    user=user,
                    status=False,
                    time=checkout_time
                )
                user.status = False
                user.save()

            send_auto_checkout_message(checkout_instance)
            logger.info(f"SUCCESS: Auto-checked out user '{user.full_name}'.")
            processed_count += 1

        except Exception as e:
            logger.error(f"ERROR: Failed to auto-checkout user '{user.full_name}': {e}", exc_info=True)

    return f"Checkout task finished successfully. Processed {processed_count} users."


@shared_task
def get_out_lunch_celery():
    task_start_time = timezone.now()
    logger.info(f"CELERY TASK STARTED: Auto checkout at [{task_start_time:%Y-%m-%d %H:%M:%S}]")

    users_to_lunch = UserModel.objects.filter(status=True)
    if not users_to_lunch.exists():
        logger.info("No users found to auto-checkout. Task finished.")
        return "No users found to auto-checkout."
    processed_count = 0
    for user in users_to_lunch:
        try:
            with transaction.atomic():
                local_now = timezone.localtime(task_start_time)
                checkout_time = local_now.replace(hour=12, minute=0, second=0, microsecond=0)

                checkout_instance = ComeGoneTimeModel.objects.create(
                    user=user,
                    status=False,
                    time=checkout_time
                )
                user.status = False
                user.save()

            send_auto_checkout_message(checkout_instance)
            logger.info(f"SUCCESS: Lunch get out out user '{user.full_name}'.")
            processed_count += 1

        except Exception as e:
            logger.error(f"ERROR: Failed to auto-checkout user '{user.full_name}': {e}", exc_info=True)

    return f"Lunch task finished successfully. Processed {processed_count} users."
