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

os.chdir("D:/0 SEM 8 3-20-20/TA/Bimbingan 10")

df = pd.read_csv("visualisasi_lda_motivasi.csv")

#-------------------------------------------------------------------------------------

app = dash.Dash(__name__)

#-------------------------------------------------------------------------------------
app.layout = html.Div([

        html.Div([
            html.Pre(children= "Visualisasi Motivasi dengan LDA | Topik 1 Pergerakan Nasional",
            style={"text-align": "center", "font-size":"100%", "color":"black", "font-weight":"bold", "font-family":"Arial"})
            #html.Label(['Topik ke 0'],style={'font-weight': 'bold', 'font-family':'Arial'}),
        ]),

        html.Div([
            html.Label(['X-axis berdasarkan:'],style={'font-weight': 'bold', 'font-family':'Arial'}),
            dcc.RadioItems(
                id='xaxis_raditem',
                options=[
                         {'label': 'Kategori: Pergerakan Nasional', 'value': 'Kategori Topik 1'},
                         {'label': 'Detail Kata', 'value': 'Detail Topik 1'},
                ],
                value='Detail Topik 1',
                style={"width": "50%", 'font-family':'Arial'}
            ),
        ]),

        html.Div([
            html.Br(),
            html.Label(['Y-axis berdasarkan:'], style={'font-weight': 'bold', 'font-family':'Arial'}),
            dcc.RadioItems(
               id='yaxis_raditem',
                options=[
                         {'label': 'Probabilitas', 'value': 'Probabilitas Topik 1'}
                ],
                value='Probabilitas Topik 1',
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
            color='Probabilitas',
            barmode='stack',
            #category_orders={"Age": ["Motivasi", "Target"]}
            )

    barchart.update_layout(xaxis={'categoryorder':'array'},
                           title={'xanchor':'center', 'yanchor': 'top', 'y':0.9,'x':0.5,},
                           uniformtext_minsize=8, uniformtext_mode='hide',
                           showlegend=False,
                           margin=dict(l=20, r=20, t=20, b=20),
                           width=600)
    barchart.update_xaxes(automargin=True)
    #update_yaxes(automargin=True)
    #barchart.update_yaxes(title_text=' ')

    return (barchart)

if __name__ == '__main__':
    app.run_server(debug=True)