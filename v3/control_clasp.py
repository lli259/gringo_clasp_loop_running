import os
import commands
import time
import sys
problemsize=sys.argv[1]

code1='enc_schur_original_xy.lp'
code2='enc_schur_original_xynum.lp'
code3='enc_schur_xy_mt.lp'

codes=[code1,code2,code3]
gringo_pid_list=['9999' for i in codes]
clasp_pid_list=['9999' for i in codes]
round_list=[0 for i in codes]
#get pid


def get_gringo_clasp_pid(cmd_g_c):
	pids=commands.getoutput('ps -ef | grep ./'+cmd_g_c).split('\n')
	#print(pids)
	valid_id=[ i for i in pids if not 'grep' in i]

	ret=[]
	for i in valid_id:
		result=i.split(' ')
		for j in result[1:]:
			if j!='':
				ret.append(j)
				break

	return ret

'''
#test all current ./gringo and ./clasp process_ids
all_gringo_pid=get_gringo_clasp_pid('gringo')
print all_gringo_pid
all_gringo_pid=get_gringo_clasp_pid('clasp')
print all_gringo_pid
exit()
'''
#run one encoding's gringo(if exists) and clasp(if exists) and stop other encodings'
def run_pass(pid_index):
	my_gringo_pid=gringo_pid_list[pid_index]
	my_clasp_pid=clasp_pid_list[pid_index]

	all_gringo_pid=get_gringo_clasp_pid('gringo')
	all_clasp_pid=get_gringo_clasp_pid('clasp')

	
	
	for p in gringo_pid_list:
		if p in all_gringo_pid:
			os.system('kill -STOP '+p)
	for p in clasp_pid_list:
		if p in all_clasp_pid:
			os.system('kill -STOP '+p)

	if my_gringo_pid in all_gringo_pid:
		os.system('kill -CONT '+my_gringo_pid)
	if my_clasp_pid in all_clasp_pid:
		os.system('kill -CONT '+my_clasp_pid)
	last_open_time=time.time()

#run its gringo+clasp cmds, record new gringo and clasp process,and stop them
def run_stop_save_pid(encoding_index):
	print encoding_index
	#old_pid
	old_gringo_pid=get_gringo_clasp_pid('gringo')
	old_clasp_pid=get_gringo_clasp_pid('clasp')
	#print 'old:',old_gringo_pid,old_clasp_pid
	#run new
	cmd='./gringo encodings2/'+codes[encoding_index]+ ' -c n='+problemsize+' |./clasp'
	print 'cmd:',cmd
	os.system(cmd+" &")
	#new_pid
	new_gringo_pid=get_gringo_clasp_pid('gringo')
	new_clasp_pid=get_gringo_clasp_pid('clasp')
	#print 'new:',new_gringo_pid,new_clasp_pid
	#get this pid
	this_gringo_pid=[i for i in new_gringo_pid if i not in old_gringo_pid][0]
	this_clasp_pid=[i for i in new_clasp_pid if i not in old_clasp_pid][0]
	print "this", this_gringo_pid,this_clasp_pid
	#save
	gringo_pid_list[encoding_index]=this_gringo_pid
	clasp_pid_list[encoding_index]=this_clasp_pid

	#pause
	pause_cmd='kill -STOP '+this_gringo_pid
	print 'Stopping',this_gringo_pid
	os.system(pause_cmd)
	pause_cmd='kill -STOP '+this_clasp_pid
	print 'Stopping',this_clasp_pid
	os.system(pause_cmd)

start_time=time.time()
#run, record and stop
for index in range(len(codes)):
	run_stop_save_pid(index)

initial_time=time.time()
print '\n'
print 'Initialization Finished!'
print 'Gringo and Clasp Process_ids:',gringo_pid_list,clasp_pid_list
print '\n'

#time pass is first given to first process
t_pass_now=0
round_now=0
time_stamp=20

print 'Problem size',problemsize
print 'Encodings',codes
print 'Start running...Each ',time_stamp,'s\n'
while True:	
	#clasp finish check
	all_clasp_pid=get_gringo_clasp_pid('clasp')
	clasp_status=[i in all_clasp_pid for i in clasp_pid_list]
	print 'Current clasp status:',clasp_status
	#if no one finishs:
	if sum(clasp_status)==len(codes):
		#run one encoding, and stop others
		round_now+=1
		print "Round ",round_now,'.Now running', t_pass_now
		run_pass(t_pass_now)
		round_list[t_pass_now]+=1
		#after time_stamp, start again with t_pass +1
		time.sleep(time_stamp)
		t_pass_now+=1
		if t_pass_now==len(codes):
			t_pass_now=0

	#when one finish,check which one
	else:
		for ind,status in enumerate(clasp_status):
			if not status:
				print ind,'solves it in',round_list[ind],' rounds.'
		break


#kill all gringo left
all_gringo_pid=get_gringo_clasp_pid('gringo')
gringo_status=[i in all_gringo_pid for i in gringo_pid_list]
print 'All running gringo',all_gringo_pid,'my gringo status',gringo_status


for ind,status in enumerate(gringo_status):
	if status:
		print 'Killing running gringo',gringo_pid_list[ind]
		os.system('kill -9 '+gringo_pid_list[ind])

#kill all clasp left
all_clasp_pid=get_gringo_clasp_pid('clasp')
clasp_status=[i in all_clasp_pid for i in clasp_pid_list]
print 'All running clasp', all_clasp_pid,'my clasp status',clasp_status
print 'Killing running clasp'
for ind,status in enumerate(clasp_status):
	if status:
		print 'Killing running gringo',clasp_pid_list[ind]
		os.system('kill -9 '+clasp_pid_list[ind])

print 'All running gringo and clasp killed.'
stop_time=time.time()
print 'All running time', round(stop_time-start_time,3)
print 'Initial time', round(initial_time-start_time,3)
print 'Solving time', round(stop_time-initial_time,3)
		
