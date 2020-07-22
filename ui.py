import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
import json
import pandas as pd
from COVID_Predictior import logoisticGrowthPredictor
from Get_KA_COVID_Data import get_KA_covid_data,getKAADistrictDropDownValue,get_districtWise
from app_figures import values,statepredictorGraph,stateDeseased,stateRecovered,stateActive
PLOTLY_LOGO = "https://www.codrindia.org/assets/images/logo/codr-icon-1.jpg"


import base64
#BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
#app = dash.Dash(external_stylesheets=[BS])

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
app = dash.Dash(external_stylesheets=[dbc.themes.SOLAR])
app.config['suppress_callback_exceptions'] = True
app.title = 'CODR'


body = html.Div([
html.Br()
,dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="40px")),
                    dbc.Col(dbc.NavbarBrand("CODR COVID-19 DASHBOARD", className="ml-2")),
                ],
                align='left',
                no_gutters=True,
            ),

        ),
        dbc.NavbarToggler(id="navbar-toggler"),

    ],
    color="dark",
    dark=True,
)


, dbc.Row([
        dbc.Col((html.Div(dbc.Alert("CASES IN KARNATAKA", color="light")),
                 html.Div(dbc.Alert([
                     html.H4("CONFIRMED", className="alert-no-fade"),

                     html.P(values()['CONFIRMED'])
                 ],color="warning", style={"height": "6rem"}
                 )),
                html.Div(dbc.Alert([
                 html.H4("RECOVERED", className="alert-heading"),

	             html.P(values()['RECOVERED'])
                ],style={"height": "6rem"}
                    )),
                 html.Div(dbc.Alert([
                     html.H4("DECEASED", className="alert-heading"),

                     html.P(values()['DECEASED'])
                 ],color="dark",style={"height": "6rem"}
                 )),
                 html.Div([
                     dcc.Graph(
                         figure=statepredictorGraph(),style={"height": "12rem"},
                     )
                 ])
                 ), md=3, xs=12)
        , dbc.Col((
                   html.Div(
                       
                       dcc.Tabs(id='tabs-example', value='tab-1', children=[
                        dcc.Tab(label= 'CODR predictor', value= 'tab-1',style=tab_style, selected_style=tab_selected_style),
                       dcc.Tab(label='Active', value='tab-2',style=tab_style, selected_style=tab_selected_style),
                       dcc.Tab(label='Recovered', value='tab-3',style=tab_style, selected_style=tab_selected_style),
                       dcc.Tab(label= 'Deceased', value= 'tab-4',style=tab_style, selected_style=tab_selected_style)
                        
                   ])),
                   html.Div(id='tabs-content1'),
                   html.Div(dbc.Alert("The first instance of the virus in the State of Karnataka was seen from a person with travel"
                                      " history from Dubai. Most of the cases that followed were present in patients who had an outside "
                                      "country travel history for the first fifteen days from the instance of virus in the state of  Karnataka."
                                      " The State Government and the citizens have excelled in its execution of protocols up until the date of June "
                                      "14th after which a spread rise is seen in most regions of the state. ", color="light"))),md =6 , xs =12)

        , dbc.Col((html.Div(dbc.Alert("Districts", color="light")),
dbc.Card(
    dbc.CardBody(
        [
            html.H4("PAC ANALYSIS", className="card-title"),
            html.H6("KA COVID-19 RATES", className="card-subtitle"),
            html.P(
                "MORTALITY RATE ",className="card-text",
            ),
            dbc.CardLink("Card link", href="#"),
            dbc.CardLink("External link", href="https://google.com"),
        ]
    )
        )), md=3, xs=12)
        ])
    ])
app.layout = html.Div([body])

@app.callback(Output('tabs-content1', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            dcc.Graph(
                figure=statepredictorGraph()
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
    app.run_server(debug = True)