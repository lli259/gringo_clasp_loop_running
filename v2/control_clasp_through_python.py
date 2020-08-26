import os
import commands
import time
code1='clasp1.py'
code2='clasp2.py'
code3='clasp3.py'

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
	valid=[ i for i in pids if not 'grep' in i]
	if len(valid)==0:
		return 0
	else:
		return 1

#result=checkpid('print_loop1.py')
#print(result)
#exit()

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
	pause_cmd='kill -STOP '+pid_list[ind]
	print pause_cmd
	os.system(pause_cmd)

print 'pids:',pid_list


#time pass is given to first process
t_pass_now=0
time_stamp=100
##########the python is pause, but clasp still running.
time.sleep(time_stamp)
exit()
###after 100 seconds all clasp done. even if python is paused.

while True:	
	#check finish
	process_status=[checkpid(p) for p in codes]
	process_sum=sum(process_status)
	print 'process_status:',process_status
	if process_sum==len(codes):
		#run it
		print 'now running', pid_list[t_pass_now]
		run_pass(t_pass_now,pid_list)
		#after time_stamp, start again with t_pass +1
		time.sleep(time_stamp)
		t_pass_now+=1
		if t_pass_now==len(codes):
			t_pass_now=0

	#when one finish
	else:
		'some one finish'
		break

print process_status
for ind,status in enumerate(process_status):
	if status==1:
		os.system('kill -9 '+pid_list[ind])



		
