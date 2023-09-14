import pandas as pd
from PIL import Image
import requests
from IPython.display import display
from io import BytesIO


table_df = pd.DataFrame()


path = r'B:\Business_Applications\Phani\Python\POC_Updated\AM_Dashboard_UW_Model.xlsx'
sheet_name = 'AM_Underwriting_Sheet'
df = pd.read_excel(path, sheet_name=sheet_name)


sheet_name = 'Operating Performance'
df1 = pd.read_excel(path, sheet_name=sheet_name)


sheet_name = 'Financial'
dtype_mapping = {
    'ExtensionOptions': str,  # Specify 'ExtensionOptions' column as string data type
    # Add other columns with appropriate data types if needed
}
df2 = pd.read_excel(path, sheet_name=sheet_name, dtype=dtype_mapping)


sheet_name = 'Market Overview'
df3 = pd.read_excel(path, sheet_name='Market Overview')


sheet_name = 'Capital Projects'
df4 = pd.read_excel(path, sheet_name='Capital Projects')


sheet_name = 'Unit Mix'
df5 = pd.read_excel(path, sheet_name='Unit Mix')


#Import the image
param_string = "?sv=2020-04-08&st=2021-08-10T15%3A16%3A35Z&se=2023-08-11T15%3A16%3A00Z&sr=c&sp=rl&sig=AiE%2BhDi2YekgYhwnK9AyYpNGhoeM0J4lM7FCG4as0uM%3D"

def img(img_df):
    # img_df = df[df['AM_Underwriting_Sheet'] == 15322]
    filtered_image_urls = img_df['Asset Hero Image URL'].tolist()
    url = "https://s7d9.scene7.com/is/image/greystarprod/Pool%20at%20Elan%20Halcyon%20Apartments?qlt=72&wid=767&fit=constrain"

#    url = url.replace(' ', '%20') 
    # filtered_image_urls_with_params  = [url + param_string for url in filtered_image_urls]
    # for url in filtered_image_urls_with_params:
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         image = Image.open(BytesIO(response.content))
    #         # dis_img = display(image)
    #     else:
    #         print(f"Failed to download the image from URL: {url}")
    # if image is not None:
    #     return image
    # else:
    #     # Return a placeholder or handle this case as needed
    #     return None
    return url
# print(imgs)
# abc=img(df)
# print(abc)


def invest_char(df)->pd.DataFrame:
    # df = filter_data(p_id)
    Investment_Characteristics = {
    'Address': '',
    'Axio Market | Axio Submarket': '',
    'Construction Type | Stories': '',
    '# of Units | Vintage': '',
    'Total Residential SF': '',
    'Total Commercial SF': '',
    'Portfolio Manager | Fund': '',
    'Asset Manager': '',
    'Operations Director': '',
    'Regional Property Manager | Property Manager': '',
    'Regional CPG Director | Construction Manager': '',
    'Acquisition Date': '',
    'Underwritten Hold Period': '',
    'Acquisition Price | Unit | PSF': '',
    'Greystar Ownership | Partner': ''
}
        
    table_df = pd.DataFrame(Investment_Characteristics.items(), columns=['Fields', 'Values'])

    column_mapping = {
    'Axio Market | Axio Submarket': ['Axio Market','Axio Submarket'],
    'Portfolio Manager | Fund': ['Portfolio Manager','Fund'],
    'Asset Manager': ['4PT Asset Manager'],
    'Operations Director': ['Operations Director'],
    'Regional CPG Director | Construction Manager': ['Regional CPG Director','Construction Manager'],
    'Acquisition Date': ['Acquisition Date'],
    'Underwritten Hold Period': ['Underwritten Hold Period'],
    'Acquisition Price | Unit | PSF': ['Acquisition Price'],
    'Greystar Ownership | Partner': ['Greystar Ownership', 'Partner']
}
    # Iterate over each row in the table DataFrame
    for index, row in table_df.iterrows():
        field = row['Fields']
        if field in column_mapping:
            column_names = column_mapping[field]
            matching_columns = [col for col in column_names if col in df.columns]
            if matching_columns:
                # Extract the values from all matching columns in the data DataFrame
                values = [df[col].iloc[0] for col in matching_columns]

                # Format the values based on the field
                if field == 'Greystar Ownership | Partner':
                    formatted_values = []
                    for val in values:
                        if isinstance(val, (int, float)):
                            formatted_values.append(f'{val * 100:.0f}%')
                        else:
                            formatted_values.append(val)
                    values = formatted_values
                elif field == 'Acquisition Date':
                    values = [val.strftime('%m/%d/%Y') for val in values]
                elif field == 'Underwritten Hold Period':
                    values = [f'{val:.0f} Years' for val in values]
                elif field == 'Acquisition Price | Unit | PSF':
                    values = [f'${val / 1000000:.0f} M' for val in values]

                values = [str(val) if str(val) != 'nan' else '' for val in values]

                table_df.at[index, 'Values'] = ' | '.join(values)

    return table_df


