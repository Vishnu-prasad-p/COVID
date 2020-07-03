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