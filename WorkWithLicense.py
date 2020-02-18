from datetime import datetime

import WorkWithData


def check_license(user_id):
    current_date = datetime.now()
    license_end_date = WorkWithData.get_user_payment_license_date(user_id)
    if license_end_date:
        if current_date < license_end_date:
            return True
    return False
