from reportlab.platypus import PageBreak
from reportlab.platypus import Spacer
from reportlab.platypus import KeepTogether
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from dash import Dash, html, Input, Output, dcc
from callbacks import register_callbacks
from Layout import f_layout
from dash_bootstrap_components.themes import BOOTSTRAP
import pdfkit
import Graph, Layout
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Image


wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe' 
style = getSampleStyleSheet()


def main() -> None:
    app = Dash(__name__, external_stylesheets=[BOOTSTRAP])
    app.title = "Asset Overview"
    app.layout = html.Div([
        html.H1( style={'textAlign': 'center'}),
        f_layout(app),
        html.Button('Export PDF', id='btn-export-pdf', n_clicks=0),
        dcc.Download(id='download-pdf'),
        html.Div(id='export-pdf-status')
    ])
    
        
    
    @app.callback(
        Output('download-pdf', 'data'),
        Input('btn-export-pdf', 'n_clicks'),
        Input('dropdown-manager', 'value')
    )
    def download_pdf(n_clicks, manager): 

        option_list = []

            
        elements = []
        if n_clicks:
            pdf_buffer = BytesIO()              
            doc = SimpleDocTemplate(pdf_buffer, pagesize=(1190,1684))
            # option_list = [15004, 12982,15322]

            df_ppt = Layout.df[Layout.df['4PT Asset Manager']==manager]
            for val in df_ppt['AM_Underwriting_Sheet']:
                option_list.append(val)


            for value in option_list:
                filt_df = Graph.df[Graph.df['AM_Underwriting_Sheet'] == value]
                filt_df_op = Graph.df1[Graph.df1['AM_Underwriting_Sheet'] == value]
                filt_df_fin = Graph.df2[Graph.df2['AM_Underwriting_Sheet'] == value]
                filt_df_mar = Graph.df3[Graph.df3['AM_Underwriting_Sheet'] == value]
                filt_df_cap = Graph.df4[Graph.df4['AM_Underwriting_Sheet'] == value]
                filt_df_um = Graph.df5[Graph.df5['AM_Underwriting_Sheet'] == value]

                
                invest_df = Graph.invest_char(filt_df)
                returns_df = Graph.returns(filt_df)
                valuation_df = Graph.valuations(filt_df)
                operating_df = Graph.op(filt_df_op)
                financial_df = Graph.fin(filt_df_fin)
                market_df = Graph.mar(filt_df_mar)
                capital_df = Graph.cap(filt_df_cap)
                unitmix_df = Graph.um(filt_df_um)


                url = "https://s7d9.scene7.com/is/image/greystarprod/Pool%20at%20Elan%20Halcyon%20Apartments?qlt=72&wid=767&fit=constrain"
                image = Image(url, width=500, height=300)


                # Convert the table DataFrame to a list of lists for the Table
                Invest_dt = [['Fields', 'Values']]
                for index, row in invest_df.iterrows():
                    Invest_dt.append([row['Fields'], row['Values']])

                return_dt = [['Fields', 'Proforma', 'Spot']]
                for index, row in returns_df.iterrows():
                    return_dt.append([row['Fields'], row['Proforma'], row['Spot']])

                val_dt = [['Field', 'Value', 'Fields','Values']]
                for index, row in valuation_df.iterrows():
                    val_dt.append([row['Field'], row['Value'], row['Fields'], row['Values']])

                op_dt = [['Fields', 'Prior YTD Actual', 'YTD Actual','YTD Budget','TTM','Proforma']]
                for index, row in operating_df.iterrows():
                    op_dt.append([row['Fields'], row['Prior YTD Actual'], row['YTD Actual'],row['YTD Budget'],row['TTM'],row['Proforma']])

                fin_dt = [['Field', 'Value', 'Fields','Values']]
                for index, row in financial_df.iterrows():
                    fin_dt.append([row['Field'], row['Value'], row['Fields'], row['Values']])

                mar_dt = [['Fields', '2023', '2024','2025']]
                for index, row in market_df.iterrows():
                    mar_dt.append([row['Fields'], row['2023'], row['2024'],row['2025']])

                cap_dt = [['Fields', 'Total', 'UW','Budget']]
                for index, row in capital_df.iterrows():
                    cap_dt.append([row['Fields'], row['Total'], row['UW'], row['Budget']])

                um_dt = [['FloorPlan', 'Total Units', 'Classic Units','Renovated Units','Classic Rent', 'Renovated Rent', 'Cost', 'ROC']]
                for index, row in unitmix_df.iterrows():
                    um_dt.append([row['FloorPlan'], row['Total Units'], row['Classic Units'], row['Renovated Units'],row['Classic Rent'],row['Renovated Rent'],row['Cost'], row['ROC']])                

            
                Dash_styles = {'Heading': ParagraphStyle(name='Heading', fontSize=40, alignment=TA_CENTER)}    
                dash_title_style = Dash_styles['Heading'] 
                ppt_styles = {'Heading': ParagraphStyle(name='Heading', fontSize=15)}            
                ppt_style = ppt_styles['Heading']
                styles = {'Heading': ParagraphStyle(name='Heading', fontSize=20, alignment=TA_CENTER)}            
                title_style = styles['Heading']
                title_style.alignment = 0 # left
                title_style.alignment = TA_CENTER
                title_style.padding = 50

                Dash_title = Paragraph("Asset Overview", dash_title_style)
                ppt_id = Paragraph(f"propertyID {value}", ppt_style)
                title_inv = Paragraph("Investment Characterstics", title_style)
                Return_title = Paragraph('Return', title_style)
                Val_title = Paragraph('Valuation', title_style)
                op_title = Paragraph('Operating Performance', title_style)            
                fin_title = Paragraph('Financial', title_style)
                mar_title = Paragraph('Market Overview', title_style)
                cap_title = Paragraph('Capital Project', title_style)
                um_title = Paragraph('Unit Mix', title_style)

                spacer_height = 0.5 * 28.35
                spacer = Spacer(width=0, height=spacer_height)
            
                tb_inv = Table(Invest_dt,colWidths='*',hAlign = 'RIGHT',vAlign = 'TOP') 
                tb_ret = Table(return_dt,colWidths='*')
                tb_val = Table(val_dt,colWidths='*')
                tb_op = Table(return_dt, colWidths='*')
                tb_fin = Table(fin_dt, colWidths='*')
                tb_mar = Table(mar_dt, colWidths='*')
                tb_cap = Table(cap_dt, colWidths='*')
                tb_um = Table(um_dt, colWidths='*')

                # tb_val.vAlign = 'TOP'
                # Apply table styles
                style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background color
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for all cells
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header bottom padding
                    # ('BACKGROUND', (1, 1), (-1, 1), colors.beige),  # Data row background color
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add border lines                    
                ])
 


                tb_inv.setStyle(style)
                tb_ret.setStyle(style)              
                tb_val.setStyle(style)
                tb_op.setStyle(style)
                tb_fin.setStyle(style)
                tb_mar.setStyle(style)
                tb_cap.setStyle(style)
                tb_um.setStyle(style)
                                

                combined_table = [
                    [spacer, spacer],
                    [spacer, spacer],
                    [ppt_id,title_inv],
                    [spacer, spacer],
                    [image, tb_inv],
                    [Return_title,Val_title],
                    [spacer,spacer],
                    [tb_ret, tb_val],
                    [op_title,fin_title],
                    [spacer,spacer],
                    [tb_op,tb_fin],
                    [mar_title,cap_title],
                    [spacer,spacer],
                    [tb_mar, tb_cap],
                    ]
                

                elements.append(Dash_title)
                

                combined_tbl_lyout = Table(combined_table,colWidths='*')
                # combined_tbl_lyout_1 = Table([[tb_ret, tb_val]], colWidths='*',vAlign='Bottom')
                elements.append(combined_tbl_lyout)
                elements.append(um_title)
                elements.append(spacer)
                elements.append(tb_um)
                elements.append(PageBreak())
                
            
        doc.build(elements)
        
        pdf_data = pdf_buffer.getvalue()
        pdf_buffer.close()


        return dcc.send_bytes(pdf_data, filename='investment_characteristics_2.pdf')


    register_callbacks(app)
    port = app.run_server(debug=False)

if __name__ == '__main__':
    main()
