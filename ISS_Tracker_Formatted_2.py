import requests
import math
import usb.core
import usb.util
import struct
import time
import serial

#----------------------------------------------------
def fetch_iss_current_location():
  url = 'https://api.wheretheiss.at/v1/satellites/25544'

  # GET Request
  response = requests.get(url)
  
  if response.status_code == 200:
      # Parse the JSON response 
      iss_data = response.json()
      return {
          'latitude': iss_data['latitude'],
          'longitude': iss_data['longitude'],
          'altitude': iss_data['altitude']
      }
  else:
      response.raise_for_status()

#----------------------------------------------------
# Constants
EARTH_RADIUS = 6371.0  # Earth's radius in kilometers

def calculate_bearing(lat1, lon1, lat2, lon2):

   #Calculate the bearing using the Haversine formula
  lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
  dlon = lon2 - lon1
  x = math.sin(dlon) * math.cos(lat2)
  y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(dlon))
  initial_bearing = math.atan2(x, y)
  bearing = (math.degrees(initial_bearing) + 360) % 360
  return bearing

#----------------------------------------------------

def calculate_angles_to_iss(observer_lat, observer_lon, iss_data):
  
  # Extract ISS position data
  iss_lat = iss_data['latitude']
  iss_lon = iss_data['longitude']
  iss_alt = iss_data['altitude']

  # Calculate the bearing using the Haversine formula
  bearing_degrees = calculate_bearing(observer_lat, observer_lon, iss_lat, iss_lon)

   # Convert all latitudes and longitudes from degrees to radians
  observer_lat_rad = math.radians(observer_lat)
  observer_lon_rad = math.radians(observer_lon)
  iss_lat_rad = math.radians(iss_lat)
  iss_lon_rad = math.radians(iss_lon)
  
  # Calculate the ECEF coordinates for the observer
  observer_x = EARTH_RADIUS * math.cos(observer_lat_rad) * math.cos(observer_lon_rad)
  observer_y = EARTH_RADIUS * math.cos(observer_lat_rad) * math.sin(observer_lon_rad)
  observer_z = EARTH_RADIUS * math.sin(observer_lat_rad)
  
  # Calculate the ECEF coordinates for the ISS
  iss_x = (EARTH_RADIUS + iss_alt) * math.cos(iss_lat_rad) * math.cos(iss_lon_rad)
  iss_y = (EARTH_RADIUS + iss_alt) * math.cos(iss_lat_rad) * math.sin(iss_lon_rad)
  iss_z = (EARTH_RADIUS + iss_alt) * math.sin(iss_lat_rad)
  
  # Calculate the vector from the observer to the ISS
  vector_x = iss_x - observer_x
  vector_y = iss_y - observer_y
  vector_z = iss_z - observer_z
  
  # Calculate the vertical angle (elevation)
  horizontal_distance = math.sqrt(vector_x**2 + vector_y**2)
  elevation = math.atan2(vector_z, horizontal_distance)
  elevation_degrees = math.degrees(elevation)

  return elevation_degrees, bearing_degrees

#----------------------------------------------------
# USB Trasnmit function to our STM32 

def send_data_to_stm32(ser, elevation_angle, bearing_angle):

  elevation_angle = int(elevation_angle)
  bearing_angle = int(bearing_angle)

  elevation_str = f"{elevation_angle:+04d}" if elevation_angle >= 0 else f"{elevation_angle:04d}"
  bearing_str = f"{bearing_angle:+04d}" if bearing_angle >= 0 else f"{bearing_angle:04d}"

  # Create a string formatted as "±000:±000\n"
  data_string = f"{elevation_str}:{bearing_str}\n"
  print(f"Data to send: {data_string}")
  ser.write(data_string.encode())



#----------------------------------------------------
def main():
  # ICT Cubes - Altitude Ignored
  observer_latitude = 50.77939  # Latitude (observer)
  observer_longitude = 6.06308  # Longitude (observer)

  # COM Port of ST-Link
  ser = serial.Serial('COM5', 115200)

  try:

      try:
          iss_data = fetch_iss_current_location()
          elevation, bearing = calculate_angles_to_iss(observer_latitude, observer_longitude, iss_data)

          elevation_int = int(elevation)
          bearing_int = int(bearing)

          print(f"Elevation Angle: {elevation_int}, Bearing Angle: {bearing_int}")
          send_data_to_stm32(ser, elevation_int, bearing_int)
          print("Data sent to STM32")

      except Exception as e:
          print(f"An error occurred: {e}")
      time.sleep(2)

  finally:
    ser.close()
#----------------------------------------------------

if __name__ == "__main__":
    main()



  
