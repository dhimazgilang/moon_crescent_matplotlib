# COba pakai matplotlib

from matplotlib import pyplot as plt, patches
from skyfield.api import load
from skyfield.framelib import ecliptic_frame
import math
import numpy as np

#from skyfield.api import N, W, S, E, load, wgs84
from skyfield import api
from skyfield.trigonometry import position_angle_of

# ==========
# input user
# ==========
# latitude = lintang lokasi pengamatan (string)
# logitude = bujur lokasi pengamatan   (string)
# height   = ketinggian lokasi pengamatan dalam meter (float)
# format untuk variabel latitude dan langitude:
#    untuk lintang utara,   latitude : 'xx.xxxx N' 
#    untuk lintang selatan, latitude : 'xx.xxxx S'
#    untuk bujur timur,     longitude: 'xx.xxxx E' 
#    untuk bujur barat,     longitude: 'xx.xxxx W'
#
# year,month,day,hour,minute,sec = 
# masing-masing tahun, bulan,tanggal, jam, menit,detik dalam UTC
# masing-masing berformat integer
#
# file_output = string nama file output
# Sertakan juga format file penyimpanan
# contoh : "moon.png", "bulan.jpg"
#
# verbose = boolean variable untuk menampilkan/tidak 
# hasil perhitungan pada terminal
#
# shadow_cirlce = boolean untuk menampilkan/tidak lingkaran 
# bantu bayangan. True untuk menampilkan, False untuk mematikan
#
# ==================================================
latitude    = '6.824444 S'
longitude   = '107.615556 E'
height      = 728
year, month, day, hour, minute, sec = 2023, 2, 21, 10, 53, 21
file_output = 'moon_2.png'
verbose     = True
shadow_circle = False
# ==================================================
# Menentukan persentase iluminasi bulan (geosentrik)
ts = load.timescale()
t = ts.utc(year, month, day, hour, minute, sec)

eph = load('de421.bsp')
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']

e = earth.at(t)
s = e.observe(sun).apparent()
m = e.observe(moon).apparent()

_, slon, _ = s.frame_latlon(ecliptic_frame)
_, mlon, _ = m.frame_latlon(ecliptic_frame)

moon_percent = 100.0 * m.fraction_illuminated(sun)
if verbose == True:
	print()
	print('Percent illuminated: {0:.1f}%'.format(moon_percent))

# Koordinat toposentrik altitude dan azimtuh matahari
location = api.Topos(latitude, longitude, elevation_m=height)

sun_pos = (earth + location).at(t).observe(sun).apparent()
s_altitude, s_azimuth, s_distance = sun_pos.altaz()

# Koordinat toposentrik altitude dan azimtuh bulan
moon_pos = (earth + location).at(t).observe(moon).apparent()
m_altitude, m_azimuth, m_distance = moon_pos.altaz()

if verbose == True:  
	print("Solar coordinate")
	print(f"Altitude: {s_altitude.degrees:.4f} °")
	print(f"Azimuth: {s_azimuth.degrees:.4f} °")
	print()
	print("Lunar coordinate")
	print(f"Altitude: {m_altitude.degrees:.4f} °")
	print(f"Azimuth: {m_azimuth.degrees:.4f} °")

position_angle = position_angle_of(moon_pos.altaz(), sun_pos.altaz())
if verbose == True:
	print()
	print('Position angel of moon and sun:')
	print(position_angle)
	
# Plot penampakan bulan
position_angle = position_angle.degrees + 270.
#position_angle = 90
r = 1
h = (1 - 2*moon_percent/100)


r_big = (h**2 + r)/(2*h)
x_big = (r_big-h)*math.cos(np.radians(position_angle))
y_big = (r_big-h)*math.sin(np.radians(position_angle))

plt.rcParams["figure.figsize"] = [4.00, 4.00]
plt.rcParams["figure.autolayout"] = True
fig = plt.figure()
ax = fig.add_subplot()

circle1 = patches.Circle((0, 0), radius=1, color='#ffcc00')
circle2 = patches.Circle((x_big, y_big), radius=r_big, color='#154870')
circle3 = patches.Circle((x_big, y_big), radius=r_big, edgecolor = '#cc0000', linewidth=1)

ax.add_patch(circle1)
ax.add_patch(circle2)
if shadow_circle == True:
	ax.add_patch(circle3)
	ax.plot([-h*np.cos(np.radians(position_angle)),x_big],[-h*np.sin(np.radians(position_angle)),y_big],'#cc0000','-',linewidth=1)

ax.set_xlim(-2,2)
ax.set_ylim(-2,2)
ax.set_facecolor("#154870")

#plt.axis('off')
#ax.plot([0,0],[-1,1],'#cc0000','-',linewidth=1)

#ax.plot(np.arange(-1,0.2,0.2),[0]*6,'r.')
#plt.text(1.5, 0 ,'zenith', color = '#ffcc00')
plt.text(-0.2,1.8,'zenith', color = '#ffcc00')
plt.savefig(file_output)
plt.show()
