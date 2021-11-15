

from os import name
import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output  
from dash import *
import flask
from waitress import *

 


flask_server = flask.Flask(__name__)
app = dash.Dash(__name__,server=flask_server,external_stylesheets=[dbc.themes.CYBORG])



df1=pd.read_csv('new_df_2.csv')
df2=df1[['Year_Reported','CDP_Region','City','Gases_Included','Change_in_emissions','TOTAL_Scope_1_2_3','Scope1','Scope2','Scope3','long','lat']]
filter=df2['TOTAL_Scope_1_2_3']!=0
df2=df2[filter]
df2.groupby(["CDP_Region"])
df2.dropna()
df2 = df2.sort_values(by=["TOTAL_Scope_1_2_3"], ascending=False)
df2.reset_index(drop=True, inplace=True)
print(df2)

        
tuple1 = (0, df2[df2.TOTAL_Scope_1_2_3 > 120000000].index[-1]+1)
tuple2 = (tuple1[1], df2[(df2.TOTAL_Scope_1_2_3 >  100000000) & (df2.TOTAL_Scope_1_2_3 <=120000000)].index[-1]+1)
tuple3 = (tuple2[1], df2[(df2.TOTAL_Scope_1_2_3 >  90000000) & (df2.TOTAL_Scope_1_2_3 <= 100000000)].index[-1]+1)
tuple4 = (tuple3[1], df2[(df2.TOTAL_Scope_1_2_3 >  80000000) & (df2.TOTAL_Scope_1_2_3 <=  90000000)].index[-1]+1)
tuple5 = (tuple4[1], df2[(df2.TOTAL_Scope_1_2_3 >  70000000) & (df2.TOTAL_Scope_1_2_3 <=  80000000)].index[-1]+1)
tuple6 = (tuple5[1], df2[(df2.TOTAL_Scope_1_2_3 >  60000000) & (df2.TOTAL_Scope_1_2_3 <=  70000000)].index[-1]+1)
tuple7 = (tuple6[1], df2[(df2.TOTAL_Scope_1_2_3>   50000000) & (df2.TOTAL_Scope_1_2_3 <=  60000000)].index[-1]+1)
tuple8 = (tuple7[1], df2[(df2.TOTAL_Scope_1_2_3>   40000000) & (df2.TOTAL_Scope_1_2_3 <=  50000000)].index[-1]+1)
tuple9 = (tuple8[1], df2[(df2.TOTAL_Scope_1_2_3>   30000000) & (df2.TOTAL_Scope_1_2_3 <=  40000000)].index[-1]+1)
tuple10 = (tuple9[1], df2[(df2.TOTAL_Scope_1_2_3>  20000000) & (df2.TOTAL_Scope_1_2_3 <=  30000000)].index[-1]+1)
tuple11 = (tuple10[1], df2[(df2.TOTAL_Scope_1_2_3> 10000000) & (df2.TOTAL_Scope_1_2_3 <=  20000000)].index[-1]+1)
tuple12 = (tuple11[1], df2[(df2.TOTAL_Scope_1_2_3> 1000000) & (df2.TOTAL_Scope_1_2_3 <=  10000000)].index[-1]+1)
tuple13 = (tuple12[1], df2[df2.TOTAL_Scope_1_2_3 <=1000000].index[-1]+1)
stages = ["120M+", "100M-120M", "90M-100M", "80M-90M", "70M-80M", "60M-70M",
         "50M-60M", "40M-50M", "30M-40M","20M-30M","10M-20M",'1M-10M','1-1M']

limits=[tuple1, tuple2, tuple3, tuple4, tuple5, tuple6, tuple7, tuple8, tuple9,tuple10,tuple11,tuple12,tuple13]

colorz = ["#CC0000","#CE1620","#E34234","#CD5C5C","#FF0000", "#FF1C00", "#FF6961","#FFC3C3","#E8C3FF","#C8B4FD","#8982E8","#5F56DC","#352BB9"  ]
# ------------------------------------------------------------------------------


