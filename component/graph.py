import dash
from dash import html, dcc, callback, Input, Output
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

from inputdata.data import app_usage_time, today_index, unlock


weekly_usage = app_usage_time[today_index-6:today_index+1]
weekly_usage['date']=pd.to_datetime(weekly_usage['date'], format = "%Y %m %d")
weekly_usage['date']=weekly_usage['date'].dt.strftime('%m/%d')

today_usage_warning = usage_time_info['hour']*60+usage_time_info['minite']
today_unlock_warning = unlock_info['time']
app_usage_warning = app_usage_info['hour']*60+app_usage_info['minite']

target_app = app_usage_info['app']


def usage_graph():
    COLORS = ['rgba(164,189,133,0.6)'] * 7
    
    for i in range(0,7):
        if (weekly_usage["Total"].values.tolist()[i]>today_usage_warning):
            COLORS[i] = 'rgba(221,151,151,0.6)'
    
    fig = px.bar(weekly_usage, x="date", y="Total", width=500, height=300)
    fig.update_traces(marker_color=COLORS)
    fig.update_layout(
        xaxis = dict(
            title = None,
            tickmode = 'array',
            showline=True, linewidth=1, linecolor='#BEBEBE',
            
        ),
        yaxis = dict(
            
            tickmode = 'array',
            tickvals = [0,120,240,360,480,600,720],
            ticktext = ['0', '2', '4', '6', '8', '10','12'],
            showgrid=True, linewidth=1,gridcolor='#E0E0E0',
            tickfont = dict(size=9)
        )
    )
    fig.update_layout(showlegend=False, plot_bgcolor='white',paper_bgcolor="rgb(0,0,0,0)",bargap=0.3)
    fig.add_hline(y=today_usage_warning, line_dash="dash", line_color="#D78A8A", annotation_text="warning!", 
              annotation_position="top right",annotation_font_size= 12, annotation_font_color='#D78A8A')
    
    fig.update_layout(
        hoverlabel=dict(
            bordercolor="rgba(0, 0, 0, 0.6)",
            bgcolor="rgba(255, 255, 255,0.8)",
            font_size=14,
            ),
            hoverlabel_namelength=100
            )
    fig.update_traces(
        hovertemplate="%{y} minutes")
    
    return fig 
    
def unlock_graph():
    weekly_unlock = unlock[today_index-6:today_index+1]
    weekly_unlock['date']=weekly_usage['date']
    color = [
        '#E4AE44' if v < app_usage_warning else '#E46060'
        for v in weekly_unlock['unlock']
    ]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=weekly_unlock['date'], y=weekly_unlock['unlock'], mode='lines+markers', line_color='#E4AE44',
                            marker=dict(
                                    color='white',
                                    size=12,
                                    line=dict(color= color,width=2)
                                )))

    fig.update_layout(
        xaxis = dict(
            title = None,
            tickmode = 'array',
            showline=True, linewidth=1, linecolor='#BEBEBE',
        ),
        yaxis =dict(
            showgrid=True, linewidth=1,gridcolor='#E0E0E0',
        )
    )
    fig.update_layout(
        hoverlabel=dict(
            bordercolor="rgba(0, 0, 0, 0.6)",
            bgcolor="rgba(255, 255, 255,0.8)",
            font_size=14,
            ),
            hoverlabel_namelength=100
            )
    fig.update_traces(
        hovertemplate="%{y} times"+'<extra></extra>')

    fig.update_layout(showlegend=False, plot_bgcolor='white',paper_bgcolor="rgb(0,0,0,0)",width=510, height=320)
    fig.add_hline(y=today_unlock_warning, line_dash="dash", line_color="#D78A8A",annotation_text="warning!", 
              annotation_position="top right",annotation_font_size= 12, annotation_font_color='#D78A8A')
    return fig 

def app_usage_graph():
    COLORS = ['rgba(104,105,134,0.6)'] * 7
    # app_usage = weekly_usage.loc[weekly_usage['']]
    
    for i in range(0,7):
        if (weekly_usage[target_app].values.tolist()[i]>app_usage_warning):
            COLORS[i] = 'rgba(221,151,151,0.6)'
    
    fig = px.bar(weekly_usage, x="date", y=target_app, width=500, height=300)
    fig.update_traces(marker_color=COLORS)
    fig.update_layout(
        xaxis = dict(
            title = None,
            tickmode = 'array',
            showline=True, linewidth=1, linecolor='#BEBEBE',
            
        ),
        yaxis = dict(
            
            tickmode = 'array',
            tickvals = [0,60,120,180,240],
            ticktext = ['0', '1', '2', '3', '4'],
            showgrid=True, linewidth=1,gridcolor='#E0E0E0',
            tickfont = dict(size=9)
        )
    )
    fig.update_layout(
        hoverlabel=dict(
            bordercolor="rgba(0, 0, 0, 0.6)",
            bgcolor="rgba(255, 255, 255,0.8)",
            font_size=14,
            ),
            hoverlabel_namelength=100
            )
    fig.update_traces(
        hovertemplate="%{y} minutes")
    
    fig.update_layout(showlegend=False, plot_bgcolor='white',paper_bgcolor="rgb(0,0,0,0)",bargap=0.3)
    fig.add_hline(y=app_usage_warning, line_dash="dash", line_color="#D78A8A", annotation_text="warning!", 
              annotation_position="top right",annotation_font_size= 12, annotation_font_color='#D78A8A')
    
    return fig 