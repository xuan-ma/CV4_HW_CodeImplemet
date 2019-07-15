# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 20:38:19 2019

@author: ww
"""

'''
Please combine image crop, color shift, rotation and perspective transform together to complete a data augmentation script.
Your code need to be completed in Python/C++ in .py or .cpp file with comments and readme file to indicate how to use.
'''
import cv2
import numpy as np

class ImgAugmentation:
    location='./'
    img_fmt='.jpg'
    def __init__(self,sourceImag,bShown=False):
        img1=cv2.imread(self.location+sourceImag)
        self.imgName=sourceImag.split('.')[0]
        self.img=img1
        self.B,self.G,self.R=cv2.split(self.img)
        self.rows=img1.shape[0]
        self.cols= img1.shape[1]
        if bShown:
            cv2.imshow(self.imgName,self.img)
            key =cv2.waitKey()
            if key == 27:
                cv2.destroyAllWindows()
    def imgCrop(self,x1,x2,y1,y2,img=None):
        max_x=int(max(x1,x2))
        min_x=int(min(x1,x2))
        max_y=int(max(y1,y2))
        min_y=int(min(y1,y2))
        self.img_crop=self.img[min_y:max_y+1,min_x:max_x+1]
        return self.img_crop
    def gammaTfm(self,gamma):
        '''
        给图加亮(暗)/增加对比度
        '''
        pass
        gamma_tab=np.array([(i/255)**gamma*255 for i in range(256)]).astype('uint8')
        return cv2.LUT(self.img, gamma_tab)
    def histTfm(self,chnl=''):
        '''
        直方图均衡化:
            输入chnl：需要均衡化的通道
        '''
        for i in range(len(chnl)):
            if 'B' in chnl:
                self.B=cv2.equalizeHist(self.B)
            if 'G' in chnl:
                self.G=cv2.equalizeHist(self.G)
            if 'R' in chnl:
                self.R=cv2.equalizeHist(self.R)
        return cv2.merge((self.B,self.G,self.R))
    def colorShift(self):
        pass
    def simTfm(self,center=(),angle=0,scale=1):
        '''
        如果angle=0,scale=1代表只做平移操作
        '''
        if not center:
            center=(self.cols/2,self.rows/2)
        if angle==0 and scale==1:
            M_sim=np.array([[1,0,center[0]],
                            [0,1,center[1]]])
        else:
            M_sim=cv2.getRotationMatrix2D(center,angle,scale)
        return cv2.warpAffine(self.img,M_sim,(self.cols,self.rows))
    def affTfm(self,pts1,pts2):
        M_aff=cv2.getAffineTransform(pts1,pts2)
        print('M_aff\n',M_aff)
        img_aff=cv2.warpAffine(self.img,M_aff,(self.cols,self.rows))
        return img_aff
    def persTfm(self,pts1,pts2):
        M_pres=cv2.getPerspectiveTransform(pts1,pts2)
#        print('M_pres:\n',M_pres)
        img_pers=cv2.warpPerspective(self.img,M_pres,(int(max(pts2[:,0])),int(max(pts2[:,1]))))
        return img_pers
    def saveImg(self,object_name='',Img_save=None):
        
        if Img_save is None:
            Img_save=self.img
            print('Img_save',Img_save)
        object_name=self.imgName+'_'+object_name+self.img_fmt
        print('object_name',object_name)
#        print('Img_save',Img_save)
        cv2.imwrite(object_name,Img_save)
    def showImg(self,title,Img_show):
        cv2.imshow(title,Img_show)
        key =cv2.waitKey()
        if key == 27:
            cv2.destroyAllWindows()
    def getAffPts(self,center=()):
        '''
        获取仿射变换需要3个点的前后坐标:
            输入：需要变换的图像，变换区域的中心
            输出：变换前和变换后3个点的坐标
        '''
        if not center:
            x,y =  self.cols/2.0,self.rows/2.0
        else:
            x,y =  center
        x_r_1=0.4
        x_r_2=0.4
        y_r_1=0.75
        y_r_2=0.9
        pts1=np.float32([[x*x_r_1     , y*y_r_1],
                         [x*(2-x_r_1) , y*y_r_1],
                         [(2-x_r_2)*x , y*y_r_2]])
        pts2=np.float32([[x*0.4                                  , y*0.4  ], #( x0 , y0)
                         [int(self.cols/2*(2-x_r_1-x_r_2))+x*0.1  , 0 ], #( x1 , y1)
                         [int(self.cols/2*(2-x_r_1-x_r_2))  , int(self.rows/2*(y_r_2-y_r_1))+y*0.1 ] #(x2 , y2)
                                                                                             ])
        print('pts1\n',pts1)
        print('pts2\n',pts2)
        return pts1,pts2
    def getPersPts(self,center=()):
        '''
        获取投影变换需要4个点的前后坐标:
            输入：需要变换的图像，变换区域的中心
            输出：变换前和变换后4个点的坐标
        '''
#        print('center',center)
        if not center:
            x,y=self.cols/2.0,self.rows/2.0
        else:
            x,y = center
        '''
        #在过center平行于x轴和y轴的两条线上分别选取两个点
        Origin(0,0)---------------------------------------------------------------
                                         ……
        ( x_r_1*x , y_r_1*y)------------...--------------( (2-x_r_1)*x , y_r_1*y)
        |                                ……                         |
        |                            center(x,y)                    |
        |                               ……                          |
        (x_r_2 * x , y_r_2*y)-----------...--------------( (2-x_r_2)*x , y_r_2*y)
        '''
        x_r_1=0.4
        x_r_2=0.4
        y_r_1=0.75
        y_r_2=0.9
        pts1=np.float32([[x*x_r_1     , y*y_r_1],
                         [x*(2-x_r_1) , y*y_r_1],
                         [(2-x_r_2)*x , y*y_r_2],
                         [x*x_r_2     , y*y_r_2]])
        scale_y=6
        scale_x=1
        '''
        将投影变换后的图像的四个顶点作为变换后的点
        ( x0 , y0)------------...--------------( x1 , y1)
             |                ……                    |
             |             center(x,y)              |
             |                ……                    |
        (x3 , y3)------------...---------------( x2 , y2)
        '''
        pts2=np.float32([[0,                                          0], #( x0 , y0)
                         [int(self.cols/2*(2-x_r_1-x_r_2))*scale_x  , 0], #( x1 , y1)
                         [int(self.cols/2*(2-x_r_1-x_r_2))*scale_x  , scale_y*int(self.rows/2*(y_r_2-y_r_1))], #( x2 , y2)
                         [0                                         , scale_y*int(self.rows/2*(y_r_2-y_r_1))]]) #(x3 , y3)

        return pts1,pts2
if __name__=='__main__':
    object_file='source2_paint.jpg'
    obj2=ImgAugmentation(object_file,True)
    #Crop img
    Img_crop=obj2.imgCrop(obj2.cols*0.2,obj2.cols*0.8,obj2.rows*0.2,obj2.rows*0.8)
    obj2.showImg('Crop',Img_crop)
    #Img perspective transform
    pts1,pts2=obj2.getPersPts((obj2.cols*0.5,obj2.rows*0.8))
    Img_pers=obj2.persTfm(pts1,pts2)
    obj2.showImg('PersTfm',Img_pers)
    obj2.saveImg('PersTfm',Img_pers)
   #gamma transform
    gamma=2.0
    Img_gamma_Bigger=obj2.gammaTfm(gamma)    #gamma > 1
    obj2.showImg('GammaTfm--(Gamma>1)',Img_gamma_Bigger)
    obj2.saveImg('GammaTfm_Gamma_{}'.format(gamma),Img_gamma_Bigger)
    gamma=0.5
    Img_gamma_Smaller=obj2.gammaTfm(0.5) #gamma < 1
    obj2.showImg('GammaTfm--(Gamma<1)',Img_gamma_Smaller)
    obj2.saveImg('GammaTfm_Gamma_{}'.format(gamma),Img_gamma_Smaller)
    #Histogram transform
    channel='BGR'
    Img_hist=obj2.histTfm(channel)
    obj2.showImg('HistTfm_Channel_{}'.format(channel),Img_hist)
    obj2.saveImg('HistTfm_Channel_{}'.format(channel),Img_hist)
    #Similarity transform
    Img_sim=obj2.simTfm((obj2.cols*0.5,obj2.rows*0.5),-30,0.5)
    obj2.showImg('SimTfm',Img_sim)
    obj2.saveImg('SimTfm',Img_sim)
    Img_translation=obj2.simTfm((obj2.cols*0.5,obj2.rows*0.5))
    obj2.showImg('SimTfm_translation',Img_translation)
    obj2.saveImg('SimTfm_translation',Img_translation)
    Img_scale=obj2.simTfm(scale=0.55)
    obj2.showImg('SimTfm_scale',Img_scale)
    obj2.saveImg('SimTfm_scale',Img_scale)
    pts1,pts2=obj2.getAffPts()
    Img_aff=obj2.affTfm(pts1,pts2)
    obj2.showImg('AffTfm',Img_aff)
    obj2.saveImg('AffTfm',Img_aff)
    