def returns(df)->pd.DataFrame:

    static_values = {
    'Sales Data': '',
    'Levered IIR': '',
    'Unlevered IIR': '',
    'Levered Multiple': '',
    'CoC': '',
    'NOI Yield': '',
    'Residual Value': ''
}
    table_df = pd.DataFrame(static_values.items(), columns=['Fields', 'Proforma'])

    column_mapping = {
    'Sales Data': {'Proforma': 'Sale Date Proforma', 'Spot': 'Sale Date Spot'},
    'Levered IIR': {'Proforma': 'Levered IRR Proforma', 'Spot': 'Levered IRR Spot'},
    'Unlevered IIR': {'Proforma': 'Unlevered IRR Proforma', 'Spot': 'Unlevered IRR Spot'},
    'Levered Multiple': {'Proforma': 'Levered Multiple Proforma', 'Spot': 'Levered Multiple Spot'},
    'CoC': {'Proforma': 'CoC Proforma', 'Spot': 'CoC Spot'},
    'NOI Yield': {'Proforma': 'NOI Yield Proforma', 'Spot': 'NOI Yield Spot'},
    'Residual Value': {'Proforma': 'Residual Value Proforma', 'Spot': 'Residual Value Spot'}
}
    
    # Iterate over each row in the table DataFrame
    for index, row in table_df.iterrows():
        field = row['Fields']
        if field in column_mapping:
            proforma_column = column_mapping[field]['Proforma']
            spot_column = column_mapping[field]['Spot']

            if proforma_column in df.columns and spot_column in df.columns:
                # Extract the values from the corresponding columns in the data DataFrame
                proforma_value = df[proforma_column].iloc[0]
                spot_value = df[spot_column].iloc[0]

                # Replace 'NaN' values with blank strings
                if pd.isna(proforma_value):
                    proforma_value = ''
                if pd.isna(spot_value):
                    spot_value = ''

                # Check if the field requires percentage formatting
                if field in ['Levered IIR', 'Unlevered IIR', 'CoC', 'NOI Yield']:
                    if isinstance(proforma_value, (int, float)):
                        proforma_value = f'{proforma_value * 100:.1f}%'  # Format the proforma value as percentage with one decimal place
                    if isinstance(spot_value, (int, float)):
                        spot_value = f'{spot_value * 100:.1f}%'
                    else:
                        spot_value = ''  # Set spot_value to an empty string if it's not a valid numeric value
                elif field == 'Residual Value':
                    if isinstance(proforma_value, (int, float)):
                        proforma_value = f'${proforma_value / 1000000:.0f} million'  # Format the proforma value as dollars in millions
                    if isinstance(spot_value, (int, float)):
                        spot_value = f'${spot_value / 1000000:.0f} million'
                    else:
                        spot_value = ''  # Set spot_value to an empty string if it's not a valid numeric value
                elif field == 'Sales Data':
                    if pd.notna(proforma_value):
                        proforma_value = proforma_value.strftime('%m/%d/%Y')  # Format the proforma value as month/day/year
                    if pd.notna(spot_value):
                        spot_value = spot_value.strftime('%m/%d/%Y')

                table_df.at[index, 'Proforma'] = proforma_value
                table_df.at[index, 'Spot'] = spot_value

    return table_df


