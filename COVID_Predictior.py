from Get_KA_COVID_Data import get_KA_covid_data
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optim

def logistic_growth(t, a, b, c):
    return c / (1 + a * np.exp(-b*t))

class logoisticGrowthPredictor:
    def Predict_logistic_growth_confirmed(Number_days_tobe_predicted = 15):
        days = Number_days_tobe_predicted
        data = get_KA_covid_data()
        p0 = np.random.exponential(size=3)
        bounds = (0,[100000., 3., 1000000000.])
        (a,b,c),cov = optim.curve_fit(logistic_growth,data['timeStep'],data['Confirmed'],bounds=bounds,p0=p0)
#         plt.figure(figsize=[20, 10])
#         plt.scatter(data['timeStep'],data['Confirmed'],c='r',label="Data")
#         plt.plot(data['timeStep'],logistic_growth(data['timeStep'], a, b, c),label="Fixed Curve")
#         plt.plot((np.arange(len(data),len(data)+days)),logistic_growth(np.arange(len(data),len(data)+days), a, b, c),label="Prediction")
#         plt.legend()
        return data['Date'],data['timeStep'],np.arange(len(data),len(data)+days),data['Confirmed'],logistic_growth(data['timeStep'], a, b, c),logistic_growth(np.arange(len(data),len(data)+days), a, b, c)
        
#     def Predict_logistic_growth_deceased(Number_days_tobe_predicted = 15):
#         days = Number_days_tobe_predicted
#         data = get_KA_covid_data()
#         p0 = np.random.exponential(size=3)
#         bounds = (0,[100000., 3., 1000000000.])
#         (a,b,c),cov = optim.curve_fit(logistic_growth,data['timeStep'],data['Deceased'],bounds=bounds,p0=p0)
#         plt.figure(figsize=[20, 10])
#         plt.scatter(data['timeStep'],data['Deceased'],c='r',label="Data")
#         plt.plot(data['timeStep'],logistic_growth(data['timeStep'], a, b, c),label="Fixed Curve")
#         plt.plot((np.arange(len(data),len(data)+days)),logistic_growth(np.arange(len(data),len(data)+days), a, b, c),label="Prediction")
#         plt.legend()
        
#     def Predict_logistic_growth_recovered(Number_days_tobe_predicted = 15):
#         days = Number_days_tobe_predicted
#         data = get_KA_covid_data()
#         p0 = np.random.exponential(size=3)
#         bounds = (0,[100000., 3., 1000000000.])
#         (a,b,c),cov = optim.curve_fit(logistic_growth,data['timeStep'],data['Recovered'],bounds=bounds,p0=p0)
#         plt.figure(figsize=[20, 10])
#         plt.scatter(data['timeStep'],data['Recovered'],c='r',label="Data")
#         plt.plot(data['timeStep'],logistic_growth(data['timeStep'], a, b, c),label="Fixed Curve")
#         plt.plot((np.arange(len(data),len(data)+days)),logistic_growth(np.arange(len(data),len(data)+days), a, b, c),label="Prediction")
#         plt.legend()