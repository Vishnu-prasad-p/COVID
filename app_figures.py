import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from COVID_Predictior import logoisticGrowthPredictor
from Get_KA_COVID_Data import get_KA_covid_data,getKAADistrictDropDownValue,get_districtWise,allDistrictstabel

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
        font_color="white",
        font_size=18
    )
    fig_State.layout.plot_bgcolor = '#002b36'
    fig_State.layout.paper_bgcolor = '#002b36'
    fig_State.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))
    return fig_State


def stateDeseased():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'].to_list()[0:len(data['Date'].to_list())-1], y=data['Deceased'].to_list(),
                    mode='lines+markers',
                    line=dict(color='white')))
    fig.layout.plot_bgcolor = '#002b36'
    fig.layout.paper_bgcolor = '#002b36'
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number Of Deseased Cases",
        font_color="white",
        font_size=18
    )
    return fig


def stateRecovered():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'].to_list()[0:len(data['Date'].to_list())-1], y=data['Recovered'].to_list(),
                    mode='lines+markers',
                    line=dict(color='green')))
    fig.layout.plot_bgcolor = '#002b36'
    fig.layout.paper_bgcolor = '#002b36'
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number Of Recovered Cases",
        font_color="white",
        font_size=18
    )
    return fig

def stateActive():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'].to_list()[0:len(data['Date'].to_list())-1], y=(data['Confirmed']-data['Recovered']-data['Deceased']).to_list(),
                    mode='lines+markers',
                    line=dict(color='red')))
    fig.layout.plot_bgcolor = '#002b36'
    fig.layout.paper_bgcolor = '#002b36'
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number Of Active Cases",
        font_color="white",
        font_size=18
    )
    return fig

def districtPie():
    df = allDistrictstabel()
#     fig = px.pie(df, values='Confirmed', names='District', color='District',
#              color_discrete_map={'Thur':'lightcyan',
#                                  'Fri':'cyan',
#                                  'Sat':'royalblue',
#                                  'Sun':'darkblue'})
    
    
#     df = px.data.gapminder().query("year == 2007").query("continent == 'Americas'")
    fig = px.pie(df, values='Confirmed', names='District',
             hover_data=['Confirmed'], labels={'Confirmed':'Confirmed'})
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    
    
    fig.layout.plot_bgcolor = '#002b36'
    fig.layout.paper_bgcolor = '#002b36'
    fig.update_layout(
        showlegend=False,
        font_color="white",
        font_size=18
    )
    return fig


def statePie():
    labels = ['Active','Recovered','Deceased']
    values = [(data['Confirmed']-data['Recovered']-data['Deceased']).iloc[-1], data['Recovered'].iloc[-1], data['Deceased'].iloc[-1]]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values,hole=.4)])
    fig.layout.plot_bgcolor = '#002b36'
    fig.layout.paper_bgcolor = '#002b36'
    fig.update_layout(
        font_color="white",
        font_size=18
    )
    return fig