import numpy as np
import os  # 遍历文件夹
import nibabel as nib  # nii格式一般都会用到这个包
import imageio  # 转换成图像
from PIL import Image
import numpy as np
from PIL import Image

np.set_printoptions(threshold=np.inf)


def nii_to_image(niifile):
    return 0


# filepath = r'F:\study\ai\datawhale\cv\process\resamble\imagesTr_resampled'  # 读取本代码同个文件夹下所有的nii格式的文件


slice_trans = []
def get_img(filenames,filepath,imgfile):
    for f in filenames:  # 开始读取nii文件
        s = f[-4:]
        # print(s)

        if s != '.nii':
            continue
        s1 = f[:-4]
        # print(s1)
        # imgfile_path = imgfile
        # if not os.path.exists(imgfile_path):
        #     os.mkdir(imgfile_path)
        # print("imgfile_path:" + imgfile_path)
        img_path = os.path.join(filepath, f)
        img = nib.load(img_path)  # 读取nii
        # print("img:")
        # print(img)
        print(img.shape)
        img_fdata = img.get_fdata()

        fname = f.replace('.nii', '')  # 去掉nii的后缀名
        img_f_path = imgfile
        # if not os.path.exists(img_f_path):
        #     os.mkdir(img_f_path)

        # 创建nii对应的图像的文件夹
        if not os.path.exists(img_f_path):
            os.makedirs(img_f_path) #新建文件夹
        #开始转换为图像
        if '.gz' in s1:
            x, y, z,_ = img.shape
            print("img2:")
            print(img.shape)
        else:
            x, y, z,_= img.shape
            print("img3:")
            print(img.shape)

        for i in range(z):  # z是图像的序列
            if i < 20 or i >40:continue
            slice = img_fdata[:, :, i,0]  # 选择哪个方向的切片都可以

            # 将浮点数数据缩放到0-255的范围
            scaled_slice = (slice - np.min(slice)) / (np.max(slice) - np.min(slice)) * 255

            # 将浮点数数据转换为无符号8位整数
            uint8_slice = np.uint8(scaled_slice)

            # 创建灰度图像对象
            image = Image.fromarray(uint8_slice, mode='L')

            # 保存为PNG格式

            if 'Train' in imgfile and int(s1) <= 5:
                imgfile2 = imgfile.replace('Train','Val')
                if not os.path.exists(imgfile2):
                    os.makedirs(imgfile2)
                image.save(os.path.join(imgfile2, f'{s1}_{i}_mask.png'))
            else:
                image.save(os.path.join(imgfile, f'{s1}_{i}_mask.png'))

path = r"F:\study\ai\datawhale\cv\brain_data"
filepath_train_mci = os.path.join(path,r'origin_data\Train\MCI')  # 读取本代码同个文件夹下所有的nii格式的文件
filepath_train_nc = os.path.join(path,r'origin_data\Train\NC')  # 读取本代码同个文件夹下所有的nii格式的文件
filepath_test = os.path.join(path,r'origin_data\Test')  # 读取本代码同个文件夹下所有的nii格式的文件
filenames_train_mci = os.listdir(filepath_train_mci)
filenames_train_nc = os.listdir(filepath_train_nc)
filenames_test = os.listdir(filepath_test)
savepath_train_mci = os.path.join(path,r'origin_img\Train\MCI')
savepath_train_nc = os.path.join(path,r'origin_img\Train\NC')
savepath_test = os.path.join(path,r'origin_img\Test')
get_img(filenames_train_mci,filepath_train_mci,savepath_train_mci)
get_img(filenames_train_nc,filepath_train_nc,savepath_train_nc)
get_img(filenames_test,filepath_test,savepath_test)