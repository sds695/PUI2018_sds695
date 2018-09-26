from __future__ import print_function
import json
try:
    import urllib2 as urllib
except ImportError:
    import urllib.request as urllib
import os
import sys


apikey = sys.argv[1]
bus=sys.argv[2]
count=0
url = "http://api.prod.obanyc.com/api/siri/vehicle-monitoring.json?key=%s"%(apikey)

print (url)
response = urllib.urlopen(url)
data = response.read().decode("utf-8")
#use the json.loads method to obtain a dictionary representation of the responose string 
dataDict = json.loads(data)

fout = open(sys.argv[3], "w")
fout.write("Latitude,Longitude,Stop Name,Stop Status\n")

vehicle_monitoring_delivery=dataDict['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']
l=[]
for v in vehicle_monitoring_delivery:
	if(v['MonitoredVehicleJourney']['PublishedLineName']==bus):
		latitude=v['MonitoredVehicleJourney']['VehicleLocation']['Latitude']
		longitude=v['MonitoredVehicleJourney']['VehicleLocation']['Longitude']
		if(v['MonitoredVehicleJourney']['MonitoredCall']['StopPointName']!={}):
			stop_name=v['MonitoredVehicleJourney']['MonitoredCall']['StopPointName']
		else:
			stop_name="N/A"
		if(v['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['PresentableDistance']!={}):
			stop_status=v['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['PresentableDistance']
		else:
			stop_status="N/A"
		fout.write(str(latitude)+","+str(longitude)+","+str(stop_name)+","+str(stop_status)+"\n")
fout.close()
