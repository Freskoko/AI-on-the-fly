from requests import get
from os import environ
from dotenv import load_dotenv

def get_calendar_events():

    load_dotenv()
    key = environ.get("cal_key")

    url = f"https://mitt.uib.no/api/v1/calendar_events?access_token={key}" #&end_date={end_date}

    data = get(url)

    return data.json()

def clean_dict(in_dict):
    outlist = []

    for event in in_dict:
        outdict = {}

        outdict["title"] = event["title"]
        outdict["start_time"] = event['start_at']
        outdict["end_time"] = event['end_at']

        outlist.append(outdict)

    if outlist == []:
        return ["No calendar events"]
    return outlist

def get_clean_events():
    return clean_dict( get_calendar_events() )

if __name__ == "__main__":
    print(get_clean_events())
