import cv2
import numpy as np
import imageio



class img_processer:



    #that's some StackOverflow script for getting only b/w part of pic
    @staticmethod
    def get_contour_of_image(in_path, out_path, pic_name, out_pic_name):
        out_pic_name = "binary_" + pic_name

        inputImage = cv2.imread(in_path + '/' + pic_name)
        imgFloat = inputImage.astype(np.cfloat) / 255.
        kChannel = 1 - np.max(imgFloat, axis=2)
        kChannel = (255 * kChannel).astype(np.uint8)

        binaryThresh = 190
        _, binaryImage = cv2.threshold(kChannel, binaryThresh, 255, cv2.THRESH_BINARY)


        def areaFilter(minArea, inputImage):
        # Perform an area filter on the binary blobs:
            componentsNumber, labeledImage, componentStats, componentCentroids = \
                cv2.connectedComponentsWithStats(inputImage, connectivity=4)
            remainingComponentLabels = [i for i in range(1, componentsNumber) if componentStats[i][4] >= minArea]
            filteredImage = np.where(np.isin(labeledImage, remainingComponentLabels) == True, 255, 0).astype('uint8')

            return filteredImage

        minArea = 100
        binaryImage = areaFilter(minArea, binaryImage)

        kernelSize = 3
        opIterations = 2
        morphKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelSize, kernelSize))
        binaryImage = cv2.morphologyEx(binaryImage, cv2.MORPH_CLOSE, morphKernel, None, None, opIterations, cv2.BORDER_REFLECT101)
        cv2.imwrite(out_path + '/' + out_pic_name, cv2.bitwise_not(binaryImage))




    #used to convert 2d density array to 3d img, so we can picture gas dencity
    #on building map
    @staticmethod
    def np_array_to_cv_img(img_width, img_height, array):
        img = np.zeros((img_width, img_height, 3))
        img[:,:,0] = 0
        img[:,:,1] = 255*(array[:,:])
        img[:,:,2] = 255*(array[:,:])
        return img
    



    #adding pic of dencity with building map pic
    @staticmethod
    def magnitude_to_map(map_img, out_folder, pic_name, magnitude, num_of_step):
        width, height, d = map_img.shape
        path = out_folder + '/' + pic_name + '_' + str(num_of_step)  + '.png'
        map_with_density = img_processer.np_array_to_cv_img(width, height, magnitude)
        cv2.imwrite(path, map_img - map_with_density)




    #making gif out of consequtive $map on density$ pictures
    @staticmethod
    def make_gif(in_pic_path, out_gif_path, in_pic_name, out_gif_name, num_of_pics):
        filenames = list()
        for num in range(1, num_of_pics - 1):
            filenames.append(in_pic_path + '/' + in_pic_name + '_' + str(num) + '.png')
        images = []
        for filename in filenames:
            images.append(imageio.imread(filename))
        imageio.mimsave(out_gif_path + '/' + out_gif_name + '.gif', images)