def valuations(df)->pd.DataFrame:
    static_values_table2 = {
    'GAV | per Unit': '',
    'Asset NAV | per Unit': '',
    'Asset NAV % of Fund': '',
    '': ''
}
    table_df2 = pd.DataFrame(static_values_table2.items(), columns=['Field', 'Value'])

    # Create a dictionary to map the column names for the second table
    column_mapping_table2 = {
        'GAV | per Unit': 'GAV',
        'Asset NAV | per Unit': 'Fund NAV',
        'Asset NAV % of Fund': 'Fund NAV % of Fund',
        '': ''
    }

    # Iterate over each row in the second table DataFrame
    for index, row in table_df2.iterrows():
        field = row['Field']
        if field in column_mapping_table2:
            column_name = column_mapping_table2[field]
            if column_name in df.columns:
                # Extract the value from the corresponding column in the data DataFrame
                value = df[column_name].iloc[0]
                
                # Check if the field requires formatting
                if field == 'GAV | per Unit' or field == 'Asset NAV | per Unit':
                    value = f'${value / 1000000:.0f} M'  # Format the value as dollars in millions
                
                table_df2.at[index, 'Value'] = value

    # Add blank columns to Table 2
    table_df2['  '] = ''
    table_df2['Fields'] = ''
    table_df2['Values'] = ''

    # Assign static values to the additional columns
    table_df2.at[0, 'Fields'] = 'Appraiser'
    table_df2.at[1, 'Fields'] = 'Going-in-yield'
    table_df2.at[2, 'Fields'] = 'Exit Cap Rate%'
    table_df2.at[3, 'Fields'] = 'Yr 1 Appraiser NOI'

    # Map values from Excel to Column C in Table 2
    table_df2.at[0, 'Values'] = df['Appraiser'].iloc[0]
    table_df2.at[1, 'Values'] = f'{df["Going-in-yield"].iloc[0] * 100:.2f}%'  # Format as percentage with two decimal places
    table_df2.at[2, 'Values'] = f'{df["Residual Cap Rate"].iloc[0] * 100:.2f}%'  # Format as percentage with two decimal places
    table_df2.at[3, 'Values'] = f'${df["Yr 1 Appraiser NOI"].iloc[0] / 1000000:.2f} M'  # Format as dollars in millions with two decimal places

    return table_df2


