#模拟任意二维带电结构的电势分布与电场强度 made by Jia DM


'''
调用使用到的依赖扩展包
'''
import numpy as np #矩阵计算
import matplotlib.pyplot as plt #矩阵画图
from PIL import Image #图片处理

#mac 用户需要额外设置图像交互界面
import matplotlib as mpl
mpl.use('TkAgg')

'''
resolution表示分辨率、格点数目;
coorx，coory分别为x和y方向的坐标;
ele_potential表示二维的电势；
x_strength表示二维的x方向电场强度；
y_strength表示二维的y方向电场强度；
'''
resolution = 201
coorx = np.linspace(-1,1,resolution)
coory = np.linspace(-1,1,resolution)
x_strength = np.zeros([resolution,resolution])
y_strength = np.zeros([resolution,resolution])
ele_potential = np.zeros([resolution,resolution])


'''
读取图片im,将im转为二维的数组image
'''
im = Image.open('1.jpg')
im = im.resize((resolution,resolution))
im = np.array(im)

'''
判断图片中像素的颜色，将红色定义为-1，蓝色定义为1,白色定义为0，分别表示像素带负电，正电和不带电。
'''
image = np.zeros([resolution,resolution])
image[im[:,:,2]<100] = -1
image[im[:,:,0]<100] = 1
image = image[::-1,:]

'''
二维空间中任意位置的电势：
'''
for i in range(resolution):
    for j in range(resolution):
        #判断二维空间中（i,j）位置的电荷是否为0
        if image[i,j] != 0 :
            #定义电势的指标（k,l）
            for k in range(resolution): 
                for l in range(resolution):
                #(k,l)位置的电势等于每个像素的电势 kq/r(ij,kl)之和
                    if (k==i and l==j)==False:
                        #计算 ij位置与kl位置的距离r
                        r = np.sqrt((coorx[k]-coorx[i])**2+(coory[l]-coory[j])**2)
                        #将每个像素的电势叠加到kl位置上
                        ele_potential[k,l] += image[i,j]/r #假设电荷q和参数k等于1

'''
二维空间中任意位置的电场强度分量Ex和Ey：
'''
for k in range(1,resolution-1): #x方向
    for l in range(1,resolution-1): #y方向
        #(k,l)位置的电场强度分为x和y方向 -dU/dx与-dU/dy，利用差分公式可得:
        x_strength[k,l] = -(ele_potential[k+1,l]-ele_potential[k-1,l])/(coorx[k+1]-coorx[k-1])
        y_strength[k,l] = -(ele_potential[k,l+1]-ele_potential[k,l-1])/(coory[l+1]-coory[l-1])            

'''
定义作图函数：
'''
def plot_figure(coorx,coory,pot,x_str,y_str):
    scale = np.abs(y_str).mean()*2
    y_str[y_str>scale] = scale
    y_str[y_str<-scale] = -scale
    x_str[x_str>scale] = scale
    x_str[x_str<-scale] = -scale
    norm = np.sqrt(x_str**2+y_str**2)
    x_str[:] = x_str/norm.max() 
    y_str[:] = y_str/norm.max() 
    scale2 = np.abs(pot).mean()*5
    pot[pot>scale2] = scale2
    pot[pot<-scale2] = -scale2
    levels = np.linspace(-np.abs(pot).max(), np.abs(pot).max(),41)
    fig,ax = plt.subplots(2,2)
    levels_image = np.array([-1,0,1])
    ax[0,0].imshow(im)
    ax[0,0].set_aspect(1)
    ax[0,1].contourf(coorx,coory,pot,levels=levels, cmap='RdBu')
    ax[0,1].set_aspect(1)
    lw = 2*norm/norm.max()
    ax[1,0].streamplot(coorx,coory,y_str, x_str, density=1, color='k', linewidth=lw)
    ax[1,0].set_aspect(1)
    ax[1,1].contourf(coorx,coory,pot,levels=levels, cmap='RdBu')
    ax[1,1].streamplot(coorx,coory,y_str, x_str, density=1, color='k', linewidth=lw)
    ax[1,1].set_aspect(1)
    plt.show()


'''
作图：
'''
plot_figure(coorx,coory,ele_potential,x_strength,y_strength)

