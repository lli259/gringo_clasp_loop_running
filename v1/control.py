import os
import commands
import time
code1='print_loop.py'
code2='print_loop1.py'
code3='print_loop2.py'

codes=[code1,code2,code3]
pid_list=['9999' for i in codes]

#get pid
def getpid(code_t):
	pids=commands.getoutput('ps -ef |grep \'python '+code_t+'\'').split('\n')
	#print(pids)
	result=pids[0].split(' ')
	for i in result[1:]:
		if i!='':
			return(i)

#check if anyone finishs
def checkpid(code_t):
	pids=commands.getoutput('ps -ef |grep \'python '+code_t+'\'').split('\n')
	#print(pids)
	result=pids[0].split(' ')
	if len(result)==1:
		return 0
	else:
		return 1

def run_pass(pid,allpids):
	for p in allpids:
		os.system('kill -STOP '+p)
	os.system('kill -CONT '+allpids[pid])


#run and pause
for ind,codet in enumerate(codes):
	#run
	os.system('python '+codet+" &")
	#save pid
	pid_list[ind]=getpid(codet)
	#pause
	os.system('kill -STOP '+pid_list[ind])


#time pass is given to first process
t_pass_now=0
time_stamp=20






while True:	
	#check finish
	process_sum=sum([checkpid(p) for p in codes])
	if process_sum==len(codes):
		#run it
		run_pass(t_pass_now,pid_list)
		#after time_stamp, start again with t_pass +1
		time.sleep(time_stamp)
		t_pass_now+=1
		if t_pass_now==len(codes):
			t_pass_now=0

	#when one finish
	else:
		break

for ind,status in enumerate(process_sum):
	if status==1:
		os.system('kill -9 '+pid_list[ind])



		
