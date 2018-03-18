# -*- coding: utf-8 -*-



# import time
# N = 1000
# st = time.clock()
# for i in range(N):
#     p = round((i+1)*100/N)
#     duration = round(time.clock()-st, 2)
#     remaining = round(duration*100/(0.01+p)-duration,2)
#     print("进度:{0}%，已耗时:{1}s，预计剩余时间:{2}s".format(p,duration,remaining)+"\r")
#     time.sleep(0.01)


# from __future__ import division
#  
# import sys,time
# j = '#'
# if __name__ == '__main__':
#     for i in range(1,61):
#         j += '#'
#         sys.stdout.write(str(int((i/60)*100))+'%  ||'+j+'->'+"\r")
#         sys.stdout.flush()
#         time.sleep(0.5)



# from __future__ import print_function
# import time,sys
# N = 1000
# for i in range(N):
#     
#     #print("进度:{0}%".format(round((i + 1) * 100 / N)),end='\r')
#     print("\r进度:{0}%".format(round((i + 1) * 100 / N)),end='')
#     #sys.stdout.write("进度:{0}%".format(round((i + 1) * 100 / N))
#     time.sleep(0.01)


import time
import progressbar
p = progressbar.ProgressBar(widgets=[])
N = 1000
for i in p(range(N)):
    time.sleep(0.01)

