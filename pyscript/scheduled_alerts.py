NOTIFICATION_TARGET = "mobile_app_will_s_iphone_14_pro"

### Sunset
# Alert me if we've left the door open after sunset
# TODO: Check weather forecast
PORCH_LEFT_OPEN_TIME = 10 * 60
PORCH_ENTITY = "binary_sensor.porch_door_contact"
@time_trigger("once(sunset)")
@service()
def check_porch_door():
  if state.get(PORCH_ENTITY) == "on":
    trig_info = task.wait_until(
        state_trigger="binary_sensor.porch_door_contact == 'off'",
        timeout=PORCH_LEFT_OPEN_TIME
      )
    if trig_info["trigger_type"] == "timeout":
      service.call(
        "notify",
        NOTIFICATION_TARGET,
        title="Close the porch door",
        message="It's cold out there!",
      )
    

# 8pm
# Alert me if I've left my bike unplugged
BIKE_CHARGER_POWER = "sensor.bike_charger_current_power"
@time_trigger("once(20:00)")
def check_bike_plug():
  power = state.get(BIKE_CHARGER_POWER)
  isPlugged = False
  try:
    isPlugged = float(power) > 0.1
  except ValueError:
    pass

  if not isPlugged:
    service.call(
        "notify",
        NOTIFICATION_TARGET,
        title="Check bike",
        message="Bike isn't plugged in",
      )

