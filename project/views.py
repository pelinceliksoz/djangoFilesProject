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
        list_of_services = [list(row) for row in df.values]
        # print(list_of_services)

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
        print(services_dict_list)
        print(services_dict_list[1])



        # uid_list = []
        # for row in df.values:
        #     uid_list.append(row[0])
        # # print(uid_list)
        #
        # service_uid_list = []
        # for uid in uid_list:
        #     service_uid = uid
        #     if uid not in service_uid_list:
        #         service_uid_list.append(service_uid)
        #
        # # for uid in service_uid_list:
        # services_list = []
        # group_trail_list = []
        #
        # i = 0
        # for service in services_dict_list:
        #     services_dict = {}
        #    # for uid in service_uid_list:
        #     for key in service.keys():
        #         while i < len(service_uid_list):
        #             if key == service_uid_list[i]:
        #                 print(key)
        #                 for value in service.values():
        #                     group_trail_list.append(value)
        #                     services_dict[key] = group_trail_list
        #                     services_list.append(services_dict)
        #                 i = i + 1
        # # print(services_list)
        # print(len(service_uid_list))

        # for uid in service_uid_list:
        #     for service in services_dict_list:
        #         print(service.)

        # for service in edited_list_of_services:
        #     group_trail_dict[service[1]] = service[2]
        #     group_trail_dict_list.append(group_trail_dict)
        # print(group_trail_dict_list)
        #
        services_dict_list = []
        # services_dict = {}
        #
        # for uid in service_uid_list:
        #     services_dict[uid] = '-'
        #
        # group_trial_dict = {}
        # group_trial_dict_list = []
        # for uid in service_uid_list:
        #     for service in edited_list_of_services:
        #         if uid == service[0]:
        #             group_trial_dict[service[1]] = {service[2]}
        #             group_trial_dict_list.append(group_trial_dict)
        #     service[0] = 0
        # print(group_trial_dict_list)
        #


        # for uid in services_dict:
        #     for service in edited_list_of_services:
        #         if uid == service[0]:
        #             for group_trail in group_trail_dict_list:
        #                 if service[2] in group_trail_dict_list:
        #                     print(girdi)
        #                     print(service[2])
        #                     # services_dict[uid] = 'aaaaa'
        #                 print('çıktı')
        # print(services_dict)



        # services_dict = {}
        # services_arr = []
        # group_trail_dict = {}
        # # for service in edited_list_of_services:
        # for uid in service_uid_list:
        #     for service in edited_list_of_services:
        #         if service[0] == uid:
        #             group_trail_dict[service[1]] = service[2]
        #             if service[0] not in services_arr:
        #                 services_arr.append(service[0])
        #     print(group_trail_dict)
                # services_dict[services_arr[0]] = group_trail_dict
                #
                #
                #

                # if service[0] != 0:
                #
                #     service[0] = 0
                #


        # for row in df.values:
        #     i = 0
        #     while i < len(service_uid_list):
        #         if row[0] == service_uid_list[i]:
        #
        #             print(row)
        #         i = i+1
        # group_dict = {}
        # group_arr = []
        # trail_dict = {}
        # group_trial_dict = {}
        # uid_dict = {}
        # for row in df.values:
        #     if row[0] == service_uid_list[1]: #i
        #         group_dict[row[1]] = row[2]   #sayılarla oynama
        #         group_arr.append(group_dict)
        #         trail_dict[row[3]] = row[4]   #sayılarla oynama
        #         uid_dict[service_uid_list[1]] = group_dict #i
        # # print(group_arr)








        context = {}
        return render(request, 'csv_data.html', context);


