import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
import json
import pandas as pd
from COVID_Predictior import logoisticGrowthPredictor

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
import json
import pandas as pd
from COVID_Predictior import logoisticGrowthPredictor
from Get_KA_COVID_Data import get_KA_covid_data, getKAADistrictDropDownValue, get_districtWise, allDistrictstabel
from app_figures import values, statepredictorGraph, stateDeseased, stateRecovered, stateActive, statePie, districtPie

PLOTLY_LOGO = "https://codrindia.in/assets/images/logo/codr-icon-1.jpg"
PLOTLY_LOGO1 ="https://pacindia.org/wp-content/uploads/2019/08/cropped-pacindia-logo-1.png"
# PLOTLY_LOGO1 = "https://sagesustainability.in/wp-content/uploads/2019/06/pac_logo.png"
import dash_table


df = allDistrictstabel()
from Get_KA_COVID_Data import get_KA_covid_data
import base64


# BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
# app = dash.Dash(external_stylesheets=[BS])

def generate_table(dataframe, max_rows=15):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


tabs_styles = {
    'height': '21px'
}
tab_style = {
    'borderBottom': '2px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'

}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'black',
    'padding': '7px'
}
search_bar = dbc.Row(
    [
        dbc.Col(html.Img(src=PLOTLY_LOGO1, height="40px")),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)
app = dash.Dash(external_stylesheets=[dbc.themes.SOLAR])
app.config['suppress_callback_exceptions'] = True
app.title = 'COVID Dashboard - Karnataka'

body = html.Div([
    html.H6(dbc.Badge("LIVE",href="#", color='warning', className="ml-1"))
    , dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="40px")),
                        dbc.Col(dbc.NavbarBrand("CODR COVID-19 DASHBOARD",className="ml-4"),sm=3, md=2),
                    ],
                    align='centre',
                    no_gutters=True,
                ),
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
        ],
        color="dark",
        dark=True,
    )

    , dbc.Row([
        dbc.Col((html.Div(dbc.Alert("CASES IN KARNATAKA", color="light")),
                 html.Div(dbc.Alert([
                     html.H4(values()['CONFIRMED'], className="alert-no-fade"),

                     html.P("CONFIRMED")
                 ], color="warning",  style={"height": "6rem"}
                 )),
                 html.Div(dbc.Alert([

                     html.H4(values()['Active'], className="alert-heading"),
                     html.P("ACTIVE")
                 ], style={"height": "6rem"}, color="info"
                 )),
                 html.Div(dbc.Alert([
                     html.H4(values()['DECEASED'], className="alert-heading"),

                     html.P("DECEASED")
                 ], color="secondary", style={"height": "6rem"}
                 )),
                 html.Div(dbc.Alert([
                     html.H4(values()['RECOVERED'], className="alert-heading"),
                     html.P("RECOVERED")
                 ], style={"height": "6rem"}
                 )),
                 html.Div([
                     dcc.Graph(
                         figure=statePie(),
                     )
                 ])
                 ), md=2, xs=12)
        , dbc.Col((
            html.Div(

                dcc.Tabs(id='tabs-example', value='tab-1', children=[
                    dcc.Tab(label='CODR predictor', value='tab-1', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Active', value='tab-2', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Recovered', value='tab-3', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Deceased', value='tab-4', style=tab_style, selected_style=tab_selected_style)

                ])),
            html.Div(id='tabs-content1'),
            html.Div(dbc.Alert([
                
                html.P("The CODR COVID-19 DASHBOARD is based on data available in the public domain. While every care is taken to develop an accurate prediction model, the model is prone to complex, evolving, and heterogeneous epidemiology of the COVID-19 disease. The predictions are subjected to an error rate of 10% or less, acceptable under prediction norms in Artificial Intelligence and Machine Learning."),

            html.P("The website and its contents herein, including analysis, mapping, and predictions are subjected to Copyright 2020 PAC."),

            html.P("Suggested Citation - Public Affairs Centre, Centre for Open Data Research. CODR COVID-19 DASHBOARD [Internet]. http://codrindia.in/. [cited Date]. Available from: http://codrindia.in")],
                               color="light"))), md=6, xs=12)

        , dbc.Col((html.Div(dbc.Alert("Districts", color="light")),
                   html.Div(
                       dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
        )
                   ), md=3, xs=12)
    ])
])
app.layout = html.Div([body])


@app.callback(Output('tabs-content1', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            dcc.Graph(
                figure=statepredictorGraph(), style={"height": "45rem"}
            )
        ])
    elif tab == 'tab-2':
        return html.Div([
            dcc.Graph(
                figure=stateActive()
            )
        ])
    elif tab == 'tab-3':
        return html.Div([
            dcc.Graph(
                figure=stateRecovered()
            )
        ])
    elif tab == 'tab-4':
        return html.Div([

            dcc.Graph(
                figure=stateDeseased()
            )
        ])

    elif tab == 'tab-5':
        return html.Div([
            html.H3('Tab content 2')
        ])

    elif tab == 'tab-6':
        return html.Div([
            html.H3('Tab content 2')
        ])


if __name__ == "__main__":
    app.run_server(debug=True)