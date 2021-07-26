import math

def reward_function(params):
	'''
	Example that penalizes steering, which helps mitigate zig-zag behaviors
	'''

	# Calculate 4 marks that are farther and father away from the center line
	marker_1 = 0.1 * params['track_width']
	marker_2 = 0.2 * params['track_width']
	marker_3 = 0.3 * params['track_width']
	marker_4 = 0.4 * params['track_width']
	distance_from_center = params['distance_from_center']
	steering_angle = params['steering_angle']
	all_wheels_on_track = params['all_wheels_on_track']
	speed = params['speed']
	track_width = params['track_width']
	objects_distance = params['objects_distance']
	_, next_object_index = params['closest_objects']
	objects_left_of_center = params['objects_left_of_center']
	is_left_of_center = params['is_left_of_center']
	heading = params['heading']
	waypoints = params['waypoints']
	closest_waypoints = params['closest_waypoints']

	# Initialize reward with a small number but not zero
	# because zero means off-track or crashed
	reward = 1e-3
	
	# Reward if the agent stays inside the two borders of the track
	if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
		reward_lane = 1.0
	else:
		reward_lane = 1e-3
	
    	# Set dynamic thresholds based on distance_from_center
	# Give higher reward if the car is closer to center line and vice versa
	# Steering penality threshold, change the number based on your action space setting
	# Set the speed threshold based your action space
	if distance_from_center <= marker_2:
		reward_lane *= 1.0
		ABS_STEERING_THRESHOLD = 20
		SPEED_THRESHOLD = 2.0
	elif distance_from_center <= marker_3:
		reward_lane *= 0.9
		ABS_STEERING_THRESHOLD = 40
		SPEED_THRESHOLD = 1.0
	elif distance_from_center <= marker_4:
		reward_lane *= 0.8
		ABS_STEERING_THRESHOLD = 60		
		SPEED_THRESHOLD = 0.5
	else:
		reward_lane *= 0.7
		ABS_STEERING_THRESHOLD = 90
		SPEED_THRESHOLD = 0.1
		
	reward_heading = 1.0
	
	# Calculate the direction of the center line based on the closest waypoints
	next_point = waypoints[closest_waypoints[1]]
	prev_point = waypoints[closest_waypoints[0]]

	# Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
	track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
	# Convert to degree
	track_direction = math.degrees(track_direction)

	# Calculate the difference between the track direction and the heading direction of the car
	direction_diff = abs(track_direction - heading)
	if direction_diff > 180:
		direction_diff = 360 - direction_diff

	# Penalize the reward if the difference is too large
	DIRECTION_THRESHOLD = 10.0
	if direction_diff > DIRECTION_THRESHOLD:
		reward_heading *= 0.5
		SPEED_THRESHOLD = 90
		

	# Penalize reward if the car is steering too much
	if abs(steering_angle) > ABS_STEERING_THRESHOLD:
		reward_heading *= 0.5

	reward_speed = 1.0
	
	if speed < SPEED_THRESHOLD:  # Penalize if the car goes too slow
	    reward_speed *= 0.5
	else:  # High reward if the car stays on track and goes fast
	    reward_speed *= 1.0
	
	# Penalize if the agent is too close to the next object
	reward_avoid = 1.0
	    
	# Distance to the next object
	distance_closest_object = objects_distance[next_object_index]
	# Decide if the agent and the next object is on the same lane
	is_same_lane = objects_left_of_center[next_object_index] == is_left_of_center

	if is_same_lane:
		if 0.5 <= distance_closest_object < 0.8: 
		    reward_avoid *= 0.5
		elif 0.3 <= distance_closest_object < 0.5:
		    reward_avoid *= 0.2
		elif distance_closest_object < 0.3:
		    reward_avoid = 1e-3 # Likely crashed

	# Calculate reward by putting different weights on 
	# the two aspects above
	reward += 1.0 * reward_lane + 4.0 * reward_avoid + 1.0 * reward_heading + 0.5 * reward_speed

	# give a reward at each time of the completing a lap
	if params['progress'] == 100 :
	    reward += 10000

	return float(reward)
