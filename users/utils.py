import json
from django.contrib.auth.models import Permission
from PIL import Image
from io import BytesIO


def change_permissions(user, json_data):

    # user.is_staff = json_data['is_admin']
    # user.save()
    
    model_data = {
        "employee": { 'app': 'employees', 'name': 'employee'},
        "employeeTransaction": { 'app': 'employees', 'name': 'employeetransaction'},
        "users": { 'app': 'auth', 'name': 'user'},
        "cashCategory": { 'app': 'cashflow', 'name': 'cashcategory'},
        "cashSubcategory": { 'app': 'cashflow', 'name': 'cashsubcategory'},
        "cash": { 'app': 'cashflow', 'name': 'transaction'},
        "currency": { 'app': 'definitions', 'name': 'currency'},
        "unit": { 'app': 'definitions', 'name': 'unit'},
        "productCategory": { 'app': 'products', 'name': 'category'},
        "productSubcategory": { 'app': 'products', 'name': 'subcategory'},
        "product": { 'app': 'products', 'name': 'product'},
        "purchases": { 'app': 'purchases', 'name': 'purchase'},
        "payment": { 'app': 'purchases', 'name': 'purchasepayment'},
        "vendor": { 'app': 'purchases', 'name': 'vendor'},
        "vendorBalance": { 'app': 'purchases', 'name': 'openingbalance'},
        "sales": { 'app': 'sales', 'name': 'order'},
        "customer": { 'app': 'sales', 'name': 'customer'},
        "collection": { 'app': 'sales', 'name': 'orderpayment'},
        "customerBalance": { 'app': 'sales', 'name': 'openingbalance'},
        "account": { 'app': 'safe_management', 'name': 'account'},
        "journalVoucher": { 'app': 'safe_management', 'name': 'journalvoucher'},
    }
    
    tables = json.loads(json_data['tables'])
    # print(tables)
    for key, value in tables.items():
        view_permission = Permission.objects.get(codename=f'view_{model_data[key]["name"]}', content_type__app_label=model_data[key]['app'])
        add_permission = Permission.objects.get(codename=f'add_{model_data[key]["name"]}', content_type__app_label=model_data[key]['app'])
        delete_permission = Permission.objects.get(codename=f'delete_{model_data[key]["name"]}', content_type__app_label=model_data[key]['app'])
        update_permission = Permission.objects.get(codename=f'change_{model_data[key]["name"]}', content_type__app_label=model_data[key]['app'])
        if value['r']:
            user.user_permissions.add(view_permission)
        else:
            user.user_permissions.remove(view_permission)
        if value['c']:
            user.user_permissions.add(add_permission)
        else:
            user.user_permissions.remove(add_permission)
        if value['u']:
            user.user_permissions.add(update_permission)
        else:
            user.user_permissions.remove(update_permission)
        if value['d']:
            user.user_permissions.add(delete_permission)
        else:
            user.user_permissions.remove(delete_permission)


def compress_image(image, image_quality):
    im = Image.open(image)
    im = im.convert('RGB')
    im.thumbnail((800, 800), Image.LANCZOS)
    output = BytesIO()
    im.save(output, format='JPEG', quality=image_quality)  # Adjust quality as needed
    output.seek(0)
    return output
