from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from django.views import View
from .models import Person
from .forms import UserForm

#### sqli using raw
def unsafe_get_users1(request, **kwargs):
    user_name = kwargs['user_name']
    users = Person.objects.raw("SELECT * FROM member_list_person WHERE name = '%s'" % user_name)
    print(users)
    return HttpResponse(users)

def unsafe_get_users2(request, **kwargs):
    user_name = kwargs['user_name']
    users = Person.objects.raw(f"SELECT * FROM member_list_person WHERE name = '{user_name}'")
    return HttpResponse(users)

def unsafe_get_users3(request, **kwargs):
    user_name = kwargs['user_name']
    users = Person.objects.raw("SELECT * FROM member_list_person WHERE name = '{}'".format(user_name))
    return HttpResponse(users)

#### sqli using extra
def unsafe_get_users4(request, **kwargs):
    user_name = kwargs['user_name']
    users = Person.objects.extra(where=["name = '%s'" % user_name])

    return HttpResponse(users)


class CreateMember(View):

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            Person.objects.create(**form.cleaned_data)
            return HttpResponse("User Created!")

    def get(self, request):
        form = UserForm()
        return render(request, 'member_list/create.html', {'form': form})

## BAD CODE
class SearchMember(View):
    template_name = 'member_list/search.html'
    def get(self, request, *args, **kwargs):
        q = (request.GET.get('q') or '').strip()

        sql = """
        SELECT *
        FROM member_list_person
        """

        if q:
            sql += "WHERE name LIKE '%s'" % q

        print(sql)

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

            rows = [row[1] for row in rows]
            print(rows)
        context = {
            'rows' : rows
        }

        return render(request, self.template_name, context)

