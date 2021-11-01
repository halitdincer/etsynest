from django.utils import timezone

def per_day(field,time):
    return format(field/((timezone.now() - timezone.localtime(time)).days+1),".2f")