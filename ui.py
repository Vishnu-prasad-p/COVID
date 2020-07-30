import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
import json
import pandas as pd
from COVID_Predictior import logoisticGrowthPredictor
from Get_KA_COVID_Data import get_KA_covid_data,getKAADistrictDropDownValue,get_districtWise,allDistrictstabel
from app_figures import values,statepredictorGraph,stateDeseased,stateRecovered,stateActive,statePie,districtPie
PLOTLY_LOGO = "https://www.codrindia.org/assets/images/logo/codr-icon-1.jpg"
import dash_table

df = allDistrictstabel()
from Get_KA_COVID_Data import get_KA_covid_data
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
html.H6("LIVE")
,dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="40px")),
                    dbc.Col(dbc.NavbarBrand("CODR COVID-19 DASHBOARD", className="ml-2")),
                ],
                align='centre',
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

                     html.H4("ACTIVE", className="alert-heading"),
                     html.P(values()['Active'])
                ],style={"height": "6rem"},color="danger"
                    )),
                 html.Div(dbc.Alert([
                     html.H4("DECEASED", className="alert-heading"),

                     html.P(values()['DECEASED'])
                 ],color="dark",style={"height": "6rem"}
                 )),
                    html.Div(dbc.Alert([
                    html.H4("RECOVERED", className="alert-heading"),
	             html.P(values()['RECOVERED'])
                 ],style={"height": "6rem"}
                 )),
                 html.Div([
                     dcc.Graph(
                         figure=statePie(),
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
                   html.Div(dbc.Alert("The model are inaccurate to the complex, evolving, and heterogeneous realities"
                                        " of different uncertainties. Predictions are uncertain by nature and take into account an error of <10% which is acceptable"
                                        " under prediction norms in Artificial Intelligence and Machine learning.This website and its contents herein, including all data, mapping, and analysis are copyright 2020 PAC, all rights reserved. When linking to the website, attribute the Website as the COVID-19 Dashboard by the Center for Open Data Research, India", color="light"))),md =6 , xs =12)

        , dbc.Col((html.Div(dbc.Alert("Districts", color="light")),
html.Div([
            dcc.Graph(
                figure=districtPie(),style={"height": "35rem"},
            )
        ]),html.Div(dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns],
    page_action='none',
    style_table={'height': '250px', 'overflowY': 'auto'},
    style_header={'backgroundColor': '#002b36'}, style_cell={ 'backgroundColor': '#002b36', 'color': 'white' }
)
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
                figure=statepredictorGraph(),style={"height": "45rem"}
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