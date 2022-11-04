WAKE_UP_SECONDS = 15

def _alert_on_low_battery(common):
  app = common.SubApp(__name__)
  battery = state.get(app.entities['battery'])
  wake_up = state.get(app.entities['wake_up'])
  charger = state.get(app.entities['charger'])

  for time in app.config.get('times', []):
    @service()
    @time_trigger(time)
    def alert_on_low_battery():
      if not battery.isnumeric():
        app.info(f"Waking up Tesla because battery status was {battery}")  
        wake_up.press()
        task.sleep(WAKE_UP_SECONDS)

      percent = int(battery)
      unplugged = charger != 'on'

      app.info(f"Tesla at {percent}% and unplugged: {unplugged}")  

      if percent < app.config['standard_threshold_percent'] and unplugged:
        app.human_notify(title="Charge the Tesla!", message=f"It's at {percent}%")

    app.register(alert_on_low_battery)
