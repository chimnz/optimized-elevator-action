from numpy import loadtxt
from sys import argv

CALLS_FILE = argv[1]  									# path to input file => {time} {floor} {dest} on each line
GOTO_TEMP = "TIME {:.2f}\tGOTO FLOOR {}"				# GOTO action template string
INITIAL_POS = 1											# elevator starts on floor 1
MOVE_SPEED = 1											# 1 floor/second

dtype = [('time', 'f'), ('floor', 'i'), ('dest', 'i')]  # "f" is for float, "i" is for integer
calls = loadtxt(fname=CALLS_FILE, dtype=dtype)  		# [(time1, floor1, dest1), (time2, floor2, dest2), ...]
calls = sorted(calls, key=lambda x: x[0])  				# sort calls by time

actions = []				# list to log elevator actions
elapsed_time = calls[0][0]	# the time of the very first call
elevator = {
	'pos': INITIAL_POS
}

def goto(floor):
	global elapsed_time
	current_pos = elevator['pos']
	time_delta = abs(floor - current_pos) / MOVE_SPEED  			# time needed to move from current_pos to floor
	
	actions.append( GOTO_TEMP.format(elapsed_time, floor) )			# log the action to be performed
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
for time, pos, dest in calls:
	pickup( pos )
	dropoff( dest )

# write elevator action time series to stdout
print( "[START FLOOR {}]".format(INITIAL_POS) )
for act in actions:
	print(act)
print( "[END FLOOR {}]".format(elevator['pos']) )