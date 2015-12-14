from drone_simulation import DroneSimulation
import random, numpy

def estimate_distance(spl):
	reference_distance = 12.5
	reference_spl = 100
	return reference_distance * 10**(0.05*(reference_spl - spl))

def estimate_direction(drone):
	p1 = drone.get_sound_pressure_level()
	drone.move_forward(25)
	p2 = drone.get_sound_pressure_level()
	drone.move_backward(25)
	drone.move_right(25)
	p3 = drone.get_sound_pressure_level()
	drone.move_left(25)

	d1 = estimate_distance(p1)
	d2 = estimate_distance(p2)
	d3 = estimate_distance(p3)

	forward = d2 - d1
	right = d3 - d1
		
	return (forward, 0, right)

if __name__ == '__main__':
	rnd = [ random.randint(0, 150) for x in range(3) ]
	drone = DroneSimulation(
			random.randint(0, 100), 100, random.randint(0, 100), 
			random.randint(0, 359))

	direction_vector = estimate_direction(drone)
	drone.rotate_to_vector(direction_vector)
	
	distance = estimate_distance(drone.get_sound_pressure_level())
	diff = -1
	while diff < 0:
		drone.move_forward(5) 
		new_distance = estimate_distance(drone.get_sound_pressure_level())
		diff = new_distance - distance
		distance = new_distance

	drone.move_backward(8)
	drone.land()
