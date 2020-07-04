import requests
import json
import pandas as pd
import numpy as np

def get_KA_covid_data():
    import requests
    import json
    import pandas as pd
    import numpy as np
    response = requests.get("https://api.covid19india.org/v3/data-all.json")
    data = json.loads(response.content)
    Date = []
    Confirmed = []
    Deceased = []
    Recovered = [] 
    Tested = []
    for key,values in data.items():
        if "KA" in values:
            Date.append(key)
            Confirmed.append(values["KA"]["total"]["confirmed"])
            if "deceased" in values["KA"]["total"]:
                Deceased.append(values["KA"]["total"]["deceased"])
            else:
                Deceased.append(0)
            if "recovered" in values["KA"]["total"]:
                Recovered.append(values["KA"]["total"]["recovered"])
            else:
                Recovered.append(0)
            if "tested" in values["KA"]["total"]:
                Tested.append(values["KA"]["total"]["tested"])
            else:
                Tested.append(0)
    df = pd.DataFrame(zip(Date,Confirmed,Deceased,Recovered))
    df['timeStep'] = np.arange(0,len(df))+1
    df.columns = ["Date","Confirmed","Deceased","Recovered","timeStep"]
    return df   


def getKAADistrictDropDownValue():
    import requests
    import json
    options = []
    response = requests.get("https://api.covid19india.org/districts_daily.json")
    data = json.loads(response.content)
    for key,value in data["districtsDaily"]["Karnataka"].items():
        options.append({'label': key, 'value': key})
    return options

def get_districtWise(district):
    import requests
    import json
    active = []
    confirmed = []
    deceased = []
    recovered = []
    date = []
    response = requests.get("https://api.covid19india.org/districts_daily.json")
    data = json.loads(response.content)
    for key,value in data["districtsDaily"]["Karnataka"].items():
        if key == district:
            for itm in value:
                active.append(itm['active'])
                confirmed.append(itm['confirmed'])
                deceased.append(itm['deceased'])
                recovered.append(itm['recovered'])
                date.append(itm['date'])
    data_df = pd.DataFrame(zip(date ,confirmed ,active ,recovered ,deceased))
    data_df['timeStep'] = np.arange(0,len(data_df))+1
    data_df.columns = ["Date","Confirmed","Active","Recovered","Deceased","timeStep"]
    return data_df