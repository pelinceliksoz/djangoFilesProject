from django.shortcuts import render
from django.views import View
import csv
import pandas as pd
import numpy as np
import warnings
import xml.etree.ElementTree as ETree



class HomeView(View):
    def get(self, request):
        context = {}
        return render(request, 'home.html', context);


class CsvFileView(View):
    def get(self, request):
        # Create a dataframe from csv
        df = pd.read_csv('books.csv', delimiter=';')
        # User list comprehension to create a list of lists from Dataframe rows
        list_of_books = [list(row) for row in df.values]
        print(list_of_books)
        context = {
            'list_of_books': list_of_books,
        }
        return render(request, 'csv_file.html', context);


class JsonFileView(View):
    def get(self, request):
        context = {}
        return render(request, 'json_file.html', context);


class XmlFileView(View):
    def get(self, request):
        context = {}
        return render(request, 'xml_file.html', context);


