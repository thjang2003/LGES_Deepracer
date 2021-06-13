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

    # Set dynamic thresholds based on distance_from_center
	# Give higher reward if the car is closer to center line and vice versa
	# Steering penality threshold, change the number based on your action space setting
	# Set the speed threshold based your action space
	if distance_from_center <= marker_1:
		reward = 1
		ABS_STEERING_THRESHOLD = 5
		SPEED_THRESHOLD = 2.0
	elif distance_from_center <= marker_2:
		reward = 0.7
		ABS_STEERING_THRESHOLD = 10
		SPEED_THRESHOLD = 1.0
	elif distance_from_center <= marker_3:
		reward = 0.5
		ABS_STEERING_THRESHOLD = 20
		SPEED_THRESHOLD = 0.5
	elif distance_from_center <= marker_4:
		reward = 0.1
		ABS_STEERING_THRESHOLD = 30
		SPEED_THRESHOLD = 0.5
	else:
		reward = 1e-3  # likely crashed/ close to off track
		ABS_STEERING_THRESHOLD = 40
		SPEED_THRESHOLD = 0.1


	# Penalize reward if the car is steering too much
	if abs(steering_angle) > ABS_STEERING_THRESHOLD:
		reward *= 0.5

	if not all_wheels_on_track: # Penalize if the car goes off track
	    reward *= 1e-3
	elif speed < SPEED_THRESHOLD:  # Penalize if the car goes too slow
	    reward *= 0.5
	else:  # High reward if the car stays on track and goes fast
	    reward *= 1.0
	    
	
	# give a reward at each time of the completing a lap
	if params['progress'] == 100 :
	    reward += 10000

	return float(reward)
