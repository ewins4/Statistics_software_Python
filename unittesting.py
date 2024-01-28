import unittest
import pandas as pd
from io import StringIO
from unittest.mock import patch
from UI_development import process_data


class TestAccidentAnalysisApp(unittest.TestCase):

    def setUp(self):
        # Create a sample CSV data for testing
        data = {
            'OBJECTID': [1, 2, 3],
            'ACCIDENT_NO': ['A1', 'A2', 'A3'],
            'ACCIDENT_STATUS': ['Open', 'Closed', 'Open'],
            'ACCIDENT_DATE': ['01/01/2018', '02/02/2019', '03/03/2020'],
            'ACCIDENT_TIME': ['08:00:00', '09:00:00', '10:00:00'],
            'SEVERITY': ['Minor', 'Major', 'Minor'],
            'ACCIDENT_TYPE': ['Collision', 'Rollover', 'Collision'],
            'ALCOHOLTIME': ['Yes', 'No', 'Yes'],
            'SPEED_ZONE': ['50 km/h', '60 km/h', '70 km/h']
        }
        self.sample_data = pd.DataFrame(data)

    @patch('streamlit.file_uploader')
    def test_file_upload(self, mock_file_uploader):
        mock_file_uploader.return_value = StringIO(self.sample_data.to_csv(index=False))
        data = process_data()
        self.assertEqual(len(data), len(self.sample_data))

    def test_filter_data_by_year(self):
        data = process_data(self.sample_data)
        filtered_data = process_data.filter_data_by_year(data, 2019)
        self.assertEqual(len(filtered_data), 1)
        self.assertTrue((filtered_data['ACCIDENT_DATE'].dt.year == 2019).all())

    def test_filter_data_by_accident_type(self):
        data = process_data(self.sample_data)
        filtered_data = process_data.filter_data_by_accident_type(data, 'Collision')
        self.assertEqual(len(filtered_data), 2)
        self.assertTrue((filtered_data['ACCIDENT_TYPE'] == 'Collision').all())

    def test_calculate_accidents_per_hour(self):
        data = process_data(self.sample_data)
        hourly_counts = process_data.calculate_accidents_per_hour(data)
        self.assertEqual(hourly_counts[8], 1)
        self.assertEqual(hourly_counts[9], 1)
        self.assertEqual(hourly_counts[10], 1)

    def test_alcohol_impacts(self):
        data = process_data(self.sample_data)
        alcohol_data, non_alcohol_data = process_data.alcohol_impacts(data)
        self.assertEqual(len(alcohol_data), 2)
        self.assertEqual(len(non_alcohol_data), 1)
        self.assertEqual(alcohol_data['ALCOHOLTIME'].unique(), ['Yes'])
        self.assertEqual(non_alcohol_data['ALCOHOLTIME'].unique(), ['No'])

    def test_speed_zone_analysis(self):
        data = process_data(self.sample_data)
        speed_zone_counts = process_data.speed_zone_analysis(data)
        self.assertEqual(speed_zone_counts['SPEED_ZONE'].tolist(), ['50', '60', '70'])
        self.assertEqual(speed_zone_counts['Total Accidents'].tolist(), [1, 1, 1])


if __name__ == '__main__':
    unittest.main()



