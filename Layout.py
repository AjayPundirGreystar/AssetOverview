from dash import Dash, html, DiskcacheManager, dash_table, dcc
from dash.dash_table import DataTable
import  Graph
import pandas as pd


path = r'B:\Business_Applications\Phani\Python\POC_Updated\AM_Dashboard_UW_Model.xlsx'
df = pd.read_excel(path, sheet_name='Operating Performance')

option = []
for val in df['AM_Underwriting_Sheet']:
    option.append({'label': str(val), 'value': val})


def get_styled_data_table(df, style_cell_conditional=None, style_data=None, style_data_conditional=None, 
                          style_header=None,style_table=None,style_cell=None):
    return dash_table.DataTable(
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
        style_cell_conditional=style_cell_conditional,
        style_data=style_data,
        style_data_conditional=style_data_conditional,
        style_header=style_header,
        style_table=style_table,
        style_cell=style_cell
    )



# Define the common styles
common_style_cell_conditional = [
    {
        'if': {'column_id': col},
        'textAlign': 'left' if col in ['Column1', 'Column2'] else 'center'
    } for col in df.columns
]

common_style_data = {
    'color': 'black',
    'backgroundColor': 'white'
}

common_style_data_conditional = [
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(220, 220, 220)',
    }
]

common_style_header = {
    'backgroundColor': 'rgb(210, 210, 210)',
    'color': 'black',
    'fontWeight': 'bold'
}

common_style_table = {
    'border': '1px solid black',
    'border-collapse':'collapse'
    # 'padding': '0.5px'
}

common_style_cell = {
    'border': '1px solid black'
    
}

