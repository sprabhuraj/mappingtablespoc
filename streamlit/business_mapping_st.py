import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session

st.title("Business Mapping Editor")

# Get the current session context
#session = get_active_session()

connection_parameters = {
 "account": "cub02553",
 "user": "JSOLIAP",
 "password": "CpVhen9bwuhG7Zg",
 "role": "SF_BUILD_NATIVE_APPS_INTERNAL",  # optional
 "warehouse": "LAB_POC_WH",  # optional
 "database": "BUSINESS_MAPPING_APP"
}  

session = Session.builder.configs(connection_parameters).create()

column_configuration = {
    "Oppty_GCoE_Branch_Type": st.column_config.SelectboxColumn(
                "Oppty GCOE Branch Type",
                help="Branch Type",
                width="medium",
                options=[
                    "Direct",
                    "Indirect",
                    "(none)",
                ],
            )
}

# Create a form
with st.form("mapping_form"):
    st.caption("Add or update the mappings in the table below")
    #  Create a data frame from a table
    df = session.sql('SELECT Oppty_GCoE_Branch_Type, Oppty_GCoE_Case_Owner_CoEBranch FROM CORE.BUSINESS_MAPPING_TABLE')
    df.collect()
    # Convert it into a Pandas data frame
    pdf = df.to_pandas()
    edited_pdf = st.data_editor(pdf, column_config=column_configuration, use_container_width=True, num_rows="dynamic")
    submit_button = st.form_submit_button("Save Data")

if submit_button:
    try:
        session.write_pandas(edited_pdf, "BUSINESS_MAPPING_TABLE", overwrite = True)
        session.sql('GRANT SELECT ON TABLE CORE.BUSINESS_MAPPING_TABLE TO APPLICATION ROLE APP_PUBLIC').collect()
        st.write('Data saved to table.')
    except:
        st.write('Error saving to table.')
