# built-in modules
import base64
import datetime
import io

# dash modules
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# graphing
import plotly.express as px

# data frames
import pandas as pd

# my modules
import mpt
import uts

# security
import dash_auth
from users import USERNAME_PASSWORD_PAIRS


# initial configuration
app = dash.Dash(__name__, suppress_callback_exceptions=True)
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)

data_set = None

# base layout structure & behaviour
app.layout = html.Div([
    html.Br(),
    dcc.Tabs(id='main-tabs', value='tab-upload', children=[
        dcc.Tab(label='Upload File', value='tab-upload'),
        dcc.Tab(label='View Data', value='tab-view'),
        dcc.Tab(label='Create Portfolio', value='tab-mpt'),
        dcc.Tab(label='Check Statistics', value='tab-stat'),
    ]),
    html.Div(id='main-tab-content', style={'background-color': '#f9f9f9'})
], style={'width': '90%', 'margin': 'auto'})


@app.callback(Output('main-tab-content', 'children'),
              Input('main-tabs', 'value'))
def route_content(tab):
    if tab == 'tab-upload':
        return render_upload_tab()
    elif tab == 'tab-view' and data_set is not None:
        return render_data_view_tab()
    elif tab == 'tab-mpt' and data_set is not None:
        return render_portfolio_page()
    elif tab == 'tab-stat' and data_set is not None:
        return render_stat_tab()
    else:
        return html.Div([
            html.Br(),
            html.Div(['You have to upload the data first.'],  style=uts.up_style_1),
            html.Br()
        ], style=uts.box_style)


# upload page
def render_upload_tab():
    return html.Div([
        html.Br(),
        html.Br(),

        html.Div([
            html.Div([
                uts.upload_tab_description
            ], style=uts.up_style_1)
        ], style=uts.box_style),

        html.Br(),

        # upload bar
        html.Div([
            dcc.Upload(id='upload-data', children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
                       style=uts.upload_bar_style, multiple=False)
        ], style=uts.box_style),
        html.Br(),
        html.Div([
            html.Div(id='output-data-upload'),
        ], style=uts.up_style_4),

        html.Hr(),

        html.Div([
            html.Div(['Expected form of csv file:'], style=uts.up_style_2),

        ], style=uts.box_style),

        html.Br(),

        dash_table.DataTable(
            id='tmp-table',
            columns=uts.template_columns,
            data=uts.template_data,
            style_cell={'textAlign': 'center'},
            style_table=uts.up_style_3
        ),

        html.Br(),

        html.Div([
            html.Div([
                html.P('Expected format:'),
                html.Div([
                    html.Label('Date: YYYY-MM-DD'),
                    html.Label('Value: float, e.g. 123.456'),
                ], style=uts.up_style_4)
            ], style=uts.up_style_2),

        ], style=uts.box_style),

        *[html.Br() for _ in range(9)],
        html.Label('Robert Orlowski, 171661', style={'text-align': 'right', 'color': 'lightgrey'}),
        html.Br()

    ], style=uts.box_style)


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_upload(content, file_name):

    global data_set

    if content is not None:
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in file_name:
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), index_col=0)

                data_set = dict()
                ticker_list = df.columns.to_list()
                data_set['tickers'] = [{'label': ticker, 'value': ticker} for ticker in ticker_list]
                data_set['dates'] = sorted(df.index.to_list())
                data_set['df'] = df

                # add here data validation - check if csv is properly formed
                return html.Div(['You have uploaded the file successfully.'], style={'color': '#81ff78'})
            else:
                return html.Div(['Incorrect file type. Try again.'], style={'color': '#fa7634'})
        except TypeError:
            data_set = None
            return html.Div(['An error occurred while processing this file.'], style={'color': '#fa7634'})
    else:
        if data_set is not None:
            return html.Label('You are already working on the uploaded file.', style={'color': '#81ff78'})
        else:
            return html.Label('You haven\'t uploaded the file yet.')