def f_layout(app) -> html.Div:
    # img = Graph.img()

    # export_button = html.Button("Export to PDF", id="btn-export-pdf", n_clicks=0)

    dropdown_manager = dcc.Dropdown(id='dropdown-manager',
                        options=option,
                        value=option[0]['value'],
                        # multi=True,
                        style={'width': '200px', 'margin-right': '10px'}
                        )
    manager_label = html.Label("Manager", style={'padding-right': '10px','font-size': '24px', 'font-weight': 'bold'})

    dropdown = dcc.Dropdown(id='dropdown-id',
                            options=option,
                            value=option[0]['value'],
                            # multi=True,
                            style={'width': '200px', 'margin-right': '10px'}
                            )
    
    dropdown_label = html.Label("PropertyID", style={'padding-right': '10px','font-size': '24px', 'font-weight': 'bold'})

    return html.Div(className="app_div", children=[
        html.H1(app.title, style={'textAlign': 'center'}),
        html.Div(style={'display': 'flex'}, children=[
            manager_label,
            dropdown_manager,
            dropdown_label,
            dropdown
            # export_button
        ]),
        html.Div(id='output-id'),
        html.Div(style={'height': '20px'}),
        html.Div(
            style={'display': 'flex', 'flex-wrap': 'wrap'},  # Enable flex-wrap for the parent div
            children=[
                html.Div(
                    children=[
                        html.Img(id='img' , style={'width': '100%','height':'88%','padding': '0.5cm','margin-top': '26px'})
                    ],
                    style={'width': '50%','width':'800px','height':'590px'}
                ),
                html.Div(
                    children=[
                        html.H2(style={'text-align': 'center'}, children="Investment Characteristics"),
                        html.Div(id='invest_fig', className="Dropdown",
                                 style={'padding-left': '0.5cm', 'padding-right': '0.5cm'},
                                 children=[
                                    #  get_styled_data_table(df, common_style_cell_conditional,
                                    #                       common_style_data,
                                    #                       common_style_data_conditional,
                                    #                       common_style_header,
                                    #                       common_style_table,
                                    #                       common_style_cell)
                                 ]),
                    ],
                    style={'flex': '1'}
                ),
                html.Div(
                    children=[
                        html.H2(style={'text-align': 'center'}, children="Returns"),
                        html.Div(id= 'returns_fig', className="Dropdown",
                                 style={'padding-left': '0.5cm', 'padding-right': '0.5cm'},
                                 children=[
                                    #  get_styled_data_table(df_r, common_style_cell_conditional,
                                    #                       common_style_data,
                                    #                       common_style_data_conditional,
                                    #                       common_style_header,
                                    #                       common_style_table,
                                    #                       common_style_cell)
                                 ]),
                    ],
                    style={'flex': '1'}
                ),
                html.Div(
                    children=[
                        html.H2(style={'text-align': 'center'}, children="Valuations"),
                        html.Div(id = 'valuation_fig', className="Dropdown",
                                 style={'padding-left': '0.5cm', 'padding-right': '0.5cm'},
                                 children=[
                                    #  get_styled_data_table(df_v, common_style_cell_conditional,
                                    #                       common_style_data,
                                    #                       common_style_data_conditional,
                                    #                       common_style_header,
                                    #                       common_style_table,
                                    #                       common_style_cell)
                                 ])
                    ],
                    style={'flex': '1'}
                ),
            ]
        ),
        html.Div(style={'height': '0.5cm'}),
        html.Div(
            style={'display': 'flex'},
            # Use display:flex to align Returns and Valuations charts side by side
            children=[
                html.Div(
                    className="op-chart",
                    style={'flex': '1', 'padding-right': '0.5cm', 'padding-left': '0.25cm'},
                    children=[
                        html.H2(style={'text-align': 'center'}, children="Operating Performance"),
                        html.Div(id = 'operating_fig', className="Dropdown",
                                 style={'padding-left': '0.5cm', 'padding-right': '0.5cm'},
                                 children=[
                                     # Add DataTable to display df_op
                                    #  get_styled_data_table(df_op, common_style_cell_conditional,
                                    #                       common_style_data,
                                    #                       common_style_data_conditional, 
                                    #                       common_style_header,
                                    #                       common_style_table,
                                    #                       common_style_cell)
                                 ])
                    ]
                ),
                html.Div(
                    className="fin-chart",
                    style={'flex': '1', 'padding-right': '0.5cm', 'padding-left': '0.25cm'},
                    children=[
                        html.H2(style={'text-align': 'center'}, children="Financial"),
                        html.Div(id='financial_fig', className="Dropdown",
                                 style={'padding-left': '0.5cm', 'padding-right': '0.5cm'},
                                 children=[
                                     # Add DataTable to display df_v
                                    #  get_styled_data_table(df_fin, common_style_cell_conditional,
                                    #                       common_style_data,
                                    #                       common_style_data_conditional, 
                                    #                       common_style_header,
                                    #                       common_style_table,
                                    #                       common_style_cell)
                                 ])
                    ]
                ),
            ]
        ),
        html.Div(style={'height': '0.5cm'}),
        # New div for "Market Overview" tables in a new line
        html.Div(
            style={'display': 'flex'},
            children=[
                html.Div(
                    className="mo-chart",
                    style={'flex': '1', 'padding-right': '0.5cm', 'padding-left': '0.25cm'},
                    children=[
                        html.H2(style={'text-align': 'center'}, children="Market Overview"),
                        html.Div(id='market_fig', className="Dropdown",
                                 style={'padding-left': '0.5cm', 'padding-right': '0.5cm'},
                                 children=[
                                    #  # Add DataTable to display df_mar
                                    #  get_styled_data_table(df_mar, common_style_cell_conditional,
                                    #                       common_style_data,
                                    #                       common_style_data_conditional, 
                                    #                       common_style_header,
                                    #                       common_style_table,
                                    #                       common_style_cell)
                                 ])
                    ]
                ),
                html.Div(
                    className="cap-chart",
                    style={'flex': '1', 'padding-right': '0.5cm', 'padding-left': '0.25cm'},
                    children=[
                        html.H2(style={'text-align': 'center'}, children="Capital Projects"),
                        html.Div(id = 'capital_fig', className="Dropdown",
                                 style={'padding-left': '0.5cm', 'padding-right': '0.5cm'},
                                 children=[
                                     # Add DataTable to display df_cap
                                    #  get_styled_data_table(df_cap, common_style_cell_conditional,
                                    #                       common_style_data,
                                    #                       common_style_data_conditional, 
                                    #                       common_style_header,
                                    #                       common_style_table,
                                    #                       common_style_cell)
                                 ])
                    ]
                ),
                html.Div(
                    className="um-chart",
                    style={'flex': '1', 'padding-right': '0.5cm', 'padding-left': '0.25cm'},
                    children=[
                        html.H2(style={'text-align': 'center'}, children="Unit Mix"),
                        html.Div(id='unitmix_fig', className="Dropdown",
                                 style={'padding-left': '0.5cm', 'padding-right': '0.5cm'},
                                 children=[
                                     # Add DataTable to display df_um
                                    #  get_styled_data_table(df_um, common_style_cell_conditional,
                                    #                       common_style_data,
                                    #                       common_style_data_conditional, 
                                    #                       common_style_header,
                                    #                       common_style_table,
                                    #                       common_style_cell)
                                 ])
                    ]
                )
            ]
        )
    ])
