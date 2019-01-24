#!/usr/bin/python3
import pandas as pd
import datetime
import os


white_list_Employees = ["Rodriguez, Cesar",
                        "Sikk, Liliana",
                        'CUMBE, JUAN',
                        'STANKER, ANTHONY',
                        'VOYTYUK, TARAS',
                        'TOWER CRANE']

white_list_Department = ['RCS', 'Office']


TIME = '12:13'
TIME_LIMIT = '00 :40:00'
CODE = 34

key_api = os.environ.get('Timestation_key')
today_date = datetime.date.today().strftime('%Y-%m-%d')
url = f"https://api.mytimestation.com/v0.1/reports/?api_key={key_api}" \
    f"&Report_StartDate={today_date}&Report_EndDate={today_date}&id={CODE}&exportformat=csv"


def time_compare(date_time):
    date1 = datetime.datetime.strptime(date_time, '%H:%M')
    date2 = datetime.datetime.strptime(TIME, '%H:%M')
    remening_time = date2 - date1
    return remening_time


def getting_data_in():
    raw_data = pd.read_csv(url)
    group_name = raw_data[raw_data["Time"] <= TIME]
    duplicates_removed = group_name.drop_duplicates(subset="Name", keep='last')
    punch_in_df = duplicates_removed[duplicates_removed.Activity.str.contains('Punch In')]
    return punch_in_df


def result_noon():
    data = getting_data_in()
    data['time_subtra'] = data['Time'].apply(time_compare)
    data_after_subt = data[data['time_subtra'] > TIME_LIMIT]
    return data_after_subt


def white_list_filter():
    data_raw = result_noon()
    data = data_raw.to_dict('index')
    no_department_list = [i for i in data.values() if i["Department"] not in white_list_Department]
    return [item for item in no_department_list if item['Name'] not in white_list_Employees]


def send_names():

    x = []
    for i in white_list_filter():
        x.append(i['Name'])
    return x


def local_display():

    for i in white_list_filter():
       print(f"{i['Name']:30}  {i['Department']:30}  {i['Time']}")
    input('')


if __name__ == '__main__':

    local_display()