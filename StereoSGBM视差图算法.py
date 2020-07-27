import numpy as np
import cv2

def update(val = 0):
    stereo.setBlockSize(cv2.getTrackbarPos('window_size', 'disparity'))
    stereo.setUniquenessRatio(cv2.getTrackbarPos('uniquenessRatio', 'disparity'))
    stereo.setSpeckleWindowSize(cv2.getTrackbarPos('speckleWindowSize', 'disparity'))
    stereo.setSpeckleRange(cv2.getTrackbarPos('speckleRange', 'disparity'))
    stereo.setDisp12MaxDiff(cv2.getTrackbarPos('disp12MaxDiff', 'disparity'))

    print('computing disparity...')
    disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0

    cv2.imshow('left', imgL)
    cv2.imshow('disparity', (disp-min_disp)/num_disp)
    

if __name__ == "__main__":
    window_size = 5
    min_disp = 16
    num_disp = 192-min_disp
    blockSize = window_size
    uniquenessRatio = 1
    speckleRange = 3
    speckleWindowSize = 3
    disp12MaxDiff = 200
    P1 = 600
    P2 = 2400
    imgL = cv2.imread(r'C:\Users\Owen\Pictures\dis2.jpg')
    imgR = cv2.imread(r'C:\Users\Owen\Pictures\dis1.jpg')
    imgL = cv2.resize(imgL,dsize=None,fx=0.2,fy=0.2)
    imgR = cv2.resize(imgR,dsize=None,fx=0.2,fy=0.2)


    cv2.namedWindow('disparity')
    cv2.createTrackbar('speckleRange', 'disparity', speckleRange, 50, update)    
    cv2.createTrackbar('window_size', 'disparity', window_size, 21, update)
    cv2.createTrackbar('speckleWindowSize', 'disparity', speckleWindowSize, 200, update)
    cv2.createTrackbar('uniquenessRatio', 'disparity', uniquenessRatio, 50, update)
    cv2.createTrackbar('disp12MaxDiff', 'disparity', disp12MaxDiff, 250, update)
    stereo = cv2.StereoSGBM_create(
        minDisparity = min_disp,  #表示可能的最小视差值。通常为0，但有时校正算法会移动图像，所以参数值也要相应调整
        numDisparities = num_disp, #表示最大的视差值与最小的视差值之差，这个差值总是大于0。在当前的实现中，这个值必须要能被16整除
        blockSize = window_size,   
        uniquenessRatio = uniquenessRatio,#表示由代价函数计算得到的最好（最小）结果值比第二好的值小多少（用百分比表示）才被认为是正确的。通常在5-15之间。
        speckleRange = speckleRange,   #指每个已连接部分的最大视差变化，如果进行斑点过滤，则该参数取正值，函数会自动乘以16、一般情况下取1或2就足够了。
        speckleWindowSize = speckleWindowSize,  #表示平滑视差区域的最大窗口尺寸，以考虑噪声斑点或无效性。将它设为0就不会进行斑点过滤，否则应取50-200之间的某个值。
        disp12MaxDiff = disp12MaxDiff,  #表示在左右视图检查中最大允许的偏差（整数像素单位）。设为非正值将不做检查。
        P1 = P1,  #控制视差图平滑度的第一个参数
        P2 = P2   #控制视差图平滑度的第二个参数，值越大，视差图越平滑。P1是邻近像素间视差值变化为1时的惩罚值，
                  #p2是邻近像素间视差值变化大于1时的惩罚值。算法要求P2>P1,stereo_match.cpp样例中给出一些p1和p2的合理取值。
    )
    update()
    cv2.waitKey()
