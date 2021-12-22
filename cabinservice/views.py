from django.shortcuts import render
import requests
from requests.structures import CaseInsensitiveDict
from rest_framework.decorators import action, api_view
from rest_framework import viewsets
from .models import Services, Orders
from .forms import NewOrderForm, DeleteOrderForm, LoginForm
from .serializers import OrderSerializer, ServicesSerializer

class OrderViewSet(viewsets.ModelViewSet):
   queryset = Orders.objects.all()
   serializer_class = OrderSerializer

class ServicesViewSet(viewsets.ModelViewSet):
   queryset = Services.objects.all()
   serializer_class = ServicesSerializer

def login(request):
    global jwt_token
    if request.method == 'POST':
        url = 'https://wom21-projekt-lindgand-hermanbex.azurewebsites.net/users/login'
        login_form = LoginForm(request.POST)
        
        if login_form.is_valid():
            json_data = { 'email': login_form.cleaned_data.get('email'), 'password': login_form.cleaned_data.get('password')}
            jwt_token = requests.post(url, json=json_data)

            if len(jwt_token.text) > 27:
                cabin_url = 'https://wom21-projekt-lindgand-hermanbex.azurewebsites.net/cabins/owned'
                headers = CaseInsensitiveDict()
                headers["Accept"] = "application/json"
                headers["Authorization"] = "Bearer " + jwt_token.text

                resp = requests.get(cabin_url, headers=headers)
                cabins_data = resp.json()
                service_data = Services.objects.values_list('type_of_service', flat=True)
                
                return render(request, 'home.html', {'cabins': cabins_data, 'type_of_service': service_data})
            
            else:
                return render(request, 'login.html')
        else:
            return render(request, 'login.html')
    else: 
        return render(request, 'login.html')

def new_order(request):
    if request.method == 'POST':
        url = 'https://wom21-projekt-lindgand-hermanbex.azurewebsites.net/cabins/owned'
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer " + jwt_token.text
       
        resp = requests.get(url, headers=headers)
        cabins_data = resp.json()
        service_data = Services.objects.values_list('type_of_service', flat=True)
        
        form = NewOrderForm(request.POST)
        if form.is_valid():
            f = Orders(date_of_service=form.cleaned_data.get('order_date'), service=form.cleaned_data.get('service'), cabin=form.cleaned_data.get('cabins'))
            
            f.save()
            order_data = Orders.objects.values()
            return render(request, 'home.html', {'order_data': order_data, 'cabins': cabins_data, 'type_of_service': service_data}) 
        else:
            form = NewOrderForm()
        return render(request, 'home.html', {'cabins': cabins_data, 'type_of_service': service_data}) 
    else:
        return render(request, 'login.html') 

def delete_order(request):
    if request.method == 'POST':
        url = 'https://wom21-projekt-lindgand-hermanbex.azurewebsites.net/cabins/owned'
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer " + jwt_token.text

        resp = requests.get(url, headers=headers)
        cabins_data = resp.json()
        service_data = Services.objects.values_list('type_of_service', flat=True)
        order_data = Orders.objects.values()
        form_for_delete = DeleteOrderForm(request.POST)
        
        if form_for_delete.is_valid():
                Orders.objects.filter(id=form_for_delete.cleaned_data.get('order')).delete()
        return render(request, 'home.html', {'order_data': order_data, 'cabins': cabins_data, 'type_of_service': service_data})
    else:
        return render(request, 'login.html') 

def update_order(request):
    if request.method == 'POST':
        url = 'https://wom21-projekt-lindgand-hermanbex.azurewebsites.net/cabins/owned'
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer " + jwt_token.text

        resp = requests.get(url, headers=headers)
        cabins_data = resp.json()
        service_data = Services.objects.values_list('type_of_service', flat=True)
        order_data = Orders.objects.values()
        form_for_update = NewOrderForm(request.POST)

        if form_for_update.is_valid():
            Orders.objects.filter(id=form_for_update.cleaned_data.get('selected_cabin')).update(date_of_service=form_for_update.cleaned_data.get('order_date'), cabin=form_for_update.cleaned_data.get('cabins'), service=form_for_update.cleaned_data.get('service'))

        return render(request, 'home.html', {'order_data': order_data, 'cabins': cabins_data, 'type_of_service': service_data})
    else:
        return render(request, 'login.html') 

def index(request):
    return render(request, 'login.html')
