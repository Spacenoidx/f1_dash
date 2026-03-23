import streamlit as st
import pandas as pd
from processor import get_season_events, get_meeting_data, get_selected_session_data, get_session_results
import datetime

def display_meeting_results(meeting_key, year, meeting_name):
    """Display results/visualization for the selected meeting"""
    st.subheader(f"Results for {year} {meeting_name}")
    
    
    
    # TODO: Fetch and display results data based on meeting_key
    
    
    meeting_data = get_meeting_data(meeting_key)  # This will return the meeting data, you can process it to extract results
    st.dataframe(meeting_data)  # Display the raw meeting data for now, you can customize this to show specific results
    
    
    # Example: results = get_race_results(meeting_key)
    # st.dataframe(results)
    # st.bar_chart(results)
    
    st.info(f"Displaying results for meeting key: {meeting_key}")
    

    

def main():
    st.title("Formula 1 Season Events Visualizer")
    
    # Check if viewing results
    if st.session_state.get('viewing_results', False):
        if st.button("← Back to Events"):
            st.session_state.viewing_results = False
            st.rerun()
        
        display_meeting_results(
            st.session_state.selected_meeting_key,
            st.session_state.selected_year,
            st.session_state.selected_meeting_name
        )
        return
    
    # check if viewing session data
    if st.session_state.get('viewing_session', False):
        if st.button("← Back to Events"):
            st.session_state.viewing_session = False
            st.rerun()
        
        selected_session_name = st.session_state.get('session_selector')
        sessions_data = get_meeting_data(st.session_state.selected_meeting_key)
        selected_session = next((session for session in sessions_data if session['session_name'] == selected_session_name), None)
        if selected_session:
            session_key = selected_session['session_key']
            session_results_data = get_session_results(session_key)
            st.write(f"Data for session: {selected_session_name} of {st.session_state.selected_year} {st.session_state.selected_meeting_name}")
            st.dataframe(session_results_data)  # Display the raw session data for now, you can customize this to show specific results
        else:
            st.warning("Selected session data not found.")
        
        return
    
    # Show events list
    year = st.number_input("Enter the year of the season you want to visualize:", min_value=1950, max_value=datetime.datetime.now().year, value=2023)
    
    events = None
    if st.button("Get Season Events"):
        events = get_season_events(year)
        st.session_state.events = events
        st.session_state.current_year = year
    elif 'events' in st.session_state and st.session_state.get('current_year') == year:
        events = st.session_state.events
    
    if events is not None:
        st.subheader(f"Events for the {year} Formula 1 World Championship:")
        #Convert column names to more readable format
        display_events = events.copy()
        display_events.columns = [col.replace('_', ' ').title() for col in display_events.columns]
        #Titlize the meeting names
        display_events['Meeting Official Name'] = display_events['Meeting Official Name'].str.title()
        #correct indexing to start from 1 instead of 0
        display_events.index = display_events.index + 1
        #give index a name
        display_events.index.name = 'Event Number'
        
        # Display dataframe
        st.dataframe(display_events)
        
        # Add selectbox for meeting selection
        meeting_options = display_events['Meeting Name'].tolist()
        selected_meeting = st.selectbox("Select a Meeting to get its Key:", 
                                        options = meeting_options, 
                                        key='meeting_selector', 
                                        index=None,
                                        placeholder="Select a Meeting")
        
        if selected_meeting is not None:
            # Find the index of the selected meeting
            selected_index = meeting_options.index(selected_meeting)
            
            # Get the original events to access meeting_key
            original_events = events  # Use the stored events
            meeting_key = original_events.iloc[selected_index]['meeting_key']
            
            # Store in session_state
            st.session_state.selected_meeting_key = meeting_key
            st.session_state.selected_meeting_name = selected_meeting
            st.session_state.selected_year = year
            st.success(f"Selected Meeting Key: *{meeting_key}* for **{year} {selected_meeting}**", icon="✅")
            
            sessions_data = get_meeting_data(meeting_key)
            st.write("Sessions Data:")
            st.selectbox("Select a Session to view details:", options=[session['session_name'] for session in sessions_data], key='session_selector')    
                    # Add button to display results only after a meeting is selected
            if meeting_key:
                if st.button("Get Session Data"):
                    st.session_state.viewing_session = True
                    st.rerun()
                    
            if st.session_state.get('viewing_session', False):
                selected_session_name = st.session_state.get('session_selector')
                selected_session = next((session for session in sessions_data if session['session_name'] == selected_session_name), None)
                if selected_session:
                    session_key = selected_session['session_key']
                    session_data = get_selected_session_data(session_key)
                    st.write(f"Data for session: {selected_session_name}")
                    st.dataframe(session_data)  # Display the raw session data for now, you can customize this to show specific results
            
            
        
        # Display results if already selected (on reruns)
            elif 'selected_meeting_key' in st.session_state:
                if st.button("View Meeting Results"):
                    st.session_state.viewing_session = True
                    st.rerun()
                    
    
            
            
            
            

            
# def meeting_data():
#     if 'selected_meeting_key' in st.session_state:
#         meeting_key = st.session_state.selected_meeting_key
#         # Here you can use the meeting_key to fetch more data about the selected meeting
#         # For example, you could call another function that gets detailed information about the meeting
#         st.write(f"Fetching data for meeting key: {meeting_key}")
#     else:
#         st.warning("Please select a meeting first to see its details.")

if __name__ == "__main__":
    main()


