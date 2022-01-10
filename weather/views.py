from django.shortcuts import render
import requests
from.models import City
from .forms import CityForm

def index(request):
    appid = '5ef7f5c82234395eb9eaac6a0bfbed69'
    url ='https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='+ appid
    #Для добавления новых городов в БД
    if(request.method == 'POST'):
        form = CityForm(request.POST)
        form.save()#Сохраняет запрос в БД

    #Что юы очистить форму при перезагрузки сайта
    form = CityForm()

    cities = City.objects.all()

    all_cities = []

    for city in cities:
        re = requests.get(url.format(city.name)).json()
        city_info = {
            'city': city.name,
            'temp': re['main']['temp'],
            'icon': re['weather'][0]['icon']
        }

        all_cities.append(city_info)



    context = {'all_info': all_cities, 'form': form}
    return render(request, 'weather/index.html', context)