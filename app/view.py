import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

from assets.database import db_session
from assets.models import Data


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

data = db_session.query(Data.date, Data.subscribers, Data.reviews).all()

dates = []
subscribers = []
reviews = []

for datum in data:
    dates.append(datum.date)
    subscribers.append(datum.subscribers)
    reviews.append(datum.reviews)

dif_subscribers = pd.Series(subscribers).diff().values
dif_reviews = pd.Series(reviews).diff().values

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
                        y=subscribers,
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
                               range=[min(subscribers) - 500, max(subscribers) + 500]),
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
                        y=reviews,
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
                               range=[0, max(reviews) + 500]),
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
