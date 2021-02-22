from django.http import HttpResponse
from .models import Person


def safe_get_users1(request, **kwargs):
    # uses parameterized query
    user_name = kwargs['user_name']
    users = Person.objects.raw('SELECT * FROM member_list_person WHERE name = %s', [user_name])
    print(users)
    return HttpResponse(users)

def safe_get_users2(request, **kwargs):
    # uses Django ORM
    user_name = kwargs['user_name']
    users = Person.objects.filter(name=user_name).first()
    return HttpResponse(users)

def safe_get_users3(request, **kwargs):
    user_name = kwargs['user_name']
    users = Person.objects.extra(where=["name = %s"], params=[user_name])
    return HttpResponse(users)