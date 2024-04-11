# Based on 04_thp_sensor.py and 05_thp_node.py
# Try to find the current altitude (in meter) based on the following formula
# Altitude(m) = 44330 * (1 - (current_pressure / seaLevelPressure)^(1/5.255))
# the current seaLevelPressure can be found at https://www.hko.gov.hk/en/wxinfo/ts/index_pre.htm