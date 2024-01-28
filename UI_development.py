import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title('Accident Analysis App')

csv_file = st.file_uploader('Upload a CSV file containing accident data', type=['csv'])


def read_csv(csv):
    if csv is not None:
        st.write('CSV file uploaded successfully!')

        data = pd.read_csv(csv)

        date_format = '%d/%m/%Y'
        data['ACCIDENT_DATE'] = pd.to_datetime(data['ACCIDENT_DATE'], format=date_format)

        st.title("Crash Statistics Data Filtering")

        # create a dropdown to select the year and accident type input
        selected_year = st.selectbox("Select a Year", list(range(2013, 2019)))
        filtered_data = data[data['ACCIDENT_DATE'].dt.year == selected_year].copy()
        accident_type = st.text_input("Accident Type:")

        if st.button(f"Show Data for {selected_year}"):
            selected_columns = ['OBJECTID', 'ACCIDENT_NO', 'ACCIDENT_STATUS',
                                'ACCIDENT_DATE', 'ACCIDENT_TIME', 'SEVERITY']
            st.dataframe(filtered_data[selected_columns])

        # create a separate button to display accident type
        display_data_for_accident_type(filtered_data, selected_year, accident_type)
        # create a button to display accidents per hour
        display_accidents_per_hour(filtered_data, selected_year)
        # create a button for alcohol impacts
        display_alcohol_impacts(filtered_data, selected_year)
        # make a button for speed zones
        display_speed_zones(data, selected_year)
    else:
        'Please upload a csv file'


def display_data_for_accident_type(filtered_data, selected_year, accident_type):
    if st.button(f"Show Data for Accident type in {selected_year}"):
        if not accident_type:
            st.warning("Please enter an accident type.")
        else:
            filtered_data_type = filtered_data[filtered_data['ACCIDENT_TYPE'].str.contains(accident_type, case=False)]
            filtered_data_type['ACCIDENT_DATE'] = filtered_data_type['ACCIDENT_DATE'].dt.date
            selected_columns = ['OBJECTID', 'ACCIDENT_NO', 'ACCIDENT_TYPE',
                                'ACCIDENT_DATE', 'ACCIDENT_TIME', 'SEVERITY']
            st.dataframe(filtered_data_type[selected_columns])


def display_accidents_per_hour(filtered_data, selected_year):
    if st.button("Accidents per hour"):
        time_format = '%H.%M.%S'
        filtered_data['ACCIDENT_TIME'] = pd.to_datetime(filtered_data['ACCIDENT_TIME'], format=time_format)
        filtered_data['hour'] = filtered_data['ACCIDENT_TIME'].dt.hour

        # group the data by hour and count the number of accidents for each hour
        hourly_counts = filtered_data.groupby('hour')['ACCIDENT_TIME'].count()

        # create a bar chart for accidents per hour and label the chart
        chart_data = pd.DataFrame({'Hour': hourly_counts.index, 'Accidents': hourly_counts.values})

        fig, ax = plt.subplots()
        ax.bar(chart_data['Hour'], chart_data['Accidents'])
        ax.set_xlabel('Hour')
        ax.set_ylabel('Accidents')
        ax.set_title(f'Hourly Accident Counts (24h) for {selected_year}')
        ax.set_xticks(range(24))

        st.pyplot(fig)


def display_alcohol_impacts(filtered_data, selected_year):
    if st.button("Alcohol Impacts"):
        # filter data where ALCOHOLTIME is yes
        alcohol_impact_data = filtered_data[filtered_data['ALCOHOLTIME'] == 'Yes'].copy()
        alcohol_impact_data['ACCIDENT_DATE'] = alcohol_impact_data['ACCIDENT_DATE'].dt.date

        selected_columns = ['OBJECTID', 'ACCIDENT_NO', 'ACCIDENT_TYPE',
                            'ACCIDENT_DATE', 'SEVERITY']
        st.dataframe(alcohol_impact_data[selected_columns])

        alcohol_impact_count = filtered_data[filtered_data['ALCOHOLTIME'] == 'Yes'].shape[0]
        non_alcohol_impact_count = filtered_data[filtered_data['ALCOHOLTIME'] == 'No'].shape[0]

        # Create a pie chart
        labels = ['Accidents with Alcohol Impact', 'Accidents without Alcohol Impact']
        sizes = [alcohol_impact_count, non_alcohol_impact_count]
        colors = ['lightcoral', 'lightblue']
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')
        plt.title(f'Alcohol Impacts in {selected_year}')
        st.pyplot(fig)


def display_speed_zones(data, selected_year):
    if st.button(f"Show data per Speed Zone for {selected_year}"):
        # takes out all strings from SPEED_ZONE and leaves only numbers
        data['SPEED_ZONE'] = data['SPEED_ZONE'].str.extract('(\d+)')
        # analyze the data and display the result
        accident_counts = data['SPEED_ZONE'].value_counts().reset_index()
        accident_counts.columns = ['SPEED_ZONE', 'Total Accidents']
        # display the total accidents per speed zone in a table
        st.write('Total Accidents per Speed Zone:')
        st.write(accident_counts)
        fig, ax = plt.subplots()
        plt.bar(accident_counts['SPEED_ZONE'], accident_counts['Total Accidents'])
        plt.xlabel('Speed Zone Km/h')
        plt.ylabel('Total Accidents')
        plt.title(f'Total Accidents per Speed Zone for {selected_year}')
        st.pyplot(fig)

read_csv(csv_file)
