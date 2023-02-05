# COba pakai matplotlib
from matplotlib import pyplot as plt, patches
import math
import numpy as np

# input user
# ==========
# moon_percent = persentase ilumninasi bulan
# nilai moon_percent harus < 50 
#
# position_angle = sudut posisi antara bulan dan matahari
# sudut posisi dihitung dari arah utara ke arah timur
# position_angle dinyatakan dalam derajat
# nilai harus antara 0 dan 360
#
# shadow_cirlce = boolean untuk menampilkan/tidak lingkaran 
# bantu bayangan. True untuk menampilkan, False untuk mematikan
#
# file_output = string nama file output
# Sertakan juga format file penyimpanan
# contoh : "moon.png", "bulan.jpg"

moon_percent   = 20
position_angle = 330
shadow_circle  = True
file_output    = "moon.png"

# Plot penampakan bulan
moon_percent = moon_percent/100.

r = 1
h = (1 - 2*moon_percent)


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
plt.text(1.5, 0 ,'Utara', color = '#ffcc00')
plt.text(-0.2,1.8,'Timur', color = '#ffcc00')
plt.savefig('moon.png')
plt.show()
