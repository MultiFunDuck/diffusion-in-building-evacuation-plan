import cv2
import numpy as np
from datetime import datetime

from pde.diffusion import diffusion_solver as ds
from helps.gas_source import gas_source as gs
from img.img_process import img_processer as ip



img_pr =ip()

img_pr.get_contour_of_image('res/in_pics', 'res/binary_pics', 'plan.png', 'binary_plan.png')

bin_img = cv2.imread('res/binary_pics' + '/' + 'binary_plan.png')

width, height, depth = bin_img.shape



#initilazing gas sources
gas_src1 = gs(width - width//4, height - height//3, 2, 0.4)
gas_src2 = gs(width//3, height//3, 2, 0.7)
gas_src = list([gas_src1])



#initial gas density
init_density = np.zeros((width, height), np.float16)
init_density[:, :] = 0



#calculating density spread for 100 steps
num_of_frames = 100
solver = ds(bin_img, 'res/gas_spread_pics', 'gas_spread', gas_src, 0.1, num_of_frames)
solver.start_simulation(init_density, num_of_frames)



#making gif out of density on map pictures
date = datetime.today().strftime('%Y%m%H%M%S')
img_pr.make_gif('res/gas_spread_pics', 'res/gas_spread_gif', 'gas_spread', 'gas_spread' + date, num_of_frames)

