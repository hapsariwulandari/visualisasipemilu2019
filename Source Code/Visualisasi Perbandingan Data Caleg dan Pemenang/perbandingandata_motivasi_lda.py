# Bar charts are useful for displaying data that is classified into nominal or ordinal categories.
# A bar chart uses bars to show comparisons between categories of data. A bar chart will always have two axis.
# One axis will generally have numerical values, and the other will describe the types of categories being compared.

import pandas as pd #(version 0.24.2)
import datetime as dt
import dash         #(version 1.0.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly       #(version 4.4.1)
import plotly.express as px

import os, re, csv

os.chdir("D:/0 SEM 8 3-20-20/TA/Source Code/Visualisasi Perbandingan Data Caleg dan Pemenang")

df = pd.read_csv("perbandingandata_motivasi_lda.csv")

app = dash.Dash(__name__)

#-------------------------------------------------------------------------------------
app.layout = html.Div([

        html.Div([
            html.Pre(children= "Perbandingan Calon Legislatif dan Pemenang Pemilu 2019",
            style={"text-align": "center", "font-size":"150%", "color":"black", "font-weight":"bold", "font-family":"Arial"})
        ]),

        html.Div([
            html.Label(['X-axis berdasarkan:'],style={'font-weight': 'bold', 'font-family':'Arial'}),
            dcc.RadioItems(
                id='xaxis_raditem',
                options=[
                        {'label': 'Topik', 'value': 'Topik'},
                ],
                value='Tipe',
                style={"width": "50%", 'font-family':'Arial'}
            ),
        ]),

        html.Div([
            html.Br(),
            html.Label(['Y-axis berdasarkan:'], style={'font-weight': 'bold', 'font-family':'Arial'}),
            dcc.RadioItems(
               id='yaxis_raditem',
                options=[
                        {'label': 'Jumlah', 'value': 'Angka'},
                        {'label': 'Jumlah Caleg', 'value': 'Angka Caleg'},
                        {'label': 'Jumlah Pemenang', 'value': 'Angka Pemenang'},
                ],
                value='Angka',
                style={"width": "50%", 'font-family':'Arial'}
            ),
        ]),

    html.Div([
        dcc.Graph(id='the_graph')
    ]),

])

#-------------------------------------------------------------------------------------
@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='xaxis_raditem', component_property='value'),
     Input(component_id='yaxis_raditem', component_property='value')]
)

def update_graph(x_axis, y_axis):

    dff = df 
    # print(dff[[x_axis,y_axis]][:1])
 
    barchart=px.bar(
            data_frame=dff,
            x=x_axis,
            y=y_axis,
            #title=y_axis+': by '+x_axis,
            #facet_col='Isu',
            color='Tipe',
            barmode='group',
            #category_orders={"Age": ["Motivasi", "Target"]}
            )

    barchart.update_layout(xaxis={'categoryorder':'array'},
                           title={'xanchor':'center', 'yanchor': 'top', 'y':0.9,'x':0.5,},
                           uniformtext_minsize=8, uniformtext_mode='hide')
    #barchart.update_xaxes(title_text=' ')
    #barchart.update_yaxes(title_text=' ')

    return (barchart)

if __name__ == '__main__':
    app.run_server(debug=True)