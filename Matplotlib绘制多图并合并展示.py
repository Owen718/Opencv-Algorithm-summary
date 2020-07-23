import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif']=['SimHei']  #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False  #用来正常显示负号

t = np.arange(0.0,2.0,0.1)
s = np.sin(t * np.pi)

plt.figure(figsize=(8,8),dpi=80)
plt.figure(1)  #表示取第一块画板，通俗地讲，一个画板就是一张图，如果你有多个画板，那么最后就会弹出多张图。
ax1 = plt.subplot(221)
ax1.plot(t,s, color="r",linestyle = "--")
ax2 = plt.subplot(222)
ax2.plot(t,s,color="y",linestyle = "-")
ax3 = plt.subplot(223)
ax3.plot(t,s,color="g",linestyle = "-.")
ax4 = plt.subplot(224)
ax4.plot(t,s,color="b",linestyle = ":")



plt.show()

plt.figure(figsize=(8,8), dpi=80)

ax1 = plt.subplot(221)
plt.plot([1,2,3,4],[4,5,7,8], color="r",linestyle = "--")
ax2 = plt.subplot(222)
plt.plot([1,2,3,5],[2,3,5,7],color="y",linestyle = "-")
ax3 = plt.subplot(212)
plt.plot([1,2,3,4],[11,22,33,44],color="g",linestyle = "-.")

plt.show()

plt.figure(figsize=(12, 10), dpi=80)

ax1=plt.subplot2grid((3,3),(0,0),colspan=3,rowspan=1)#相当于格子分成3行3列,列跨度为3，行跨度为1
ax1.plot([1,2],[1,2]) #轴的范围，x轴，y轴。 
ax1.set_title('ax1_title')
ax2=plt.subplot2grid((3,3),(1,0),colspan=2,rowspan=1)#格子分为3行3列，列跨度为2，行跨度为1
ax2.plot([2,4,6],[7,9,15])
ax3=plt.subplot2grid((3,3),(1,2),colspan=1,rowspan=1)
x = np.arange(4)
y = np.array([15,20,18,25])
ax3.bar(x,y)
ax4=plt.subplot2grid((3,3),(2,0),colspan=1,rowspan=1)
ax5=plt.subplot2grid((3,3),(2,1),colspan=2,rowspan=1)
plt.show()