import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd


netflix = pd.read_csv('netflix_titles.csv')
netflix1 = pd.read_csv('netflix_titles.csv')


app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([

    html.Div([
        html.Div([
            html.Div([
                html.H3('Netflix Movies and TV Shows', style = {'margin-bottom': '0px', 'color': 'white'}),
            ])
        ], className = "create_container1 four columns", id = "title"),

    ], id = "header", className = "row flex-display", style = {"margin-bottom": "25px"}),

    html.Div([
        html.Div((
            html.P('Filter by Release Year', className = 'fix_label', style = {'text-align': 'center', 'color': 'white'}),
            dcc.Slider(id = 'slider_year',
                       included = True,
                       updatemode='drag',
                       tooltip={'always_visible': True},
                       min = 1925,
                       max = 2020,
                       step = 1,
                       value = 2009,
                       marks = {str(yr): str(yr) for yr in range(1925, 2020, 10)},
                       className = 'dcc_compon'),


        ), className = "create_container2 six columns", style = {'margin-bottom': '30px'}),

    ], className = "row flex-display"),

    html.Div([
        html.Div([
            dcc.Graph(id = 'line_chart',
                      config = {'displayModeBar': 'hover'}),

        ], className = "create_container2 eight columns"),

    ], className = "row flex-display"),

], id= "mainContainer", style={"display": "flex", "flex-direction": "column"})


@app.callback(Output('line_chart', 'figure'),
              [Input('slider_year', 'value')])
def update_graph(slider_year):
    type_movie = netflix[(netflix['type'] == 'Movie')][['type', 'release_year']]
    type_movie['type1'] = type_movie['type']
    type_movie_1 = type_movie.groupby(['release_year', 'type1'])['type'].count().reset_index()
    filter_movie = type_movie_1[(type_movie_1['release_year'] >= slider_year)]

    type_tvshow = netflix1[(netflix1['type'] == 'TV Show')][['type', 'release_year']]
    type_tvshow['type2'] = type_tvshow['type']
    type_tvshow_1 = type_tvshow.groupby(['release_year', 'type2'])['type'].count().reset_index()
    filter_tvshow = type_tvshow_1[(type_tvshow_1['release_year'] >= slider_year)]


    return {
        'data':[go.Scatter(
                    x=filter_movie['release_year'],
                    y=filter_movie['type'],
                    mode = 'markers+lines',
                    name='Movie',
                    line = dict(shape = "spline", smoothing = 1.3, width = 3, color = 'green'),
                    marker = dict(size = 10, symbol = 'circle', color = 'white',
                          line = dict(color = 'orange', width = 2)
                          ),

                  hoverinfo='text',
                  hovertext=
                  '<b>Release Year</b>: ' + filter_movie['release_year'].astype(str) + '<br>' +
                  '<b>Type</b>: ' + filter_movie['type1'].astype(str) + '<br>' +
                  '<b>Count</b>: ' + [f'{x:,.0f}' for x in filter_movie['type']] + '<br>'



              ),

            go.Scatter(
                x = filter_tvshow['release_year'],
                y = filter_tvshow['type'],
                mode = 'markers+lines',
                name = 'TV Show',
                line = dict(shape = "spline", smoothing = 1.3, width = 3, color = '#FF00FF'),
                marker = dict(size = 10, symbol = 'circle', color = 'white',
                              line = dict(color = '#FF00FF', width = 2)
                              ),

                hoverinfo = 'text',
                hovertext =
                '<b>Release Year</b>: ' + filter_tvshow['release_year'].astype(str) + '<br>' +
                '<b>Type</b>: ' + filter_tvshow['type2'].astype(str) + '<br>' +
                '<b>Count</b>: ' + [f'{x:,.0f}' for x in filter_tvshow['type']] + '<br>'

            )],


        'layout': go.Layout(
            # barmode = 'group',
             plot_bgcolor='#1f2c56',
             paper_bgcolor='#1f2c56',
             title={
                'text': 'Movies and TV Shows by Release Year',

                'y': 0.98,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': 'white',
                        'size': 15},

             hovermode='x',

             xaxis=dict(title='<b>Card Category</b>',
                        # tick0=0,
                        # dtick=1,
                        color='white',
                        showline=True,
                        showgrid=True,
                        linecolor='white',
                        linewidth=1,


                ),

             yaxis=dict(title='<b>Count</b>',
                        color='white',
                        showline=False,
                        showgrid=True,
                        linecolor='white',

                ),

            legend = {
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},
            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'white')


                 )

    }


if __name__ == '__main__':
    app.run_server(debug=True)