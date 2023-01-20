def generate_zones(rows, columns):
	final = []
	zone_height = round(1 / columns, 3)
	zone_width = round(1 / rows, 3)
	#format for zone coordinates is top left, top right, bottom right, bottom left
	for row in range(rows):
		for col in range(columns):
			zone = []
			zone.append([row * zone_width, col * zone_height])
			zone.append([(row + 1) * zone_width, col * zone_height])
			zone.append([(row + 1) * zone_width, (col + 1) * zone_height])
			zone.append([row * zone_width, (col + 1) * zone_height])
			final.append(zone)
	return final