# portfolio page
def render_portfolio_page():
    return html.Div([
        html.Br(),
        html.Br(),
        html.Div([
            html.Div([
                uts.portfolio_tab_description
            ], style=uts.up_style_1)
        ], style={'margin': 'auto', 'width': '60%'}),
        html.Hr(),
        html.Div(['Choose preffered stocks'], style=uts.up_style_2),
        html.Br(),
        dcc.Dropdown(
            id='stocks-multi-dropdown-1',
            options=data_set['tickers'],
            multi=True,
            style={'margin': 'auto', 'width': '60%'},
        ),
        html.Br(),
        html.Br(),
        html.Div(['Select estimation window range'], style=uts.up_style_2),
        html.Br(),
        html.Div([
            dcc.DatePickerRange(
                id='estimation-picker',
                display_format='YYYY-MM-DD',
                min_date_allowed=datetime.datetime.strptime(data_set['dates'][0], '%Y-%m-%d').date(),
                max_date_allowed=datetime.datetime.strptime(data_set['dates'][-1], '%Y-%m-%d').date(),
                initial_visible_month=datetime.datetime.strptime(data_set['dates'][0], '%Y-%m-%d').date(),
                minimum_nights=3,
                number_of_months_shown=3,
                with_portal=False
            ),
        ], style={'text-align': 'center'}),
        html.Br(),
        html.Br(),
        html.Div(['Select evaluation window range'], style=uts.up_style_2),
        html.Br(),
        html.Div([
            dcc.DatePickerRange(
                id='evaluation-picker',
                display_format='YYYY-MM-DD',
                min_date_allowed=datetime.datetime.strptime(data_set['dates'][0], '%Y-%m-%d').date(),
                max_date_allowed=datetime.datetime.strptime(data_set['dates'][-1], '%Y-%m-%d').date(),
                initial_visible_month=datetime.datetime.strptime(data_set['dates'][0], '%Y-%m-%d').date(),
                minimum_nights=3,
                number_of_months_shown=3,
                with_portal=False
            ),
        ], style={'text-align': 'center'}),
        html.Br(),
        html.Br(),
        html.Div(['Enter risk-free rate'], style=uts.up_style_2),
        html.Div([
            dcc.Input(id='risk-free-rate', type='number', debounce=True)
        ], style={'text-align': 'center'}),

        html.Br(),
        html.Br(),
        html.Div(['When all input data has been provided, the graphs should appear below.'], style=uts.up_style_5),

        html.Div(id='graphs')

    ], style=uts.box_style)


@app.callback(Output('graphs', 'children'),
              Input('estimation-picker', 'start_date'),
              Input('estimation-picker', 'end_date'),
              Input('evaluation-picker', 'start_date'),
              Input('evaluation-picker', 'end_date'),
              Input('stocks-multi-dropdown-1', 'value'),
              Input('risk-free-rate', 'value'))
def update_portfolio(est_start, est_end, eval_start, eval_end, stocks, risk_free):
    if None not in (est_start, est_end, eval_start, eval_end, stocks, risk_free) and stocks != []:

        est_data = mpt.select_data(data_set['df'], stocks, est_start, est_end)
        est_data = mpt.process_data(est_data)

        eval_data = mpt.select_data(data_set['df'], stocks, eval_start, eval_end)
        eval_data = mpt.process_data(eval_data)

        df_all_data = mpt.run_mpt_calculations(est_data, eval_data, risk_free)

        fig_return = px.line(df_all_data, x='days', y='ExpReturn', color='strategy', hover_name='strategy',
                             title='Return ~ Days')
        fig_risk = px.line(df_all_data, x='days', y='Risk', color='strategy', hover_name='strategy',
                           title='Risk ~ Days')
        fig_sharpe = px.line(df_all_data, x='days', y='Sharpe', color='strategy', hover_name='strategy',
                             title='Sharpe Ratio ~ Days')

        tmp_div = html.Div([
            html.Hr(),
            dcc.Graph(figure=fig_return),
            html.Br(),
            dcc.Graph(figure=fig_risk),
            html.Br(),
            dcc.Graph(figure=fig_sharpe),
            html.Br()
        ])

        return tmp_div
    else:
        return html.Div([html.Br()])


# data view page
def render_data_view_tab():
    return html.Div([
        html.Br(),
        html.Br(),

        html.Div([
            html.Div([
                uts.data_view_tab_description
            ], style=uts.up_style_1)
        ], style={'margin': 'auto', 'width': '60%'}),

        html.Hr(),
        html.Div(['Current Data (Preview)'], style=uts.up_style_2),
        html.Br(),
        get_data_view_table(data_set['df']),
        html.Br(),
        html.Div([
            html.Button('Validate Data', id='validate-button', n_clicks=0),
        ], style={'text-align': 'center'}),
        html.Div(id='validation-output')

    ], style=uts.box_style)


def get_data_view_table(df: pd.DataFrame):

    df_2 = df.copy()
    df_2 = df_2[df_2.columns[:8]]
    df_2 = df_2[:10]
    df_2['date'] = df_2.index
    columns = df_2.columns.to_list()
    columns = columns[-1:] + columns[:-1]
    df_2 = df_2[columns]

    return dash_table.DataTable(
        columns=[{'name': i, 'id': i} for i in df_2.columns],
        data=df_2.to_dict('records'),
        style_cell={'textAlign': 'center'},
        style_table=uts.up_style_3
    )


@app.callback(Output('validation-output', 'children'),
              Input('validate-button', 'n_clicks'))
