import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from COVID_Predictior import logoisticGrowthPredictor
from Get_KA_COVID_Data import get_KA_covid_data,getKAADistrictDropDownValue,get_districtWise

data = get_KA_covid_data()
dt,ts,pts,ad,cf,pda = logoisticGrowthPredictor.Predict_logistic_growth_confirmed(data)
dti = pd.date_range(dt[0], periods=len(ts)+len(pts), freq='D')

def values():
    return {
        "CONFIRMED": data['Confirmed'].iloc[-1],
        "RECOVERED": data['Recovered'].iloc[-1],
        "DECEASED": data['Deceased'].iloc[-1],
        "Active": (data['Confirmed']-data['Recovered']-data['Deceased']).iloc[-1]
    }


def statepredictorGraph():
    fig_State = go.Figure()
    fig_State.add_trace(go.Scatter(x=dti[0:len(dt)-1].tolist(), y=cf,
                        mode='lines',
                        name='Curve Fixture'))
    fig_State.add_trace(go.Scatter(x=dti[len(dt)-1:len(ts)+len(pts)].tolist(),
                             y=pda,
                        mode='lines+markers',
                        name='Prediction'))
    fig_State.add_trace(go.Scatter(x=dti[0:len(dt)-1].tolist(), y=ad,
                        mode='markers', name='Actual Data'))

    fig_State.add_trace(go.Scatter(
        x=dti[len(dt)-1:len(ts)+len(pts)].tolist(),
        y=(pda+(pda*0.03)),
        fill='toself',
        fillcolor='rgba(0,100,80,0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name='Confidence Region',
    ))
    fig_State.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of confirmed cases",
    )
    return fig_State


def stateDeseased():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'].to_list(), y=data['Deceased'].to_list(),
                    mode='lines+markers',
                    name='lines+markers',line=dict(color='royalblue', width=4, dash='dot')))
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number Of Deseased Cases",
    )
    return fig


def stateRecovered():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'].to_list(), y=data['Recovered'].to_list(),
                    mode='lines+markers',
                    name='lines+markers'))
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number Of Recovered Cases",
    )
    return fig

def stateActive():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'].to_list(), y=(data['Confirmed']-data['Recovered']-data['Deceased']).to_list(),
                    mode='lines+markers',
                    name='lines+markers'))
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number Of Active Cases",
    )
    return fig