import datetime
import requests
import pandas
from dateutil import relativedelta

def python_task():
    # input the parameters and split by blank space
    keys = input("Enter keys:").split(' ')
    colored = input("Enter True or False:").lower().strip() or True

    #make the first request
    login_url = 'https://api.baubuddy.de/index.php/login'
    url = 'https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active'

    login_info = {
        'username': '365',
        'password': '1'
    }

    headers_auth_token = {
        "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
        "Content-Type": "application/json"
    }
    # request to get the bearer token
    access_token_request = requests.post(login_url, headers=headers_auth_token, json=login_info)

    auth_info = access_token_request.json()['oauth']
    auth_bearer_token = auth_info['access_token']

    headers = {
        "Authorization": f'Bearer {auth_bearer_token}',
    }

    # request to get the resources and parse them to pandas data frame
    resources = requests.get(url, headers=headers,)

    data = resources.json()
    request_df = pandas.DataFrame(data)

    # filter out resources without hu field
    request_df = request_df[request_df.hu > '']

    # read and parse the csv file
    csv_file = pandas.read_csv('vehicles.csv', sep=';')

    format = '%Y-%m-%d'
    today = datetime.date.today()
    writer = pandas.ExcelWriter(f'vehicles_{today}.xlsx')

    # concat the two data frames
    frames = [request_df, csv_file]
    
    concat_data = pandas.concat(frames)


python_task()