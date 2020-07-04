from Get_KA_COVID_Data import get_KA_covid_data
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optim

def logistic_growth(t, a, b, c):
    return c / (1 + a * np.exp(-b*t))

class logoisticGrowthPredictor:
    def Predict_logistic_growth_confirmed(data,Number_days_tobe_predicted = 15):
        days = Number_days_tobe_predicted
        p0 = np.random.exponential(size=3)
        bounds = (0,[100000., 3., 1000000000.])
        (a,b,c),cov = optim.curve_fit(logistic_growth,data['timeStep'],data['Confirmed'],bounds=bounds,p0=p0)
        return data['Date'],data['timeStep'],np.arange(len(data),len(data)+days),data['Confirmed'],logistic_growth(data['timeStep'], a, b, c),logistic_growth(np.arange(len(data),len(data)+days), a, b, c)