import cv2
import numpy as np
from helps.condition_handler import conditions_handler as ch
from img.img_process import img_processer as ip



class diffusion_solver:

    

    def __init__(self, img, out_path, solution_name, gas_sources, diff_coef, work_time):
        self.img = img
        self.out_path = out_path
        self.sol_name = solution_name
        self.gas_sources = gas_sources
        self.diff_coef = diff_coef
        self.work_time = work_time



    #convolute density with gaussian filter
    #the same as calculating finite-diff laplace operator 
    #in 2-nd order approximation
    def convolute(self, density, x, y):
        filter = [[1, 4, 7, 4 ,1],
                  [4, 16, 26, 16 ,4],
                  [7, 26, 0, 26, 7],
                  [4, 16, 26, 16 ,4],
                  [1, 4, 7, 4 ,1]]
        data = density[x-2 : x+3, y-2 : y+3]
        return sum(sum(filter*data))/273




    def finite_diff_step(self, density, x, y, gas_src, step):
        power = gas_src.power
        dist = gas_src.dist_from_src(x, y)
        D = self.diff_coef
        w, h , d = self.img.shape
        area = w*h
        
        total_steps = self.work_time
        t = step/total_steps
        
        
        conv_res = self.convolute(density, x, y)

        #multiplier representing diffusion process, corresponds to green's function 
        #for diffusion equation. 
        coef = (1/(4*np.pi*D*t)**(1/2))*(np.e**(-(dist/area)/2*D*t))

        return coef*power*conv_res
    




    def density_per_src_change(self, prev_density, gas_src,  step):
        #initializing zero-density
        map_img = self.img
        width, height, depth = map_img.shape
        cur_density = np.zeros((width, height))


        xc, yc = gas_src.x, gas_src.y
        power = gas_src.power

        
        

        #iterating over square of pixels with size $step$, but not outside picture
        for x in range(max(2, xc - step), min(width - 2, xc + step)):
            for y in range(max(2, yc - step), min(height - 2, yc + step)):
                
                #inside the source gas density is equal to power of source
                if(gas_src.contain(x,y)):
                    cur_density[x,y] = power


                #making sure gas does not spread through wall

                #cutting square of pixels to circle, 
                #because gas can't spread faster than calculation
                elif(not ch.is_len_away_from_wall(map_img, 1, x, y) and ch.is_in_range(x - xc, y - yc, step)):

                    xy_density = prev_density[x,y] + self.finite_diff_step(prev_density, x, y, gas_src, step)
                    cur_density[x, y] = min(power, xy_density)

        return cur_density
        



    #iterationg over gas_sources
    def calc_cur_density(self, prev_density, step):
        width, height, d = self.img.shape
        cur_density = np.zeros((width, height), np.float16)
        for gas_src in self.gas_sources:
            density_per_source = self.density_per_src_change(prev_density, gas_src, step)
            cur_density = cur_density + density_per_source
        return cur_density




    #making one time step calculation 
    #saving calculated density on map pic
    def make_time_step(self, prev_density, step):

        density = self.calc_cur_density(prev_density, step)
        ip.magnitude_to_map(self.img, self.out_path, self.sol_name, density, step)
        return density
    



    #initial function that starts the whole process
    def start_simulation(self, init_density, num_of_steps):
        prev_density = init_density
        for t in range(1, num_of_steps):
            density = self.make_time_step(prev_density, t)
            prev_density = density
    
