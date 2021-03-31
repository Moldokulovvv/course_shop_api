from rest_framework import serializers



import requests
from bs4 import BeautifulSoup
import json
import csv

from django.shortcuts import render

print('Hello world!')


def get_html(url):
    response = requests.get(url)
    return response.text


def write_to_csv(data):
    with open('test.csv', 'a') as my_file:
        writer = csv.writer(my_file, delimiter='/')
        writer.writerow((data['title'], data['photo'], data['description']))


list_news = []

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    product_list = soup.find('div', class_='b-plainlist')
    products = product_list.find_all('li', class_='b-plainlist__item')

    for product in products:

        try:
            title = product.find('img').get('title')

        except:
            title = ''

        try:
            photo = product.find('img').get('src')
        except:
            photo = ''

        try:
            description = product.find('div', class_='b-plainlist__announce')

        except:
            description = ''

        data = {'title': title, 'photo': photo, 'description': str(description)[38:-10]}
        list_news.append(data)
        # write_to_csv(data)

    return data

context = list_news
def new(request):
    odejda_url = 'https://ru.sputnik.kg/tags/event_koncert/'
    pages = ''
    result = get_page_data(get_html(odejda_url))
    result = context


    return render(request, 'blog.html', {'result': result})





class NewsSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, read_only=True)
    description = serializers.CharField(max_length=255, read_only=True)


    def to_representation(self, instance):
        ...