def op(df1) -> pd.DataFrame:
    OperatingPerformance = {
        'Occupancy': '',
        'Effective Rent': '',
        'Total Revenue': '',
        'Controllable Expenses': '',
        'Non-Controllable Expenses': '',
        'Net Operating Income': '',
        'Margin': '',
        'Rpm. Reserves/Units': '',
        'NOI After Replacements': ''
    }

    table_df = pd.DataFrame(OperatingPerformance.items(), columns=['Fields', 'Prior YTD Actual'])

    column_mapping = {
        'Occupancy':{
            'Prior YTD Actual':'Prior YTD Actual Occupancy',
            'YTD Actual':'YTD Actual Occupancy',
            'YTD Budget':'YTD Budget Occupancy',
            'TTM':'TTM Occupancy',
            'Proforma':'Proforma Occupancy'
        },
        'Effective Rent':{
            'Prior YTD Actual':'Prior YTD Actual Effective Rent',
            'YTD Actual':'YTD Actual Effective Rent',
            'YTD Budget':'YTD Budget Effective Rent',
            'TTM':'TTM Effective Rent','Proforma':
            'Proforma Effective Rent'
        },
        'Total Revenue':{
            'Prior YTD Actual':'Prior YTD Actual Total Revenue',
            'YTD Actual':'YTD Actual Total Revenue',
            'YTD Budget':'YTD Budget Total Revenue',
            'TTM':'TTM Total Revenue',
            'Proforma':'Proforma Total Revenue'
        },
        'Controllable Expenses':{
            'Prior YTD Actual':'Prior YTD Actual Controllable Expenses',
            'YTD Actual':'YTD Actual Controllable Expenses',
            'YTD Budget':'YTD Budget Controllable Expenses',
            'TTM':'TTM Controllable Expenses',
            'Proforma':'Proforma Controllable Expenses'
        },
        'Non-Controllable Expenses':{
            'Prior YTD Actual':'Prior YTD Actual Non-Controllable Expenses',
            'YTD Actual':'YTD Actual NoN-Controllable Expenses',
            'YTD Budget':'YTD Budget NoN - Controllable Expenses',
            'TTM':'TTM NoN Controllable Expenses',
            'Proforma':'Proforma NoN Controllable Expenses'
        },
        'Net Operating Income':{
            'Prior YTD Actual':'Prior YTD Actual NOI',
            'YTD Actual':'YTD Actual NOI',
            'YTD Budget':'YTD Budget NOI',
            'TTM':'TTM NOI',
            'Proforma':'Proforma NOI'
        },
        'Margin':{
            'Prior YTD Actual':'Prior YTD Actual Margin',
            'YTD Actual':'YTD Actual Margin',
            'YTD Budget':'YTD Budget Margin',
            'TTM':'TTM Margin',
            'Proforma':'Proforma Margin'
        },
        'Rpm. Reserves/Units':{
            'Prior YTD Actual':'Prior YTD Actual Rpm Reserves/Units',
            'YTD Actual':'YTD Actual Rpm Reserves/Units',
            'YTD Budget':'YTD Budget Rpm Reserves/Units',
            'TTM':'TTM Rpm Reserves/Units',
            'Proforma':'Proforma Rpm Reserves/Units'
        },
        'NOI After Replacements':{
            'Prior YTD Actual':'Prior YTD Actual NOI After Replacements',
            'YTD Actual':'YTD Actual NOI After Replacements',
            'YTD Budget':'YTD Budget NOI After Replacements',
            'TTM':'TTM NOI After Replacements',
            'Proforma':'Proforma NOI After Replacements'}
}


    for index, row in table_df.iterrows():
        field = row['Fields']
        if field in column_mapping:
            PriorYTDActual = column_mapping[field]['Prior YTD Actual']
            YTDActual = column_mapping[field]['YTD Actual']
            YTDBudget = column_mapping[field]['YTD Budget']
            TTM = column_mapping[field]['TTM']
            Proforma = column_mapping[field]['Proforma']

            if PriorYTDActual in df1.columns and YTDActual in df1.columns and YTDBudget in df1.columns and TTM in df1.columns and Proforma in df1.columns:
                # Extract the value from the corresponding column in the data DataFrame
                PriorYTDActual = df1[PriorYTDActual].iloc[0]
                YTDActual = df1[YTDActual].iloc[0]
                YTDBudget = df1[YTDBudget].iloc[0]
                TTM = df1[TTM].iloc[0]
                Proforma = df1[Proforma].iloc[0]

                # Ensure the values are numeric or can be converted to numeric
                def to_numeric_or_empty(value):
                    try:
                        return float(value)
                    except (ValueError, TypeError):
                        return None

                PriorYTDActual = to_numeric_or_empty(PriorYTDActual)
                YTDActual = to_numeric_or_empty(YTDActual)
                YTDBudget = to_numeric_or_empty(YTDBudget)
                TTM = to_numeric_or_empty(TTM)
                Proforma = to_numeric_or_empty(Proforma)

                # Perform formatting for 'Occupancy' and 'Margin' fields for specific columns
                if field == 'Occupancy':
                    if isinstance(PriorYTDActual, (int, float)):
                        PriorYTDActual = f'{PriorYTDActual * 100:.0f}%'
                    if isinstance(YTDActual, (int, float)):
                        YTDActual = f'{YTDActual * 100:.0f}%'
                    if isinstance(YTDBudget, (int, float)):
                        YTDBudget = f'{YTDBudget * 100:.0f}%'
                    if isinstance(TTM, (int, float)):
                        TTM = f'{TTM * 100:.0f}%'
                    if isinstance(Proforma, (int, float)):
                        Proforma = f'{Proforma * 100:.0f}%'

                elif field == 'Margin':
                    if isinstance(PriorYTDActual, (int, float)):
                        PriorYTDActual = f'{PriorYTDActual * 100:.0f}%'
                    if isinstance(YTDActual, (int, float)):
                        YTDActual = f'{YTDActual * 100:.0f}%'
                    if isinstance(YTDBudget, (int, float)):
                        YTDBudget = f'{YTDBudget * 100:.0f}%'
                    if isinstance(TTM, (int, float)):
                        TTM = f'{TTM * 100:.0f}%'
                    if isinstance(Proforma, (int, float)):
                        Proforma = f'{Proforma * 100:.0f}%'


            table_df.at[index, 'Prior YTD Actual'] = PriorYTDActual
            table_df.at[index, 'YTD Actual'] = YTDActual
            table_df.at[index, 'YTD Budget'] = YTDBudget
            table_df.at[index, 'TTM'] = TTM
            table_df.at[index, 'Proforma'] = Proforma

    return table_df


