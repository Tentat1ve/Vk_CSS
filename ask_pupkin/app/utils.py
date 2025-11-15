# app/utils.py
from django.core.paginator import Paginator, Page

def paginate(objects_list, request, per_page=20):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    
    try:
        page_number = int(page_number)
    except (TypeError, ValueError):
        page_number = 1
    
    page_obj = paginator.get_page(page_number)
    return page_obj