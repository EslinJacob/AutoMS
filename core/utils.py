def check_employee_type(user, type_list):
    if not (user.employee_type == type_list[0]
            or user.employee_type == type_list[1]):
        return False
    return True


def generate_invoice(order):
    from datetime import datetime
    from Management.models import Order

    date = str(datetime.now().strftime('%Y%m%d'))
    full_num = str(order.customer.phone_no)
    phone_no = full_num[:3]
    order_count = str(Order.objects.all().count())

    invoice_number = date+'-'+phone_no+'-'+order_count
    return invoice_number
