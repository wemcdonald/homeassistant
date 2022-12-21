app_config = None
config = None
registered_triggers = []

def _master_switch(common, name):
  app = common.SubApp(name)

  # Turn off lights
  master_expressions = []
  for master in app.entities['masters']:
    master_expressions.append(f"{master} == 'off'")

  @state_trigger(" or ".join(master_expressions))
  def light_turned_off(trigger_type=None, var_name=None, value=None):
    task.unique(f"master_switch_off_{name}")

    for area_id in app.entities.get('slave_areas', []):
      turn_off_light(area_id=area_id)
    for device_id in app.entities.get('slave_devices', []):
      turn_off_light(device_id=device_id)
    for entity_id in app.entities.get('slave_entities', []):
      turn_off_light(entity_id=entity_id)
  app.register(light_turned_off)

  # Turn on lights
  master_expressions = []
  for master in app.entities['masters']:
    master_expressions.append(f"{master} == 'on'")

  @state_trigger(" or ".join(master_expressions))
  def light_turned_on(trigger_type=None, var_name=None, value=None):
    task.unique(f"master_switch_on_{name}")

    for area_id in app.entities.get('slave_areas', []):
      turn_on_light(area_id=area_id)
    for device_id in app.entities.get('slave_devices', []):
      turn_on_light(device_id=device_id)
    for entity_id in app.entities.get('slave_entities', []):
      turn_on_light(entity_id=entity_id)

  app.register(light_turned_on)

class SubApp:
  def __init__(self, name):
    self.full_config = config
    self.app_config = app_config
    self.name = name.replace('willflix.', '')
    self.config = app_config.get(self.name, {})
    self.entities = self.config.get('entities')

  def register(self, trigger):
    registered_triggers.append(trigger)

  def debug(self, msg):
    log.debug(msg.replace("\n", f"\n[Willflix][{self.name}]: "))
  def info(self, msg):
    log.info(msg.replace("\n", f"\n[Willflix][{self.name}]: "))
  def warn(self, msg):
    log.warn(msg.replace("\n", f"\n[Willflix][{self.name}]: "))
  def error(self, msg):
    log.error(msg.replace("\n", f"\n[Willflix][{self.name}]: "))

  
  def turn_on_light(self, area_id=None, device_id=None, entity_id=None, brightness=None):
    self.info(f"Turning on light: area={area_id}")
    if brightness is None:
      brightness = 254
    light.turn_on(area_id=area_id, device_id=device_id, entity_id=entity_id, brightness=brightness)

  def turn_off_light(self, area_id=None, device_id=None, entity_id=None):
    self.info(f"Turning off light: area={area_id}")
    light.turn_off(area_id=area_id, device_id=device_id, entity_id=entity_id)
  
  def human_notify(self, title, message):
    people = self.config.get('notify')
    if people == None:
      people = self.app_config['common']['default_notify']

    for person in people:
      person = self.app_config['common']['notify_entities'].get(person, person)
      self.info(f"\n\n    TO: {person}")
      self.info(f"TITLE: {title}")
      self.info(f" BODY: {message}")
      service.call("notify", person, title=title, message=message)


class Scene(SubApp):
  def __init__(self, name, scene_conf):
    # TODO: Figure out why super() wasn't working
    self.full_config = config
    self.app_config = app_config
    self.name = name.replace('willflix.', '')
    self.config = app_config.get(self.name, {})
    self.entities = self.config.get('entities')

    self.scene_conf = scene_conf

  def run_scene(self):
    # Turn things on
    for area_id in self.scene_conf.get('turn_on', {}).get('areas', []) or []:
      self.turn_on_light(area_id=area_id)
    for entity_id in self.scene_conf.get('turn_on', {}).get('entities', []) or []:
      self.turn_on_light(entity_id=entity_id)

    # Turn things off
    for area_id in self.scene_conf.get('turn_off', {}).get('areas', []) or []:
      self.turn_off_light(area_id=area_id)
    for entity_id in self.scene_conf.get('turn_off', {}).get('entities', []) or []:
      self.turn_off_light(entity_id=entity_id)

    # Dim things
    for entity_id, percent in self.scene_conf.get('dim', {}).get('entities', {}) or {}:
      brightness = int(percent/100.0 * 255)
      self.turn_on_light(entity_id=entity_id, brightness=brightness)
