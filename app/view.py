import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# 可視化するデータの取得
df = pd.read_csv("assets/data.csv")

dates = []
for _date in df['date']:
    dates.append(datetime.strptime(_date, '%Y/%m/%d').date())

n_subscribers = df['subscribers'].values
n_reviews = df['reviews'].values

dif_subscribers = df['subscribers'].diff().values
dif_reviews = df['reviews'].diff().values

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# 可視化部分
app.layout = html.Div(children=[
    html.H2(children='PythonによるWebスクレイピング'),
    html.Div(children=[
        dcc.Graph(
            id='subscriber_graph',
            figure={
                'data': [
                    go.Scatter(
                        x=dates,
                        y=n_subscribers,
                        mode='lines+markers',
                        name='受講生総数',
                        opacity=0.7,
                        yaxis='y1'
                    ),
                    go.Bar(
                        x=dates,
                        y=dif_subscribers,
                        name='増加人数',
                        yaxis='y2'
                    )
                ],
                'layout': go.Layout(
                    title='受講生総数の推移',
                    xaxis=dict(title='date'),
                    yaxis=dict(title='受講生総数', side='left', showgrid=True,
                               range=[min(n_subscribers) - 500, max(n_subscribers) + 500]),
                    yaxis2=dict(title='増加人数', side='right', showgrid=False,
                                range=[0, max(dif_subscribers[1:]) + 20], overlaying='y'),
                    margin=dict(l=200, r=200, b=100, t=100)
                )
            }
        )
    ]),
    html.Div(children=[
        dcc.Graph(
            id='review_graph',
            figure={
                'data': [
                    go.Scatter(
                        x=dates,
                        y=n_reviews,
                        mode='lines+markers',
                        name='レビュー総数',
                        opacity=0.7,
                        yaxis='y1'
                    ),
                    go.Bar(
                        x=dates,
                        y=dif_reviews,
                        name='増加人数',
                        yaxis='y2'
                    )
                ],
                'layout': go.Layout(
                    title='レビュー総数の推移',
                    xaxis=dict(title='date'),
                    yaxis=dict(title='レビュー総数', side='left', showgrid=True,
                               range=[0, max(n_reviews) + 500]),
                    yaxis2=dict(title='増加人数', side='right', showgrid=False,
                                range=[0, max(dif_reviews[1:]) + 20], overlaying='y'),
                )
            }
        )
    ])
],style={
    'textAlgin': 'center',
    'width': '1200px',
    'margin': '0 auto'
})

if __name__ == '__main__':
    app.run_server(debug=True)
