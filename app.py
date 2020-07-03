import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from COVID_Predictior import logoisticGrowthPredictor

app = dash.Dash(__name__)

dt,ts,pts,ad,cf,pda = logoisticGrowthPredictor.Predict_logistic_growth_confirmed()
dti = pd.date_range(dt[0], periods=len(ts)+len(pts), freq='D')


fig = go.Figure()
fig.add_trace(go.Scatter(x=dti[0:len(dt)-1].tolist(), y=cf,
                    mode='lines',
                    name='Curve Fixture'))
fig.add_trace(go.Scatter(x=dti[len(dt)-1:len(ts)+len(pts)].tolist(), y=pda,
                    mode='lines+markers',
                    name='Prediction'))
fig.add_trace(go.Scatter(x=dti[0:len(dt)-1].tolist(), y=ad,
                    mode='markers', name='Actual Data'))
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Number of confirmed cases",
)



app.layout = html.Div(children=[
    html.H1(children='COVID-19 Logistic growth - Karnataka',style={
            'textAlign': 'center',
        }),

    html.Div(children='''
        A logistic growth model to predict the number of cumulative cases in kaernataka for the next 15 days.
    ''',style={
            'textAlign': 'center',
        }),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port = 8080)