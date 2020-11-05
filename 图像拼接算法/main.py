import cv2
import numpy as np
import os
import time
import matplotlib.pyplot as plt
class figure_mat():  #画板类   图片插入光标位置 
    def __init__(self,shape,np_type):
        self.figure = np.ones(shape,dtype = np_type)
        self.figure = self.figure * 255
        self.insert_x = 0
        self.insert_y = 0
        self.width_used = 0
        self.height_used = 0
        self.figure_width = shape[0]
        self.figure_height = shape[1]
        self.img_record = []

    def save_img_shape(self,img): #记录图片大小
        self.img_record.append(img.shape)
    

def get_img_list(file_path): 
    filelist = os.listdir(file_path) #该文件夹下的所有文件
    img_list = []
    for file in filelist: #遍历所有文件 包括文件夹
        Olddir = os.path.join(path,file)#原来文件夹的路径
        if os.path.isdir(Olddir):#如果是文件夹，则跳过
            continue
        else:
            img_list.append(Olddir)

    return img_list

def cv_show(name,img):
    img = cv2.resize(img,dsize =None,fx = 0.1,fy = 0.1)
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def img_shape_sort(img_file_list):
    img_list = []
    shape_list = []  
    original_list = [] #存储图片的列表，提高遍历速度
    original_file_list = [] #存储图片的路径
    for i,original_file in enumerate(img_file_list):
        original = cv2.imread(original_file) #读取
        original_list.append(original)  #存入图片
        original_file_list.append(original_file) #存入图片路径列表
        shape_list.append(int(original.shape[0]*original.shape[1]))
    shape_list.sort(reverse = False )  #升序
    
    for shape in shape_list: #遍历图片大小列表
        for j,img in enumerate(original_list): #遍历图片路径列表
            if (original_list[j].shape[0]*original_list[j].shape[1])== shape : #判断大小是否符合
                if original_file_list[j] not in img_list:
                    img_list.append(original_file_list[j])  #若是符合，读入
    

        print("正在遍历")
    return img_list



    


start = time.time()
path=r"D:\teeth_project\pictures\test\normal2"  #图片文件夹路径



# figure_width = input("请输入画板的宽:") 
# figure_height = input("请输入画板的宽:")
figure_height = 5000
figure_width  = 5000
img_type = '.jpg'  #支持jpg/bmp/png/tiff

figure1 = figure_mat((figure_width,figure_height,3),np.uint8)
img_list = get_img_list(path)

result_num = 0

img_list = img_shape_sort(img_list)

for i,original_file in enumerate(img_list):
    original = cv2.imread(original_file)
    if( original.shape[1] + figure1.insert_x < figure1.figure_width): #若是加上这张图片后宽度超过范围，那么:
        if(original.shape[0] + figure1.insert_y < figure1.figure_height):    #判断排入下一行是否会超过画板高度
            figure1.figure[figure1.insert_y:figure1.insert_y+original.shape[0],figure1.insert_x:figure1.insert_x+original.shape[1]] = original   #若是不超过,#按位置填入，并且记录
            figure1.save_img_shape(original)   #记录
            figure1.insert_x += original.shape[1]  #更新插入光标
            figure1.width_used += original.shape[1] #更新已使用x
            if(figure1.height_used < original.shape[0]): #让y等于这一行最大的一个值。
                figure1.height_used = original.shape[0] #更新已使用y
            
        else:  #超过了高度
            #cv_show('figure',figure1.figure)
            result_num += 1
            result_name = path + '\\result\\result' + str(result_num) + img_type  
            cv2.imwrite(result_name,figure1.figure)                               #保存图片
            figure1 = figure_mat((figure_width,figure_height,3),np.uint8)             #清空figure_mat
            
    

    else:  #换行:
        figure1.insert_y += figure1.height_used #换行
        if(original.shape[0] + figure1.insert_y < figure1.figure_height):    #判断排入下一行是否会超过画板高度   
            figure1.insert_x = 0
            figure1.height_used = 0 #重新统计一行的高度
            figure1.figure[figure1.insert_y:figure1.insert_y+original.shape[0],figure1.insert_x:figure1.insert_x+original.shape[1]] = original   #若是不超过,#按位置填入，并且记录
            figure1.save_img_shape(original)   #记录
            figure1.insert_x += original.shape[1]  #更新插入光标
            figure1.width_used += original.shape[1] #更新已使用x
            
            if(figure1.height_used < original.shape[0]): #让y等于这一行最大的一个值。
                figure1.height_used += original.shape[0] #更新已使用y

        else:  #超过了高度
            #cv_show('figure',figure1.figure)
            result_num += 1
            result_name = path + '\\result\\result' + str(result_num) + img_type  
            cv2.imwrite(result_name,figure1.figure)                               #保存图片
            figure1 = figure_mat((figure_width,figure_height,3),np.uint8)     #清空figure_mat
 

result_num +=1
#cv_show('figure',figure1.figure)
result_name = path + '\\result\\result' + str(result_num) + img_type  
cv2.imwrite(result_name,figure1.figure)                               #保存图片
figure1 = figure_mat((figure_width,figure_height,3),np.uint8)     #清空figure_mat
    


result_list = os.listdir((path + '\\result'))
plt.figure()

for i,img_file in enumerate(result_list):
    plt.subplot(len(result_list)/2,len(result_list)/2,i+1)
    img = cv2.imread( path + '\\result\\'+ img_file)
    img = cv2.resize(img,dsize = None,fx=0.5,fy=0.5) #对图片显示效果进行缩小，减小运算时间，不影响结果图片的图像质量。
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    plt.imshow(img)


plt.show()
    
