from numpy import loadtxt, mean, array
from sys import argv

CALLS_FILE = argv[1]  									# path to input file => {time} {floor} {dest} on each line
OUT_FILE = argv[2]										# path to output file
GOTO_TEMP = "TIME {:.2f}\tGOTO FLOOR {}"				# GOTO action template string
STAT_TEMP = "AVERAGE {} TIME: {}"
OUT_TEMP = "[START FLOOR {}]\n{}\n[END FLOOR {}]"
INITIAL_POS = 1											# elevator starts on floor 1
MOVE_SPEED = 1											# 1 floor/second

dtype = [('time', 'f'), ('floor', 'i'), ('dest', 'i')]  # "f" is for float, "i" is for integer
calls = loadtxt(fname=CALLS_FILE, dtype=dtype)  		# [(time1, floor1, dest1), (time2, floor2, dest2), ...]
calls = sorted(calls, key=lambda x: x[0])  				# sort calls by time

actions = []				# list to log elevator actions
wait_time = []				# array of pickup time_delta values
inside_time = []			# array of dropoff time_delta values
elapsed_time = calls[0][0]	# the time of the very first call
elevator = {
	'pos': INITIAL_POS
}

def goto(floor, pickup=True):
	global elapsed_time, wait_time, inside_time
	current_pos = elevator['pos']
	time_delta = abs(floor - current_pos) / MOVE_SPEED  			# time needed to move from current_pos to floor

	if pickup:														# log time_delta in appropriate time_delta_list (wait_time/inside_time)
		wait_time.append( time_delta )
	else:  															# if not pickup, must be dropoff
		inside_time.append( time_delta )
	
	actions.append( GOTO_TEMP.format(elapsed_time, floor) )			# log the action to be performed
	elapsed_time += time_delta										# "wait until elevator arrives at floor"
	elevator['pos'] = floor											# update elevator position

	time_delta = 30 if floor == 1 else 5							# time needed to pick up or drop off riders
	elapsed_time += time_delta

# sequentially perform pick ups and drop offs
for time, pos, dest in calls:
	goto( pos )														# goto, then pick up at pos
	goto( dest, pickup=False )										# goto, then drop off at dest

# write elevator action time series to stdout
s = OUT_TEMP.format(
	INITIAL_POS, "\n".join(act for act in actions), elevator['pos']
)
with open(OUT_FILE, 'w') as f:
	f.write(s)

# compute stats
wait_time, inside_time = array(wait_time), array(inside_time)
total_time = wait_time + inside_time
data = [ ('WAIT', wait_time), ('INSIDE', inside_time), ('TOTAL', total_time) ]
for time_type, time_delta_array in data:
	mean_value = mean(time_delta_array)
	print( STAT_TEMP.format(time_type, mean_value) )