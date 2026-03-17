from urllib.request import urlopen
import json
import datetime

def get_season_events(year):

    response = urlopen(f'https://api.openf1.org/v1/meetings?year={year}')
    data = json.loads(response.read().decode('utf-8'))

    #If the event is a pre-season test, skip it
    if __name__ == "__main__":
        print(f"Events for the {year} Formula 1 World Championship: \n")
        
        for datum in data:
            if datum['meeting_name'] == 'Pre-Season Testing':
                continue
            print(f"{datum['meeting_name']} - {datum['country_name']}")
            
    else:
        import pandas as pd
        df = pd.DataFrame(data)
        #remove unnecessary columns (keep meeting_key for selection)
        events_table = df.drop(columns=['country_key', 'country_flag', 'year', 'circuit_info_url',  'circuit_image'])
        #remove pre-season testing events
        events_table = events_table[events_table['meeting_name'] != 'Pre-Season Testing']
        events_table.reset_index(drop=True, inplace=True)
        return events_table

def get_meeting_data(meeting_key):
    response = urlopen(f'https://api.openf1.org/v1/meetings?meeting_key={meeting_key}')
    data = json.loads(response.read().decode('utf-8'))
    return data
            
if __name__ == "__main__":
    year = datetime.datetime.now().year - 1           
    get_season_events(year)


# If you want, you can import the results in a DataFrame (you need to install the `pandas` package first)
# import pandas as pd
# df = pd.DataFrame(data)

