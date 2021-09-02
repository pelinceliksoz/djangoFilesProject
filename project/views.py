from django.shortcuts import render
from django.views import View
import csv
import pandas as pd
import numpy as np
import warnings
import xml.etree.ElementTree as ETree
from openpyxl.utils.dataframe import dataframe_to_rows


class HomeView(View):
    def get(self, request):
        context = {}
        return render(request, 'home.html', context);


class CsvFileView(View):
    def get(self, request):
        # Create a dataframe from csv
        df = pd.read_csv('data.csv', delimiter=',')
        # User list comprehension to create a list of lists from Dataframe rows
        list_of_books = [list(row) for row in df.values]
        context = {
            'list_of_books': list_of_books,
        }
        return render(request, 'csv_file.html', context);


class JsonFileView(View):
    def get(self, request):

        df_json = pd.read_json('data.json')
        list_of_books = [list(row) for row in df_json.values]
        # print(list_of_books)
        keys = df_json.keys()
        key_values = keys.values
        # print(key_values)
        context = {
            'list_of_books': list_of_books,
            'key_values': key_values,
        }
        return render(request, 'json_file.html', context);


class XmlFileView(View):
    def get(self, request):
        tree = ETree.parse('data.xml')
        root = tree.getroot()
        a = []
        for ele in root:
            b = {}
            for i in list(ele):
                b.update({i.tag: i.text})
                a.append(b)

        df_xml = pd.DataFrame(a)
        df_xml.drop_duplicates(keep='first', inplace=True)
        list_of_books = df_xml.values.tolist()
        xml_keys = df_xml.keys()
        xml_keys_list = xml_keys.values
        context = {
            'list_of_books': list_of_books,
            'xml_keys_list': xml_keys_list,
        }
        return render(request, 'xml_file.html', context);


class CsvDataView(View):
    def get(self, request):
        # Create a dataframe from csv
        df = pd.read_csv('data.csv', delimiter=',')
        service_list = get_service_list(df)
        main = '1MAIN'
        spare_1 = '1SPARE'
        spare_2 = '2SPARE'
        context = {
            'service_list': service_list,
            'main': main,
            'spare_1': spare_1,
            'spare_2': spare_2
        }
        return render(request, 'csv_data.html', context);


class JsonDataView(View):
    def get(self, request):
        # Create a dataframe from csv
        df = pd.read_json('data.json')
        service_list = get_service_list(df)
        main = '1MAIN'
        spare_1 = '1SPARE'
        spare_2 = '2SPARE'
        context = {
            'service_list': service_list,
            'main': main,
            'spare_1': spare_1,
            'spare_2': spare_2
        }
        return render(request, 'json_data.html', context);


class XmlDataView(View):
    def get(self, request):
        tree = ETree.parse('data.xml')
        root = tree.getroot()
        a = []
        for ele in root:
            b = {}
            for i in list(ele):
                b.update({i.tag: i.text})
                a.append(b)

        df = pd.DataFrame(a)
        df.drop_duplicates(keep='first', inplace=True)
        service_list = get_service_list(df)
        main = '1MAIN'
        spare_1 = '1SPARE'
        spare_2 = '2SPARE'
        context = {
            'service_list': service_list,
            'main': main,
            'spare_1': spare_1,
            'spare_2': spare_2
        }
        return render(request, 'xml_data.html', context);


class ShowDetailsView(View):
    def get(self, request):
        context = {}
        return render(request, 'show_details.html', context);


def get_service_list(df):
    list_of_services = [list(row) for row in df.values]
    # print(list_of_services)

    uid_list = []
    for row in df.values:
        uid_list.append(row[0])
    # print(uid_list)

    service_uid_list = []
    for uid in uid_list:
        service_uid = uid
        if uid not in service_uid_list:
            service_uid_list.append(service_uid)

    edited_list_of_services = []
    group_trial_dict_list = []
    services_dict_list = []

    for service in list_of_services:
        edited_services = []
        group_trial_dict = {}
        services_dict = {}
        group_name = str(service[2]) + str(service[1])
        trail_name = str(service[4]) + str(service[3])
        edited_services.append(service[0])
        edited_services.append(group_name)
        edited_services.append(trail_name)
        edited_list_of_services.append(edited_services)

        group_trial_dict[group_name] = trail_name
        services_dict[service[0]] = group_trial_dict
        services_dict_list.append(services_dict)
        # group_trial_dict_list.append(group_trial_dict)
    # print(services_dict_list)
    service_list = []
    service_dict = {}
    for uid in service_uid_list:
        group_list = []
        for service in services_dict_list:
            for key in service.keys():
                if key == uid:
                    group_list.append(service.get(uid))
        # print(group_list)
        sorted_group_list = get_sorted_group_list(group_list)
        service_dict[uid] = sorted_group_list
    service_list.append(service_dict)
    return service_list


def get_sorted_group_list(group_list):
    # for main
    sorted_group_list = []
    sort_groups(group_list, '1MAIN', '1', sorted_group_list)
    sort_groups(group_list, '1MAIN', '2', sorted_group_list)
    sort_groups(group_list, '1MAIN', '3', sorted_group_list)
    sort_groups(group_list, '1SPARE', '1', sorted_group_list)
    sort_groups(group_list, '1SPARE', '2', sorted_group_list)
    sort_groups(group_list, '1SPARE', '3', sorted_group_list)
    sort_groups(group_list, '2SPARE', '1', sorted_group_list)
    sort_groups(group_list, '2SPARE', '2', sorted_group_list)
    sort_groups(group_list, '2SPARE', '3', sorted_group_list)
    return sorted_group_list


def sort_groups(group_list, key_name, order, sorted_group_list):
    for group in group_list:
        for key, value in group.items():
            if key == key_name:
                if value.startswith(order):
                    last_index = len(value)
                    edited_value = value[1:last_index]
                    sorted_group_list.append({key: edited_value})




