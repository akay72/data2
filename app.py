import streamlit as st
import pandas as pd
st.set_page_config(layout="wide")

col1, col2 = st.columns([1, 3])

with col1:
    logo_path = 'Logo-w(1).png'  # Replace with the path to your logo file
    st.image(logo_path, use_column_width='always')

from st_aggrid import AgGrid, GridOptionsBuilder

# Function to get unique values from a column after splitting by comma
def get_unique_values_from_column(df_column):
    unique_values = sorted(set([x.strip().upper() for x in df_column.str.split(',').explode()]))
    return ['All'] + unique_values  # Include 'All' option



# Radio button to select the type of firms
col1, col2 = st.columns([2, 3])
with col1:
    st.markdown("## Demand Request Details")
with col2:

    firm_type = st.radio("Panel Firms", ('Yes', 'No'))

# Load the data from the selected sheet in Excel
excel_path = 'updated file_ea77359d-19df-4ad1-9857-28efdcec9fa4.xlsx'
sheet_name = 'Panel Firms' if firm_type == 'Yes' else 'Non_Panel Firms'
df = pd.read_excel(excel_path, sheet_name=sheet_name)

# Get unique values for practice areas and jurisdictions from the loaded sheet
practice_areas = get_unique_values_from_column(df['Practice Area'])
jurisdictions = get_unique_values_from_column(df['Jurisdiction'])
firm_names = ['All'] + df['Firm Names'].unique().tolist()

# Dropdown for selecting practice area
col1, col2 = st.columns([2, 3])
with col1:
    st.write("What is the main practice area your request relates to?")
with col2:    
    selected_practice_area = col2.selectbox('Select a Practice Area', practice_areas)

# Dropdown for selecting jurisdiction
col1, col2 = st.columns([2, 3])
with col1:
    st.write("What is the main jurisdiction your request relates to? Please select as many as relevant for your request. ")
with col2:     
    selected_jurisdiction = st.selectbox('Select a Jurisdiction', jurisdictions)
    
def filter_firms_by_selection(df, practice_area, jurisdiction):
    if practice_area != 'All':
        df = df[df['Practice Area'].str.upper().str.contains(practice_area.upper(), na=False)]
    if jurisdiction != 'All':
        df = df[df['Jurisdiction'].str.upper().str.contains(jurisdiction.upper(), na=False)]
    return df['Firm Names'].unique().tolist()    

filtered_firm_names = filter_firms_by_selection(df, selected_practice_area, selected_jurisdiction)
filtered_firm_names.insert(0, 'All')

# Dropdown for selecting firm names based on practice area and jurisdiction
col1, col2 = st.columns([2, 3])
with col1:
    st.write("Select the firms you would like to reach out to for an offer? ")
with col2:    
    # Using multiselect instead of selectbox
    selected_firm_names = st.multiselect('Select Firm Names', filtered_firm_names, default='All')


spend_ranges = [
    "Less than USD 5.000",
    "Between USD 5.001 and USD 10.000",
    "Between USD 10.001 and USD 25.000",
    "Between USD 25.001 and USD 50.000",
    "Between USD 50.001 and USD 100.000",
    "Between USD 100.001 and USD 500.000",
    "Between USD 500.001 and USD 1m",
    "Between USD 1m and USD 2.5m",
    "Between USD 2.5m and USD 5m",
    "More than USD 5m"
]

col1, col2 = st.columns([2, 3])
with col1:
      st.write("What do you, in the best of your experience, will be the expected spend for this matter? ")
with col2:
    selected_spend_range = st.selectbox('Select a Spend Range', spend_ranges)

cost_objects = [
    "Litigation, General",
    "Litigation, Patent Defensive",
    "Litigation, Patent Offensive RIPL",
    "Litigation, Tax disputes",
    "Legal -Labor",
    "Legal -Insurance claims",
    "M&A",
    "Trade Compliance",
    "Trademark",
    "Domain Names",
    "Legal -Compliance (excl. Trade Compliance)",
    "Legal -Corporate Governance",
    "Legal -Legalization/Notarius Publicus",
    "Legal -General Commercial",

]

cost_centers = [
    658116,
    658112,
    692115,
    658115,
    658113,
    658114,
    658122,
    658123,
    693101,
    693102,
    658111,
    658124,
    658125,
    658117

]

cost_object_to_center = dict(zip(cost_objects, cost_centers))
col1, col2 = st.columns([2, 3])
# Dropdown to select cost object
with col1:
    st.write("What cost object will be the costs for this engagement be booked against (cost center / Purchase Order etc.)?  ")

with col2:    
    selected_cost_object = st.selectbox('Select a Cost Object', cost_objects)

# Optionally display the corresponding cost center if needed
    selected_cost_center = cost_object_to_center[selected_cost_object]
    st.write("Selected Cost Center: ", selected_cost_center)

# Function to apply filters only when a specific option is selected
# Function to apply filters only when a specific option is selected
def apply_filters(df, practice_area, jurisdiction, firm_names):
    if practice_area != 'All':
        df = df[df['Practice Area'].str.upper().str.contains(practice_area.upper(), na=False)]
    if jurisdiction != 'All':
        df = df[df['Jurisdiction'].str.upper().str.contains(jurisdiction.upper(), na=False)]
    if firm_names != ['All']:  # Now firm_names is a list, not a single value
        df = df[df['Firm Names'].isin(firm_names)]
    return df



# Apply the filtering
filtered_df = apply_filters(df, selected_practice_area, selected_jurisdiction, selected_firm_names)
columns_to_display = ['Firm Names', 'Contact Name', 'Phone Number', 'Email']
filtered_df = filtered_df[columns_to_display]
# Display the filtered data in the app

gb = GridOptionsBuilder.from_dataframe(filtered_df)
gb.configure_pagination()  # Enable pagination
gb.configure_side_bar()  # Enable side bar
gb.configure_selection('multiple', use_checkbox=True, rowMultiSelectWithClick=True, suppressRowDeselection=False)
gridOptions = gb.build()

# Display the DataFrame with checkboxes using AgGrid

with st.container():
    aggrid_response = AgGrid(
        filtered_df,
        gridOptions=gridOptions,
        # height=300,
        resizable=True,
        filterable=True,
        sortable=True,
        width='100%',
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,  # Required to allow JsCode for the cell renderer
    )

# Access the selected rows

# selected_rows = aggrid_response['selected_rows']

# # Display selected rows
# if st.button('Show Selected Rows'):
#     st.dataframe(selected_rows)


st.markdown('---')

# Create two placeholder containers for the buttons
custom_css = """
<style>


.placeholder-button {
    color: black; /* White text color */
    background-color:#04A3D0; /* Blue background color */
    padding: 5px 20px; /* Padding inside the button */
    border-radius: 5px; /* Rounded corners */
    border:4px solid #F9DA19;
    font-size: x-large;
    text-align: center; /* Center the text */
    display: block; /* Make sure it takes up the full container width */
    # margin: 0px 0; /* Spacing above and below the element */
}
</style>
"""

# Inject custom CSS with markdown
st.markdown(custom_css, unsafe_allow_html=True)

# Use markdown to create the divider
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Create two columns with placeholders styled as buttons
col1, col2 = st.columns(2)

# Use markdown to place styled text within the columns
col1.markdown('<div class="placeholder-button">Submit my selected firms for approval</div>', unsafe_allow_html=True)
col2.markdown('<div class="placeholder-button">Invite selected firms to my e-auction</div>', unsafe_allow_html=True)