def fin(df2) -> pd.DataFrame:
    Financial = {
        'Original Loan Balance': '',
        'Current Loan Balance': '',
        'Amortization Term': '',
        'Lender': '',
        'Structure': '',
        'Index': '',
        'Spread': ''
    }

    table_df3 = pd.DataFrame(Financial.items(), columns=['Field', 'Value'])

    # Create a dictionary to map the column names for the second table
    column_mapping_table2 = {
        'Original Loan Balance': 'OriginalBalance',
        'Current Loan Balance': 'CurrentBalance',
        'Amortization Term': 'AmortizationTerm',
        'Lender': 'Lender',
        'Structure': 'Structure',
        'Index': 'Index',
        'Spread': 'Spread'
    }

    # Iterate over each row in the second table DataFrame
    for index, row in table_df3.iterrows():
        field = row['Field']
        if field in column_mapping_table2:
            column_name = column_mapping_table2[field]
            if column_name in df2.columns:
                # Extract the value from the corresponding column in the data DataFrame
                value = df2[column_name].iloc[0]

                # Check if the field requires formatting
                if field == 'Original Loan Balance' or field == 'Current Loan Balance':
                    if pd.notnull(value):
                        value = f'${value:.0f} M'
                    else:
                        value = ''
                elif field == 'Amortization Term':
                    if pd.notnull(value):
                        value = f'{value:.0f}'
                    else:
                        value = ''

                table_df3.at[index, 'Value'] = value

    # Add blank columns to Table 2
    table_df3['  '] = ''
    table_df3['Fields'] = ''
    table_df3['Values'] = ''

    # Assign static values to the additional columns
    table_df3.at[0, 'Fields'] = 'LTV'
    table_df3.at[1, 'Fields'] = 'LTC'
    table_df3.at[2, 'Fields'] = 'Maturity'
    table_df3.at[3, 'Fields'] = 'Prepayment Terms'
    table_df3.at[4, 'Fields'] = 'Current Prepay Penalty'
    table_df3.at[5, 'Fields'] = 'Extension Options'

    # Fill blank cells in the PrepaymentTerms column with an empty string
    # df2['PrepaymentTerms'] = df2['PrepaymentTerms'].fillna('')

    # Convert "LTV" to numeric (handle non-numeric values)
    try:
        ltv_value = pd.to_numeric(df2["LTV"].iloc[0], errors='coerce')
        if pd.notnull(ltv_value):
            table_df3.at[0, 'Values'] = f'{ltv_value * 100:.1f}%'
        else:
            table_df3.at[0, 'Values'] = ''
    except (ValueError, TypeError):
        table_df3.at[0, 'Values'] = ''

    # Convert "LTC" to numeric (handle non-numeric values)
    try:
        ltc_value = pd.to_numeric(df2["LTC"].iloc[0], errors='coerce')
        if pd.notnull(ltc_value):
            table_df3.at[1, 'Values'] = f'{ltc_value * 100:.1f}%'
        else:
            table_df3.at[1, 'Values'] = ''
    except (ValueError, TypeError):
        table_df3.at[1, 'Values'] = ''

    # Handle NaT in the "Maturity" column
    maturity_value = df2["Maturity"].iloc[0]
    if pd.notnull(maturity_value):
        table_df3.at[2, 'Values'] = maturity_value.strftime('%m/%d/%Y')
    else:
        table_df3.at[2, 'Values'] = ''  # Set to empty string if NaT

    # Convert "CurrentPrepayPenalty" to string
    current_prepay_penalty_value = df2["CurrentPrepayPenalty"].iloc[0]
    if pd.notnull(current_prepay_penalty_value):
        try:
            table_df3.at[4, 'Values'] = f'{current_prepay_penalty_value * 100:.0f}%'
        except ValueError:
            table_df3.at[4, 'Values'] = ''
    else:
        table_df3.at[4, 'Values'] = ''  # Set to empty string if NaN

    # Convert "ExtensionOptions" to string
    extension_options_value = df2["ExtensionOptions"].iloc[0]
    if pd.notnull(extension_options_value):
        table_df3.at[5, 'Values'] = extension_options_value
    else:
        table_df3.at[5, 'Values'] = ''  # Set to empty string if NaN

    # Fill blank cells in the DataFrame with empty strings
    for col in table_df3.columns:
        table_df3[col] = table_df3[col].fillna('')

    # Print the resulting table DataFrame
    return table_df3


