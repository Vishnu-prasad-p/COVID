import requests
import json
import pandas as pd
import numpy as np

response = requests.get("https://api.covid19india.org/v4/data-all.json")
data = json.loads(response.content)

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
    for key, val in data.popitem()[1].items():
        if key == 'KA':
            for k,v in val['districts'].items():
                options.append({'label': k, 'value': k})
    return options

def get_districtWise(district):
    import requests
    import json
    import pandas as pd
    import numpy as np
    confirmed = []
    deceased = []
    recovered = []
    date = []
    for key,value in data.items():
        if 'KA' in value:
            if 'districts' in value['KA']:
                for k,itm in value['KA']['districts'].items():
                    if k == 'Bagalkote':
                        confirmed.append(itm['total']['confirmed'])
                        deceased.append(itm['total']['deceased'])
                        recovered.append(itm['total']['recovered'])
                        date.append(key)
    data_df = pd.DataFrame(zip(date ,confirmed ,recovered ,deceased))
    data_df['timeStep'] = np.arange(0,len(data_df))+1
    data_df.columns = ["Date","Confirmed","Recovered","Deceased","timeStep"]
    return data_df

def allDistrictstabel():
    import requests
    import json
    import pandas as pd
    import numpy as np
    response = requests.get("https://api.covid19india.org/state_district_wise.json")
    data = json.loads(response.content)
    District = []
    Confirmed = []
    Deceased = []
    Recovered = [] 
    Tested = []
    Active = []
    for key,values in data.items():
        if key == "Karnataka":
            for k,v in values["districtData"].items():
                District.append(k)
                Confirmed.append(v["confirmed"])
                Deceased.append(v["deceased"])
                Recovered.append(v["recovered"])
                Active.append(v["active"])
    df = pd.DataFrame(zip(District,Active,Confirmed,Deceased,Recovered))
    df.columns = ["District","Active","Confirmed","Deceased","Recovered"]
    df.set_index('District')
    return df



