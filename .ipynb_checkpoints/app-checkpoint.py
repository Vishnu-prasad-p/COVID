import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from COVID_Predictior import logoisticGrowthPredictor
from Get_KA_COVID_Data import get_KA_covid_data,getKAADistrictDropDownValue,get_districtWise

app = dash.Dash(__name__)

data = get_KA_covid_data()
dt,ts,pts,ad,cf,pda = logoisticGrowthPredictor.Predict_logistic_growth_confirmed(data)
dti = pd.date_range(dt[0], periods=len(ts)+len(pts), freq='D')


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


app.layout = html.Div(children=[
    html.H1(children='COVID-19 Logistic growth - Karnataka',style={
            'textAlign': 'center',
        }),
    html.Div(children='''
        A logistic growth model to predict the number of cumulative cases in karnataka for the next 15 days.
    ''',style={
            'textAlign': 'center',
        }),

    dcc.Graph(
        id='State_cummulative_prediction',
        figure=fig_State
    ),
    html.H1(children='COVID-19 District wise - Karnataka',style={
            'textAlign': 'center',
        }),
    dcc.Dropdown(
        id='Select-District',
        options=getKAADistrictDropDownValue(),
        value='Bagalkote'
    ),
    dcc.Graph(id='district')
])

@app.callback(
    dash.dependencies.Output('district', 'figure'),
    [dash.dependencies.Input('Select-District', 'value')])

def update_output(value):
    dt1,ts1,pts1,ad1,cf1,pda1 = logoisticGrowthPredictor.Predict_logistic_growth_confirmed(get_districtWise(value))
    dti1 = pd.date_range(dt1[0], periods=len(ts1)+len(pts1), freq='D')
    fig_Dist = go.Figure()
    fig_Dist.add_trace(go.Scatter(x=dti1[0:len(dt1)-1].tolist(), y=cf1,
                    mode='lines',
                    name='Curve Fixture'))
    fig_Dist.add_trace(go.Scatter(x=dti1[len(dt1)-1:len(ts)+len(pts1)].tolist(),
                             y=pda1,
                        mode='lines+markers',
                        name='Prediction'))
    fig_Dist.add_trace(go.Scatter(x=dti1[0:len(dt1)-1].tolist(), y=ad1,
                        mode='markers', name='Actual Data'))

    fig_Dist.add_trace(go.Scatter(
        x=dti1[len(dt1)-1:len(ts1)+len(pts1)].tolist(),
        y=(pda1+(pda1*0.03)),
        fill='toself',
        fillcolor='rgba(0,100,80,0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name='Confidence Region',
    ))
    fig_Dist.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of confirmed cases",
    )

    return fig_Dist
    #     return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug = True)