def mar(df3)->pd.DataFrame:
    MO = {
    'Axio': '',
    'CoStar': '',
    'REIS': '',
    'GS Houseview': ''
}

    table_df4 = pd.DataFrame(MO.items(), columns=['Fields', '2023'])

    # Create a dictionary to map the column names and spot values
    column_mapping = {
        'Axio': {'2023': 'Axio2023', '2024': 'Axio2024','2025':'Axio2025'},
        'CoStar': {'2023':'CoStar2023', '2024':'CoStar2024','2025':'CoStar2025'},
        'REIS': {'2023': 'REIS2023', '2024': 'REIS2024','2025':'REIS2025'},
        'GS Houseview': {'2023': 'GSHouseview2023', '2024': 'GSHouseview2024','2025':'GSHouseview2025'}

    }

    # Iterate over each row in the table DataFrame
    for index, row in table_df4.iterrows():
        field = row['Fields']
        if field in column_mapping:
            _2023 = column_mapping[field]['2023']
            _2024 = column_mapping[field]['2024']
            _2025 = column_mapping[field]['2025']

            if _2023 in df3.columns and _2024 in df3.columns and _2025 in df3.columns:
                # Extract the values from the corresponding columns in the data DataFrame
                _2023 = df3[_2023].iloc[0]
                _2024 = df3[_2024].iloc[0]
                _2025 = df3[_2025].iloc[0]

                # Convert values to percentage format
                _2023 = f"{_2023:.2%}" if pd.notna(_2023) else ""
                _2024 = f"{_2024:.2%}" if pd.notna(_2024) else ""
                _2025 = f"{_2025:.2%}" if pd.notna(_2025) else ""

            table_df4.at[index, '2023'] = _2023
            table_df4.at[index, '2024'] = _2024
            table_df4.at[index, '2025'] = _2025

    # Fill NaN values with blanks
    table_df4.fillna('Fields', inplace=True)
    return table_df4


def cap(df4)->pd.DataFrame:
    CapitalProjects = {
    'Number of Units Renovated': '',
    'Cost per Unit': '',
    'Avg. ROC': ''
}

    table_df5 = pd.DataFrame(CapitalProjects.items(), columns=['Fields', 'Total'])

    # Create a dictionary to map the column names and spot values
    column_mapping = {
        'Number of Units Renovated': {'Total': 'UnitsRenovatedTotal', 'UW': 'UnitsRenovatedUW','Budget':'UnitsRenovatedBudget'},
        'Cost per Unit': {'Total':'CostperUnitTotal', 'UW':'CostperUnitUW','Budget':'CostperUnitBudget'},
        'Avg. ROC': {'Total': 'ROCTotal', 'UW': 'ROCUW','Budget':'ROCBudget'}
    }

    # Iterate over each row in the table DataFrame
    for index, row in table_df5.iterrows():
        field = row['Fields']
        if field in column_mapping:
            Total = column_mapping[field]['Total']
            UW = column_mapping[field]['UW']
            Budget = column_mapping[field]['Budget']
            
            if Total in df4.columns and UW in df4.columns and Budget in df4.columns:
                # Extract the values from the corresponding columns in the data DataFrame
                Total = df4[Total].iloc[0]
                UW = df4[UW].iloc[0]
                Budget = df4[Budget].iloc[0]
            
            # Format 'Avg. ROC' as a percentage with two decimal places and multiplied by 100
            if field == 'Avg. ROC':
                table_df5.at[index, 'Total'] = f'{Total * 100:.2f}%' if pd.notna(Total) else ''
                table_df5.at[index, 'UW'] = f'{UW * 100:.2f}%' if pd.notna(UW) else ''
                table_df5.at[index, 'Budget'] = f'{Budget * 100:.2f}%' if pd.notna(Budget) else ''
            else:
                # Format 'Number of Units Renovated' with a single decimal place
                if field == 'Number of Units Renovated':
                    table_df5.at[index, 'Total'] = f'{Total:.0f}' if pd.notna(Total) else ''
                    table_df5.at[index, 'UW'] = f'{UW:.0f}' if pd.notna(UW) else ''
                    table_df5.at[index, 'Budget'] = f'{Budget:.0f}' if pd.notna(Budget) else ''
                else:
                    # Add thousand separator and dollar symbol for 'Cost per Unit'
                    table_df5.at[index, 'Total'] = f'${Total:,.0f}' if pd.notna(Total) else ''
                    table_df5.at[index, 'UW'] = f'${UW:,.0f}' if pd.notna(UW) else ''
                    table_df5.at[index, 'Budget'] = f'${Budget:,.0f}' if pd.notna(Budget) else ''

    return table_df5


