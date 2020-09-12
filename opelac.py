import numpy as np
from sys import argv

actions = []		# list to log elevator actions
elevator = {
	'pos': 1		# elevator starts on floor 1
}
move_speed = 1		# 1 floor/second
elapsed_time = 0.0

GOTO_TEMP = "TIME {}\tGOTO FLOOR {}"	# GOTO action string template
INITIAL_POS = elevator['pos']

def read_calls():	
	CALLS_FILE = argv[1]  									# path to input file => {time} {floor} {dest} on each line
	dtype = [('time', 'f'), ('floor', 'i'), ('dest', 'i')]  # "f" is for float, "i" is for integer
	calls = np.loadtxt(fname=CALLS_FILE, dtype=dtype)  		# [(time1, floor1, dest1), (time2, floor2, dest2), ...]
	return sorted(calls, key=lambda x: x[0])  				# sort calls by time

def goto(floor):
	global elapsed_time
	current_pos = elevator['pos']
	time_delta = abs(floor - current_pos) / move_speed  			# time needed to move from current_pos to floor
	
	actions.append( GOTO_TEMP.format(elapsed_time, floor) )			# log the action to be performed action
	elapsed_time += time_delta										# "wait until elevator arrives at floor"
	elevator['pos'] = floor											# update elevator position

def pickup(floor):
	global elapsed_time
	goto(floor)
	time_delta = 30 if floor == 1 else 5							# time needed to pick up riders

	elapsed_time += time_delta										# "wait until finished loading passengers"

def dropoff(floor):
	pickup(floor)													# in this simplified system, picking up is the same as dropping off

# sequentially perform pick ups and drop offs
for time, pos, dest in read_calls():
	pickup( pos )
	dropoff( dest )

# write elevator action time series to stdout
print( "[START FLOOR {}]".format(INITIAL_POS) )
for act in actions:
	print(act)
print( "[END FLOOR {}]".format(elevator['pos']) )