def update_data_view_tab(n_clicks):
    if n_clicks != 0:

        issues = mpt.validate_input_data(data_set['df'])
        communicate_list = []

        if issues:
            for index, issue in enumerate(issues):
                tmp_div = html.Div([
                    html.Div(['Issue #' + str(index + 1) + ' ' + issue], style=uts.up_style_2),
                    html.Br()
                ])
                communicate_list.append(tmp_div)

            communicate_list.append(html.Div(['Try to repair the data set and reupload it.'], style=uts.up_style_2))

        else:
            communicate_list.append(html.Div(['Data set passed the validation.'], style=uts.up_style_2))

        return html.Div([
            html.Hr(),
            *communicate_list,
            html.Br()
        ])
    else:
        return html.Div([html.Br()])


# statistics page
def render_stat_tab():
    return html.Div([
        html.Br(),
        html.Br(),

        html.Div([
            html.Div([
                uts.statistics_tab_description
            ], style=uts.up_style_1)
        ], style={'margin': 'auto', 'width': '60%'}),

        html.Hr(),
        html.Div(['Summary statistics'], style=uts.up_style_2),
        html.Br(),
        html.Br(),
        dcc.Dropdown(
            id='stocks-dropdown-1',
            options=data_set['tickers'],
            multi=False,
            style={'margin': 'auto', 'width': '60%'},
            placeholder='Select a stock'
        ),
        html.Br(),
        html.Br(),
        html.Div([
            dcc.DatePickerRange(
                id='hist-picker',
                display_format='YYYY-MM-DD',
                min_date_allowed=datetime.datetime.strptime(data_set['dates'][0], '%Y-%m-%d').date(),
                max_date_allowed=datetime.datetime.strptime(data_set['dates'][-1], '%Y-%m-%d').date(),
                initial_visible_month=datetime.datetime.strptime(data_set['dates'][0], '%Y-%m-%d').date(),
                minimum_nights=3,
                number_of_months_shown=3,
                with_portal=False,
            ),
        ], style={'text-align': 'center'}),
        html.Br(),
        html.Div(id='hist-plot', style={'margin': 'auto', 'width': '70%'}),
        html.Br(),
        html.Div(id='stat-table'),
        html.Hr(),
        html.Div(['Correlation (Risk)'], style=uts.up_style_2),
        html.Br(),
        dcc.Dropdown(
            id='stocks-multi-dropdown-2',
            options=data_set['tickers'],
            multi=True,
            style={'margin': 'auto', 'width': '60%'},
            placeholder='Select multiple stocks'
        ),
        html.Br(),
        html.Div([
            dcc.DatePickerRange(
                id='corr-picker',
                display_format='YYYY-MM-DD',
                min_date_allowed=datetime.datetime.strptime(data_set['dates'][0], '%Y-%m-%d').date(),
                max_date_allowed=datetime.datetime.strptime(data_set['dates'][-1], '%Y-%m-%d').date(),
                initial_visible_month=datetime.datetime.strptime(data_set['dates'][0], '%Y-%m-%d').date(),
                minimum_nights=3,
                number_of_months_shown=3,
                with_portal=False
            ),
        ], style={'text-align': 'center'}),
        html.Br(),
        html.Div(id='corr-plot', style={'margin': 'auto', 'width': '70%'}),
        html.Br(),
    ])


@app.callback(Output('hist-plot', 'children'),
              Output('stat-table', 'children'),
              Input('stocks-dropdown-1', 'value'),
              Input('hist-picker', 'start_date'),
              Input('hist-picker', 'end_date'))
def update_histogram(value, start_date, end_date):
    if None not in (value, start_date, end_date):
        raw_data = mpt.select_data(data_set['df'], value, start_date, end_date)
        hist_data = mpt.process_data(raw_data)
        stats_data = mpt.get_statistics(hist_data)
        fig = px.histogram(hist_data)
        return dcc.Graph(figure=fig), dash_table.DataTable(columns=[{'name': i, 'id': i} for i in stats_data.columns],
                                                           data=stats_data.to_dict('records'),
                                                           style_cell={'text-align': 'center'},
                                                           style_table={'margin': 'auto', 'width': '50%'})
    return dcc.Graph(figure=uts.empty_plot_layout), html.Div()


@app.callback(Output('corr-plot', 'children'),
              Input('stocks-multi-dropdown-2', 'value'),
              Input('corr-picker', 'start_date'),
              Input('corr-picker', 'end_date'))
def update_heatmap(stocks, start_date, end_date):
    if None not in (stocks, start_date, end_date) and stocks != []:
        raw_data = mpt.select_data(data_set['df'], stocks, start_date, end_date)
        heatmap_data = mpt.process_data(raw_data)
        fig = px.imshow(heatmap_data.corr(), title='Correlation')
        return dcc.Graph(figure=fig)

    return dcc.Graph(figure=uts.empty_plot_layout)


# main call
if __name__ == '__main__':
    app.run_server(debug=False)
