from img.img_process import img_processer as ip

from datetime import datetime

date = datetime.today().strftime('%Y%m%H%M%S')

img_pr =ip()
img_pr.make_gif('res/gas_spread_pics', 'res/gas_spread_gif', 'gas_spread', 'gas_spread' + date, 699)