app.layout = html.Div([
    html.H1("Emissions Around The World", style={'text-align': 'center','color':'white','font-family':'Courier New','font-size':20}),
    html.H2("CPD data presentation", style={'text-align': 'center','color':'white','font-family':'monospace'}),
    dash.dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2019", "value":2019},
                     {"label": "2020", "value":2020},
                     {"label": "2021", "value":2021}],
                 multi=False,
                 value=2019,
                 style={'width': "40%"}
                 ),

    
    html.Div(id='output_container', children=[]),
     html.Br(),
     html.Br(),
   dbc.Row( [ 
    dbc.Col(dash.dcc.Graph(id='output-graph2', figure={}),width=5, lg={'size': 5,  "offset": 0, 'order': 'first'}), 
    dbc.Col(dash.dcc.Graph(id='output-graph', figure={}), width=5, lg={'size': 5,  "offset": 0, 'order': 'last'})                
   
                        
 ])
])


# ------------------------------------------------------------------------------

@app.callback(
    [
    Output(component_id='output_container', component_property='children'),
     Output(component_id='output-graph', component_property='figure'),
      Output(component_id='output-graph2', component_property='figure'),
      Input(component_id='slct_year', component_property='value')
    ])
    
    
def update_graph(option_slctd):
 
    container = "The year chosen by user was: {}".format(option_slctd)
    dff = df2.copy()
    dff = dff[dff["Year_Reported"] == option_slctd]
    print(dff)
    stages = ["120M+", "100M-120M", "90M-100M", "80M-90M", "70M-80M", "60M-70M",
         "50M-60M", "40M-50M", "30M-40M","20M-30M","10M-20M",'1M-10M','1-1M']




    fig = go.Figure()
    stage_counter = 0
    for i in range(len(limits)):
        lim = limits[i]
        df_sub = dff[lim[0]:lim[1]]
        fig.add_trace(go.Scattergeo(
            lon = df_sub['long'],
            lat = df_sub['lat'],
            hovertext=df_sub[['CDP_Region','City','Scope1','Scope2','Scope3','TOTAL_Scope_1_2_3','Gases_Included','Change_in_emissions']],
            locationmode = 'ISO-3',
            customdata=df_sub[['CDP_Region','City','Scope1','Scope2','Scope3','TOTAL_Scope_1_2_3','Gases_Included','Change_in_emissions']],
            marker = dict(
                size = df_sub['TOTAL_Scope_1_2_3']*0.000002,
                color = colorz[i],
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode='area'
            ),
            name = '{}'.format(stages[stage_counter])))   
        stage_counter = stage_counter+1
        
         
    fig.update_geos(bgcolor= 'rgba(0,0,0,0)',
    showland=True,
    showcountries=True,countrycolor="#333300",projection_type="orthographic",oceancolor='#051D53',showocean=True,landcolor='#244804', showlakes=True, lakecolor='#0A3E63',
    showrivers=True, rivercolor="#2B3856")
    layout=fig.update_layout(height=400,width=650,margin={"r":20,"t":0,"l":5,"b":0},paper_bgcolor='rgb(0,0,0)'
, plot_bgcolor='rgb(0,0,0)', geo=dict(bgcolor= 'rgba(0,0,0,0)'),font_color='white')


    fig.update_yaxes(visible=False, showticklabels=False) 
    fig.update_xaxes(visible=False, showticklabels=False)
    fig.update_traces(
    hovertemplate="<br>".join([
        "CPD_Region: %{customdata[0]}",
        "City: %{customdata[1]}",
        "Scope1: %{customdata[2]}",
        "Scope2: %{customdata[3]}",
        "Scope3: %{customdata[4]}",
        "Total_Emissions: %{customdata[5]}",
        "Co2e: %{customdata[6]}",
        "Status: %{customdata[7]}"
    ])
) 


    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
    y=dff['CDP_Region'],
    x=dff['Scope1'],
    name='Scope1',
    orientation='h',
    marker=dict(
    color='#4B0082'
     )
))
    fig2.add_trace(go.Bar(
    y=dff['CDP_Region'],
    x=dff['Scope2'],
    name='Scope2',
    orientation='h',
    marker=dict(
        color='cyan'
    )
))
    fig2.add_trace(go.Bar(
    y=dff['CDP_Region'],
    x=dff['Scope3'],
    name='Scope3',
    orientation='h',
    marker=dict(
        color='#FFFFE0'
    )
))
    fig2.update_layout(barmode='stack',height=400,width=400,margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='rgb(0,0,0)'
    , plot_bgcolor='rgb(0,0,0)', font_color='white')
    fig2.update_xaxes(visible=False, showticklabels=False,showgrid=False)
    fig2.update_yaxes(visible=False, showticklabels=False,showgrid=False)
    

    
    return  container,fig,fig2
   

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run_server(debug=True)
serve(app.server, host="0.0.0.0", port=8050)