def um(df5)->pd.DataFrame:
    UnitMix = {
    'One BedRoom': '',
    'Two BedRoom': '',
    'Three BedRoom': '',
    'Studio': ''
}

    table_df6 = pd.DataFrame(UnitMix.items(), columns=['FloorPlan', 'Total Units'])

    # Create a dictionary to map the column names and spot values
    column_mapping = {
        'One BedRoom': {
            'Total Units': 'OneTotalUnit',
            'Classic Units': 'OneClassicUnit',
            'Renovated Units': 'OneRenovated',
            'Classic Rent': 'OneClassicRent',
            'Renovated Rent': 'OneRenovatedRent',
            'Cost': 'OneCost',
            'ROC': 'OneROC'
        },
        'Two BedRoom': {
            'Total Units': 'TwoTotalUnit',
            'Classic Units': 'TwoClassicUnit',
            'Renovated Units': 'TwoRenovated',
            'Classic Rent': 'TwoClassicRent',
            'Renovated Rent': 'TwoRenovatedRent',
            'Cost': 'TwoCost',
            'ROC': 'TwoROC'
        },
        'Three BedRoom': {
            'Total Units': 'ThreeTotalUnit',
            'Classic Units': 'ThreeClassicUnit',
            'Renovated Units': 'ThreeRenovated',
            'Classic Rent': 'ThreeClassicRent',
            'Renovated Rent': 'ThreeRenovatedRent',
            'Cost': 'ThreeCost',
            'ROC': 'ThreeROC'
        },
        'Studio': {
            'Total Units': 'StudioTotalUnit',
            'Classic Units': 'StudioClassicUnit',
            'Renovated Units': 'StudioRenovated',
            'Classic Rent': 'StudioClassicRent',
            'Renovated Rent': 'StudioRenovatedRent',
            'Cost': 'StudioCost',
            'ROC': 'StudioROC'}
}

    # Iterate over each row in the table DataFrame
    for index, row in table_df6.iterrows():
        field = row['FloorPlan']
        if field in column_mapping:
            TotalUnits = column_mapping[field]['Total Units']
            ClassicUnits = column_mapping[field]['Classic Units']
            RenovatedUnits = column_mapping[field]['Renovated Units']
            ClassicRent = column_mapping[field]['Classic Rent']
            RenovatedRent = column_mapping[field]['Renovated Rent']
            Cost = column_mapping[field]['Cost']
            ROC = column_mapping[field]['ROC']

            if TotalUnits in df5.columns and ClassicUnits in df5.columns and RenovatedUnits in df5.columns and ClassicRent in df5.columns and RenovatedRent in df5.columns and Cost in df5.columns and ROC in df5.columns:
                # Extract the values from the corresponding columns in the data DataFrame
                TotalUnits = f'{df5[TotalUnits].iloc[0]:.0f}' if not pd.isnull(df5[TotalUnits].iloc[0]) else ''
                ClassicUnits = f'{df5[ClassicUnits].iloc[0]:.0f}' if not pd.isnull(df5[ClassicUnits].iloc[0]) else ''
                RenovatedUnits = f'{df5[RenovatedUnits].iloc[0]:.0f}' if not pd.isnull(df5[RenovatedUnits].iloc[0]) else ''
                ClassicRent = f'{df5[ClassicRent].iloc[0]:,.2f}' if not pd.isnull(df5[ClassicRent].iloc[0]) else ''
                RenovatedRent = f'{df5[RenovatedRent].iloc[0]:,.2f}' if not pd.isnull(df5[RenovatedRent].iloc[0]) else ''
                Cost = f'{df5[Cost].iloc[0]:,.2f}' if not pd.isnull(df5[Cost].iloc[0]) else ''
                ROC = f'{df5[ROC].iloc[0] * 100:.2f}%' if not pd.isnull(df5[ROC].iloc[0]) else ''
            
        table_df6.at[index, 'Total Units'] = TotalUnits
        table_df6.at[index, 'Classic Units'] = ClassicUnits
        table_df6.at[index, 'Renovated Units'] = RenovatedUnits
        table_df6.at[index, 'Classic Rent'] = ClassicRent
        table_df6.at[index, 'Renovated Rent'] = RenovatedRent
        table_df6.at[index, 'Cost'] = Cost
        table_df6.at[index, 'ROC'] = ROC

    return table_df6
