import time
if __name__ == '__main__':
  print('Test Start:\n')
  time1 = time.time()
  time2 = time.localtime(time1)
  time3 = time.asctime(time2)
  print('{}{}{}'.format(time1, time2, time3))
  
