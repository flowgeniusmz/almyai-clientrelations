import streamlit as st
import pandas as pd
from simple_salesforce import Salesforce
import uuid
import streamlit_modal as modal
from functions import pagesetup as ps

# Function to fetch cases from Salesforce
@st.cache
def fetch_cases():
    sf = Salesforce(username=st.secrets.salesforce.sfuser, password=st.secrets.salesforce.sfcred, security_token=st.secrets.salesforce.sftoken)
    query = """
        SELECT Id, AccountId, Account.Name, Account.ShippingStreet, Account.ShippingCity,
        Account.ShippingState, Account.ShippingPostalCode, Account.ShippingLongitude,
        Account.ShippingLatitude, Type, Status, Queues__c, Owner.Name, CreatedDate 
        FROM Case Where Account.Subsidiary__c = 'Alma Lasers , Inc.' 
        ORDER BY CreatedDate DESC 
        LIMIT 200
        """
    data = sf.query(query)
    records = data['records']
    data_new = []
    for record in records:
        row_data = {
            'caseid': record['Id'],
            'accountid': record['AccountId'],
            'accountname': record.get('Account', {}).get('Name', ''),
            'type': record.get('Type', ''),
            'status': record.get('Status', ''),
            'queue': record.get('Queues__c', ''),
            'owner': record.get('Owner', {}).get('Name', ''),
            # Add other fields as needed
        }
        data_new.append(row_data)
    return pd.DataFrame(data_new)

def show_case_modal(case):
    with modal.container():
        outer_col1, modal_container, outer_col2 = st.columns([1, 2, 1])

        with modal_container:
            col1, col2 = st.columns(2)

            with col1:
                st.write("Case Details")
                st.text(f"Case ID: {case['caseid']}")
                st.text(f"Account ID: {case['accountid']}")
                st.text(f"Account Name: {case['accountname']}")
                st.text(f"Type: {case['type']}")
                st.text(f"Status: {case['status']}")
                st.text(f"Queue: {case['queue']}")
                st.text(f"Owner: {case['owner']}")
                # Make fields editable
                type_input = st.text_input("Type", case['type'])
                status_input = st.text_input("Status", case['status'])
                queue_input = st.text_input("Queue", case['queue'])
                # Add other editable fields as needed

            with col2:
                with st.form("update_form"):
                    comments = st.text_area("Comments", value="")
                    # Add form submission logic if needed
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        # Logic to handle form submission
                        st.success("Form submitted!")
                        # Update Salesforce record logic goes here

            if st.button("Exit"):
                modal.close()

def generate_row(row_id, case):
    row_container = st.empty()
    row_columns = row_container.columns((2, 2, 1, 1, 1, 1, 1))
    row_columns[0].write(case['accountname'])
    row_columns[1].write(case['accountid'])
    row_columns[2].write(case['type'])
    row_columns[3].write(case['status'])
    row_columns[4].write(case['queue'])
    row_columns[5].write(case['owner'])

    if row_columns[6].button("Details", key=f"btn_{row_id}", type="primary"):
        show_case_modal(case)

def main():
    ps.set_title("Client Relations", "Salesforce Case Manager")
    ps.set_page_overview("Overview", "The **Salesforce Case Manager** page enables you to view all **in process, technical service, client relations** cases assigned to you. You can view and edit the details and the case will automatically be updated in Salesforce.")
    ps.set_blue_header("Case List")
    headercontainer = st.container()
    with headercontainer:
        header_columns = st.columns((2, 2, 1, 1, 1, 1,1))
        header_columns[0].markdown("**Account Name**")
        header_columns[1].markdown("**Account Id**")
        header_columns[2].markdown("**Case Type**")
        header_columns[3].markdown("**Case Status**")
        header_columns[4].markdown("**Case Queue**")
        header_columns[5].markdown("**Case Owner**")
        header_columns[6].markdown("**Details**")
    st.divider()

    cases_df = fetch_cases()

    if "rows" not in st.session_state:
        st.session_state["rows"] = []

    if len(st.session_state["rows"]) == 0:
        for _, case in cases_df.iterrows():
            st.session_state["rows"].append((str(uuid.uuid4()), case))

    for row_id, case in st.session_state["rows"]:
        generate_row(row_id, case)

    if len(st.session_state["rows"]) > 0:
        st.subheader("Case Data")
        display = st.columns(1)
        data = pd.DataFrame([case for _, case in st.session_state["rows"]])
        display[0].dataframe(data=data, use_container_width=True)

if __name__ == "__main__":
    main()
