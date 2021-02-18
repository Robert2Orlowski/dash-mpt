# Styling
empty_plot_layout = {
    "layout": {
        "xaxis": {
            "visible": False
        },
        "yaxis": {
            "visible": False
        },
        "annotations": [
            {
                "text": "No data found",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {
                    "size": 28
                }
            }
        ]
    }
}

box_style = {
    'width': '90%',
    'margin': 'auto',
}

column_style = {
    'width': '50%',
    'float': 'left'
}

upload_bar_style = {
    'width': '50%',
    'height': '60px',
    'lineHeight': '60px',
    'borderWidth': '1px',
    'borderStyle': 'dashed',
    'borderRadius': '5px',
    'textAlign': 'center',
    'margin': 'auto',
}

up_style_1 = {
    'font-size': '20px',
    'text-align': 'center'
}

up_style_2 = {
    'font-size': '16px',
    'text-align': 'center'
}

up_style_3 = {
    'width': '40%',
    'margin': 'auto'
}

up_style_4 = {
    'font-size': '14px',
    'text-align': 'center'
}

up_style_5 = {
    'font-size': '12px',
    'text-align': 'center'
}

template_columns = [
    {'name': 'date', 'id': 'date'},
    {'name': 'stock A', 'id': 'stock A'},
    {'name': 'stock B', 'id': 'stock B'},
    {'name': 'stock C', 'id': 'stock C'},
]

template_data = [
    {'date': 'date 1', 'stock A': 'value 1', 'stock B': 'value 4', 'stock C': 'value 7'},
    {'date': 'date 2', 'stock A': 'value 2', 'stock B': 'value 5', 'stock C': 'value 8'},
    {'date': 'date 3', 'stock A': 'value 3', 'stock B': 'value 6', 'stock C': 'value 9'},
]

upload_tab_description = 'Here you can upload a csv file with a stock data (or replace the existing one).'
data_view_tab_description = 'This tab allows you to view uploaded data and validate (test) it against requirements ' \
                            'of features performing calculations'
portfolio_tab_description = 'The purpose of \"Create Portfolio\" tab is to provide a calulation tool allowing ' \
                            'composition of investments based on method using estimation and evaluation windows.'
statistics_tab_description = 'Statistics tab gives you an insight into data characteristics'


empty_plot_layout = {
    "layout": {
        "xaxis": {
            "visible": False
        },
        "yaxis": {
            "visible": False
        },
        "annotations": [
            {
                "text": "No data found",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {
                    "size": 28
                }
            }
        ]
    }
}