#This script cleans the Blight Violations csv file produced by the City of Detroit's Dept of Administrative Hearings.
#The script will reduce all violations to only those violations occuring in the last five years, and it will aggregate
#violations by the fine amount if they reoccur at the same location.
#The script was created by Paul McCord on 6-19-18.

#Import modules
import sys
import os
import numpy as np
import pandas as pd

#Blight data
blight_data = 'C:\\Users\\Paul McCord\\Google Drive\\Personal\\Detroit_GISAnalystII\\Preparation\\GIS_Data\\blightViolations.csv'

#Define Local Variables
outputLocation = "C:\\Users\\Paul McCord\\Google Drive\\Personal\\Detroit_GISAnalystII\\Preparation\\GIS_Data"

#Convert Blight csv file to Pandas data frame
#The 8th, 26th, and 27th column of the csv file have mixed data types.
#These columns are not important for this analysis, so set all to dtype String.
blight_df = pd.read_csv(blight_data, dtype = {8:'S50', 26: 'S50', 27: 'S50'})

#Drop columns from data frame that aren't needed
drop_list = ['Ticket ID', 'Ticket Number', 'Agency Name', 'Inspector Name', 'Violator ID', 'Mailing Address Street Number', 
			'Mailing Address Street Name', 'Mailing Address City', 'Mailing Address State', 'Mailing Address Zip Code', 
			'Mailing Address Non-USA Code', 'Mailing Address Country', 'Hearing Date', 'Hearing Time', 'Disposition', 
			'Payment Date (Most Recent)', 'Payment Status', 'Collection Status', 'Violation Location']
blight_df = blight_df.drop(drop_list, axis = 1)

#Remove violations that took place more than 5 years ago
blight_df['ViolationYear'] = blight_df['Violation Date'].str[-4:]
blight_df['ViolationYear'] = blight_df['ViolationYear'].astype('i4')
blight_recent_df = blight_df[blight_df['ViolationYear'] >= 2013]

#Aggregate violation payments if more than one occurred at a residence
#Need to remove commas from fine violation column, then convert to float
blight_recent_df['TotalFines'] = blight_recent_df['Judgment Amount (Total Due)'].str.replace(',', '')
blight_recent_df['TotalFines'] = blight_recent_df['TotalFines'].astype(float)
blight_agg_df = blight_recent_df.groupby(['Violation Address']).agg({'TotalFines': sum, 'Violation Latitude': 'first',
																	'Violation Longitude': 'first'})

#Remove observations where the fine was $0
blight_agg_df = blight_agg_df[blight_agg_df['TotalFines'] != 0]

#Remove NaN observations in fines, latitude, and longitude
blight_agg_df = blight_agg_df.dropna(subset = ['Violation Latitude', 'Violation Longitude', 'TotalFines'])

#Output csv file
blight_agg_df.to_csv(os.path.join(outputLocation, 'blightClean.csv'))
