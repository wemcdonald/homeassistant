def _alert_on_warm_fridge(common):
  app = common.SubApp(__name__)
  @service()
  @state_trigger(
    app.entities['sensor'],
    f"float({app.entities['sensor']}) > {app.config['max_temp_f']}",
    state_hold=(app.config['hold_minutes'] * 60),
  )
  def alert_on_warm_fridge(value=None):
    title = f"🌡️ The fridge is {value}°"
    message = f"It's been > {app.config['max_temp_f']}º for {app.config['hold_minutes']} minutes."
    app.human_notify(title, message)
  app.register(alert_on_warm_fridge)
