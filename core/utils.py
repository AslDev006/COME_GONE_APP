import pandas as pd
from .models import ComeGoneTimeModel

def create_excel_report(user_id):
    data = ComeGoneTimeModel.objects.filter(user_id=user_id).values()
    df = pd.DataFrame(data)
    
    # Excel faylni saqlash
    file_path = f'reports/{user_id}_come_gone_time_report.xlsx'
    df.to_excel(file_path, index=False)
    
    return file_path