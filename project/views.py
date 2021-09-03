from django.shortcuts import render
from django.views import View
import pandas as pd
import xml.etree.ElementTree as ETree


class HomeView(View):
    def get(self, request):
        context = {}
        return render(request, 'home.html', context);


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
        print(df)
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
    def get(self, request, uid, file_type):
        uid = uid
        file_type = file_type

        if file_type == 'csv':
            df = pd.read_csv('data.csv', delimiter=',')
            service_list = get_service_list(df)
        elif file_type == 'json':
            df = pd.read_json('data.json')
            service_list = get_service_list(df)
        else:
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

        service_uid_list = get_service_uid_list(df)

        group_list = []
        for service in service_list:
            for id, group in service.items():
                if str(id) == uid:
                    group_list = group
        main_list = []
        spare_1_list = []
        spare_2_list = []
        for group in group_list:
            for group_type, trail in group.items():
                if group_type == '1MAIN':
                    main_list.append(str(trail))
                elif group_type == '1SPARE':
                    spare_1_list.append(str(trail))
                else:
                    spare_2_list.append(str(trail))

        print(main_list)
        print(spare_1_list)
        print(spare_2_list)

        df = pd.read_csv('data.csv', delimiter=',')
        service_list = get_service_list(df)
        context = {
            'service_list': service_list,
            'uid': uid,
            'file_type': file_type,
            'main_list': main_list,
            'spare_1_list': spare_1_list,
            'spare_2_list': spare_2_list,
        }
        return render(request, 'show_details.html', context);


def get_service_list(df):
    list_of_services = [list(row) for row in df.values]
    service_uid_list = get_service_uid_list(df)
    services_dict_list = get_services_dict_list(list_of_services)

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


def get_service_uid_list(df):
    uid_list = []
    for row in df.values:
        uid_list.append(row[0])

    service_uid_list = []
    for uid in uid_list:
        service_uid = uid
        if uid not in service_uid_list:
            service_uid_list.append(service_uid)

    return service_uid_list


def get_services_dict_list(list_of_services):
    edited_list_of_services = []
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
    return services_dict_list


def get_sorted_group_list(group_list):
    # for main
    sorted_group_list = []
    sort_groups(group_list, '1MAIN', '1', sorted_group_list)
    sort_groups(group_list, '1MAIN', '2', sorted_group_list)
    sort_groups(group_list, '1MAIN', '3', sorted_group_list)
    # for first spare
    sort_groups(group_list, '1SPARE', '1', sorted_group_list)
    sort_groups(group_list, '1SPARE', '2', sorted_group_list)
    sort_groups(group_list, '1SPARE', '3', sorted_group_list)
    # for second spare
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




