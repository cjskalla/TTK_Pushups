import streamlit as st
import pandas as pd
from datetime import date

input_file = pd.read_excel("inputs.xlsx")

tribal_members = [
                    "Bino",
                    "Calvin",
                    "Carter",
                    "Charlie",
                    "David",
                    "Kade",
                    "Parker",
                    "Petey",
                    "Ryan",
                    "Tauke",
                    "Von"
                    ]

# Get the current date
current_date = date.today().strftime("%#m/%d/%Y")

#Title
title = st.markdown(
        f"""
        <h3 style="
            text-align: center;
            font-family: Forum;
            font-weight: 100;
            font-size: 175%;
            ">
            Select a Tribal Member to Log {current_date}
        </h1>
        """,
        unsafe_allow_html=True
    )

tribal_member = st.selectbox(
    "",
    tribal_members,
    index=None,
    placeholder="Tribal Member"
)



if tribal_member:

    submit = st.button(f'Log {current_date}',
                    use_container_width=True)


    if submit: 
    
        submission = pd.DataFrame({
            'Tribal Member': [tribal_member],
            'Day' : current_date,
            'Pushups': 1
            }
        )

        input_file = pd.concat([input_file, submission], ignore_index=True)

        input_file.to_excel("inputs.xlsx", index=False)

        st.write(f"You logged pushups for {tribal_member} for {current_date}")







#Creating data editor session
if 'data_editor' not in st.session_state:
    st.session_state['data_editor'] = False

#create button to turn data editor on
def start_editing():
    st.session_state['data_editor'] = True


edit_data = st.button('Edit Previous Days',
                    use_container_width=True,
                    on_click=start_editing)


#If editing data has turned to TRUE
if st.session_state['data_editor']:    
    
    edited_data = st.data_editor(input_file[["Tribal Member", "Day", "Pushups"]],
                                column_config= {
                                    "Tribal Member": "Tribal Member",
                                    "Day" : st.column_config.DatetimeColumn(
                                        "Day",
                                        format="MM/DD/YYYY"
                                    ),
                                    "Pushups" : st.column_config.SelectboxColumn(
                                        "Pushups",
                                        options= [0,1],
                                        required=True
                                    )
                                },
                                disabled=["Tribal Member", "Day"],
                                hide_index=True,
                                use_container_width=True
                                )
    
    #Creating data editor session
    if 'commit_change' not in st.session_state:
        st.session_state['commit_change'] = False
    
    #create button to turn data editor on
    def transform_changes():
        st.session_state['commit_change'] = True

    col = st.columns([2, 1])

    with col[0]: 
        #Commit Changes button
        commit_changes = st.button(
            label="Submit Changes",
            on_click=transform_changes,
            use_container_width=True
            )
    
    with col[1]:
        #Cancel button
        cancel_button = st.button(
            label="Cancel Edits",
            on_click=transform_changes,
            use_container_width=True
            )
    
    #Perform all transformations after Changes Commit
    if st.session_state['commit_change']:

        edited_data.to_excel("inputs.xlsx", index=False)

        st.session_state['commit_change'] = False        
        st.session_state['data_editor'] = False

        st.experimental_rerun()
        


        
