import time
if __name__ == '__main__':
  print('Test Start:\n')
  time1 = time.time()
  time2 = time.localtime(time1)
  time3 = time.asctime(time2)
  print(time1 + '\n' + time2 + '\n' + time3)
  
