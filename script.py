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

    # color rows
    def color_row(color, row):
        return [f'background-color: {color}'] * len(row)

    def make_rows_colored():
        for index, row in concat_data.iterrows():
        
            if isinstance(row['hu'], str):
                curr_date = datetime.datetime.strptime(row['hu'], format)
                today = datetime.date.today()
                difference_in_dates = relativedelta.relativedelta(today, curr_date)

        
                if difference_in_dates.months < 3:
                    print('green #007500')
                    color = '#007500'
                    color_row(color, row)
                
                    # concat_data.style.apply(color_row, axis=1)
                
                elif difference_in_dates.months > 3 or difference_in_dates.months < 12:
                    print('orange #FFA500')
                    color = '#FFA500'
                    color_row(color, row)
                
                    # concat_data.style.apply(color_row, axis=1)
                
                elif difference_in_dates.months > 12:
                    print('red #b30000')
                    color = '#b30000'
                    color_row(color, row)

                    # concat_data.style.apply(color_row, axis=1)
                
        concat_data.reset_index(drop=True).style.apply(color_row, axis=1)

    if (colored == True) or (colored == "true"):
        print('true')
        make_rows_colored()

    # sort by gruppe row
    result = concat_data.sort_values(by='gruppe')

    filtered_data = result[['gruppe', 'rnr', *keys]]

    # filtered_data.reset_index(drop=True).style.apply(color_row, axis=1).to_excel(writer, sheet_name='welcome', index=False)
    filtered_data.to_excel(writer, sheet_name='welcome', index=False)
    writer.save()


python_task()