import time
starttime=time.time()
while True:
  print ("tick")
  time.sleep(60.0 - ((time.time() - starttime) % 60.0))