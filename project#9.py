import plotly 
plotly.tools.set_credentials_file(username='eungseon', api_key='ntzaOnpFsaTSJRRVYJPr')

import plotly.plotly as py
import plotly.graph_objs as go

stream_id = '6b14yummvl'
stream_1 = dict(token=stream_id, maxpoints=60)

trace1 = go.Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    stream=stream_1
)

data = go.Data([trace1])

layout = go.Layout(title='Time Series')
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='python-streaming')

s = py.Stream(stream_id)
s.open()

import datetime
import time
import random
import math

time.sleep(5)
degree = 10
temp = 10

while True:
    th = math.radians(degree)       # 각도를 theta(radian값)으로 변환
    k = math.radians(temp)
    
    sin_value = math.sin(th)
    y = k * sin_value
    
    # x축은 degree(각도), y축은 함수 y = ksinx 값
    # 처음에는 k = x이다가  각도가 720도가 되면 k값은 감소하기 시작
    # k가 어느 값 이하가 되면 다시 증가하고 이를 반복
    
    s.write(dict(x=degree, y=y))     
    time.sleep(0.1)
    
    
    if temp == 720:
        a = 1
    elif temp == 10:
        a = 0

    if a == 1:
        temp = temp - 10
    elif a == 0:
        temp = temp + 10

    degree = degree + 10
    

s.close()
