from datetime import datetime, timedelta

import WorkWithData


def check_license(chat_id):
    current_date = datetime.now()
    license_end_date = WorkWithData.get_user_payment_license_date(chat_id)
    if license_end_date:
        if current_date.date() < license_end_date:
            return True
    return False


def set_trial(chat_id):
    if WorkWithData.access_trial_license(chat_id):
        current_date = datetime.now().date()
        end_date = current_date + timedelta(days=15)
        WorkWithData.insert_trial_license(chat_id, end_date)
        return True
    else:
        return False
