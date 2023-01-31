def generate_zones(rows, columns):
	final = []
	zone_height = round((1 / rows), 3)
	zone_width = round((1 / columns), 3)
	#format for zone coordinates is top left, top right, bottom right, bottom left
	for col in range(columns):
		for row in range(rows):
			zone = []
			zone.append([col * zone_width, row * zone_height])
			zone.append([(col + 1) * zone_width, row * zone_height])
			zone.append([(col + 1) * zone_width, (row + 1) * zone_height])
			zone.append([col * zone_width, (row + 1) * zone_height])
			final.append(zone)
	return final