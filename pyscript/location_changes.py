NOTIFICATION_TARGET = "mobile_app_will_s_iphone_14_pro"

# @state_trigger("sensor.wills_iphone_ble")
# def alert_on_sensor_location(trigger_type=None, var_name=None, value=None, old_value=None):
#   log.info(f"BLE: {trigger_type} ({var_name}): {old_value} => {value}")
#   service.call(
#     "notify",
#     NOTIFICATION_TARGET,
#     title=f"iPhone is in {value} ({value.distance}m)",
#     message=f"{var_name} was {old_value}",
#   )
  