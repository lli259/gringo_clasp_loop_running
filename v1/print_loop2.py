import time
i=0
print(i)
for j in range(60):
    time.sleep(1)
    i+=1
    if i%10==0:
        print('loop2',i)
