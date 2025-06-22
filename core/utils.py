import pandas as pd
from .models import ComeGoneTimeModel
from datetime import timedelta
from django.utils import timezone



def create_excel_report(user_id):
    data = ComeGoneTimeModel.objects.filter(user_id=user_id).values()
    df = pd.DataFrame(data)
    
    file_path = f'reports/{user_id}_come_gone_time_report.xlsx'
    df.to_excel(file_path, index=False)
    
    return file_path


def calculate_work_summary(user, start_date, end_date):
    start_date_aware = timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time()))
    end_date_aware = timezone.make_aware(timezone.datetime.combine(end_date, timezone.datetime.max.time()))

    events = ComeGoneTimeModel.objects.filter(
        user=user,
        time__gte=start_date_aware,
        time__lte=end_date_aware
    ).order_by('time')

    total_duration = timedelta(0)
    work_days = set()
    arrival_time = None

    for event in events:
        work_days.add(event.time.date())

        if event.status is True and arrival_time is None:
            arrival_time = event.time
        elif event.status is False and arrival_time is not None:
            duration = event.time - arrival_time
            total_duration += duration
            arrival_time = None

    return {
        "total_duration": total_duration,
        "total_days": len(work_days)
    }