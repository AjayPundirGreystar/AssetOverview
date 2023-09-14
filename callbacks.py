from dash.dependencies import Input, Output, State
import pandas as pd
import Graph, Layout
import pdfkit
from dash.exceptions import PreventUpdate
from dash import dcc, html

wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe' 


def register_callbacks(app):
    @app.callback(
    Output('img', 'src'),
    Output('invest_fig', 'children'),
    Output('returns_fig', 'children'),
    Output('valuation_fig', 'children'),
    Output('operating_fig', 'children'),
    Output('financial_fig', 'children'),
    Output('market_fig', 'children'),
    Output('capital_fig', 'children'),
    Output('unitmix_fig', 'children'),
    Output('dropdown-id', 'options'),
    Output('dropdown-manager', 'options'),
    # Output('download-pdf', 'data'),
    # Input('btn-export-pdf', 'n_clicks'),
    Input('dropdown-manager', 'value'),
    Input('dropdown-id', 'value'))
    
    
    
    

    def filter_df(manager, selected_value):
        filt_df = Graph.df[Graph.df['AM_Underwriting_Sheet'] == selected_value]
        filt_df_op = Graph.df1[Graph.df1['AM_Underwriting_Sheet'] == selected_value]
        filt_df_fin = Graph.df2[Graph.df2['AM_Underwriting_Sheet'] == selected_value]
        filt_df_mar = Graph.df3[Graph.df3['AM_Underwriting_Sheet'] == selected_value]
        filt_df_cap = Graph.df4[Graph.df4['AM_Underwriting_Sheet'] == selected_value]
        filt_df_um = Graph.df5[Graph.df5['AM_Underwriting_Sheet'] == selected_value]

        img_df = Graph.img(filt_df)


        invest_df = Graph.invest_char(filt_df)
        invest_fig = Layout.get_styled_data_table(invest_df, Layout.common_style_cell_conditional,
                                        Layout.common_style_data,
                                        Layout.common_style_data_conditional,
                                        Layout.common_style_header,
                                        Layout.common_style_table,
                                        Layout.common_style_cell)
        
        returns_df = Graph.returns(filt_df)
        returns_fig = Layout.get_styled_data_table(returns_df, Layout.common_style_cell_conditional,
                                Layout.common_style_data,
                                Layout.common_style_data_conditional,
                                Layout.common_style_header,
                                Layout.common_style_table,
                                Layout.common_style_cell)
        
        valuation_df = Graph.valuations(filt_df)
        valuation_fig = Layout.get_styled_data_table(valuation_df, Layout.common_style_cell_conditional,
                                Layout.common_style_data,
                                Layout.common_style_data_conditional,
                                Layout.common_style_header,
                                Layout.common_style_table,
                                Layout.common_style_cell)
        
        operating_df = Graph.op(filt_df_op)
        operating_fig = Layout.get_styled_data_table(operating_df, Layout.common_style_cell_conditional,
                                Layout.common_style_data,
                                Layout.common_style_data_conditional,
                                Layout.common_style_header,
                                Layout.common_style_table,
                                Layout.common_style_cell)
        
        financial_df = Graph.fin(filt_df_fin)
        financial_fig = Layout.get_styled_data_table(financial_df, Layout.common_style_cell_conditional,
                                Layout.common_style_data,
                                Layout.common_style_data_conditional,
                                Layout.common_style_header,
                                Layout.common_style_table,
                                Layout.common_style_cell)
        
        market_df = Graph.mar(filt_df_mar)
        market_fig = Layout.get_styled_data_table(market_df, Layout.common_style_cell_conditional,
                                Layout.common_style_data,
                                Layout.common_style_data_conditional,
                                Layout.common_style_header,
                                Layout.common_style_table,
                                Layout.common_style_cell)
        
        capital_df = Graph.cap(filt_df_cap)
        capital_fig = Layout.get_styled_data_table(capital_df, Layout.common_style_cell_conditional,
                                Layout.common_style_data,
                                Layout.common_style_data_conditional,
                                Layout.common_style_header,
                                Layout.common_style_table,
                                Layout.common_style_cell)
        
        unitmix_df = Graph.um(filt_df_um)
        unitmix_fig = Layout.get_styled_data_table(unitmix_df, Layout.common_style_cell_conditional,
                                Layout.common_style_data,
                                Layout.common_style_data_conditional,
                                Layout.common_style_header,
                                Layout.common_style_table,
                                Layout.common_style_cell)
        op = [15004, 12184,12982]
        options = [{'label': str(value), 'value': value} for value in op]

        option = []
        df_ppt = Layout.df[Layout.df['4PT Asset Manager']==manager]
        for val in df_ppt['AM_Underwriting_Sheet']:
            option.append({'label': str(val), 'value': val})

        option_manager = []
        df_op = Layout.df['4PT Asset Manager']
        for val in df_op:
            option_manager.append({'label': str(val), 'value': val})

        return  img_df, invest_fig, returns_fig, valuation_fig, operating_fig,  financial_fig , market_fig, capital_fig, unitmix_fig, option, option_manager
    
        
