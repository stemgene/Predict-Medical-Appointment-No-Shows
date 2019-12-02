import pandas as pd
import numpy as np
import csv
#import pandas_profiling
import matplotlib.pyplot as plt
#%matplotlib inline
import geopandas as gpd
import pyepsg
import folium
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster

attributes = ['PatientId', 'AppointmentID','Gender', 'ScheduledDay', 'AppointmentDay', 'Age', 'Neighbourhood', 'Scholarship', 'Hipertension', 'Diabetes', 'Alcoholism', 'Handcap', 'SMS_received', 'No-show']
with open('noshowdata.csv') as csv_file:
  next(csv_file)
  csv_reader = csv.reader(csv_file, delimiter=',')
  df = pd.DataFrame(csv_reader, columns=attributes)
patient_loc = df[['Neighbourhood','PatientId']].groupby(["Neighbourhood"])
towns_keys = [el for el in patient_loc.groups.keys()] # approach of get keys after 'groupby'
patient_count = [patient_loc.count().iloc[i,0] for i in range(len(patient_loc.count()))]
towns = dict(zip(towns_keys, patient_count))

with open('towns.csv') as csv_file:
  next(csv_file)
  csv_reader = csv.reader(csv_file, delimiter=',')
  towns = {row[0]:[int(row[1]),float(row[2]),float(row[3])] for row in csv_reader} # load file is string type, need to transform float
##  towns = pd.DataFrame(csv_reader4, columns=attributes)
#print(towns)

cluster_df = df[["PatientId", 'Neighbourhood']]
cluster_df.drop(cluster_df.index[cluster_df['Neighbourhood'] == 'ILHAS OCEÂNICAS DE TRINDADE'], inplace = True)
cluster_df.drop(cluster_df.index[cluster_df['Neighbourhood'] == 'PARQUE INDUSTRIAL'], inplace = True)
whole_towns_gps = [(towns[key][1], towns[key][2]) for key in cluster_df['Neighbourhood'].values]
cluster_df.insert(2,"town gps", whole_towns_gps)
#print(cluster_df.tail(2))

# difference of 0.001(gps) = 110m
np.random.seed(0)
cov = ([-3e-8, 0],[0, 3e-8]) # range of random
patient_gps = [np.random.multivariate_normal(v,  cov , 1) for v in cluster_df['town gps'].values]
cluster_df.insert(3,"patient gps", patient_gps)
cluster_df.tail(2)


locationlist = [(v[0][0],v[0][1]) for v in cluster_df['patient gps'].values]
map2 = folium.Map(location=[-20.268857, -40.302106], tiles='cartodbdark_matter', zoom_start=13)
marker_cluster = MarkerCluster().add_to(map2)

for point in range(0, len(cluster_df['patient gps'])):
    folium.Marker(locationlist[point]).add_to(marker_cluster)
map2
map2.save('map3.html')