
#class used in $diffusion.py$ to check conditions for x,y 
#coords on pic 
class conditions_handler:              
    

    @staticmethod
    def is_on_pic(img, x, y):
        width, height, depth = img.shape
        return (1 < x and x < height - 1) and (1 < y and y < width - 1)
    
    
    @staticmethod
    def is_in_range(x, y, rad):
        return x*x + y*y < rad*rad

    
    @staticmethod
    def is_len_away_from_wall(img, len, x, y):
            for dx in range(-len, len):
                for dy in range(-len, len):
                    if(sum(img[x + dx, y + dy]) < 255*2.8):
                        return True