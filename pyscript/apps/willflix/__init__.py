from . import common
from . import fridge
from . import tesla

common.app_config = pyscript.app_config
common.config = pyscript.config

fridge._alert_on_warm_fridge(common)
tesla._alert_on_low_battery(common)

# Auto-run any subapps by 'type'
for subapp_name, hash in common.app_config.items():
  type = hash.get('type')
  if type is not None:
    func = getattr(common, f"_{type}")
    func(common, subapp_name)

# for name, scene in common.config['scenes'].items():
#   app = common.Scene(name, scene)
#   @service(f"willflix.{app.name}")
#   def run_scene():
#     app.run_scene()
  
#   run_scene.__name__ = name
#   common.registered_triggers.append(run_scene)

@service()
def out_of_town():
  name = "out_of_town"
  app = common.Scene(name, common.config['scenes'][name])
  app.run_scene()

@service()
def garage_on():
  name = "garage_on"
  app = common.Scene(name, common.config['scenes'][name])
  app.run_scene()

@service()
def garage_off():
  name = "garage_off"
  app = common.Scene(name, common.config['scenes'][name])
  app.run_scene()

@service()
def bedtime():
  name = "bedtime"
  app = common.Scene(name, common.config['scenes'][name])
  app.run_scene()

@service()
def colin_sleep():
  name = "colin_sleep"
  app = common.Scene(name, common.config['scenes'][name])
  app.run_scene()

@service()
def story_time():
  name = "story_time"
  app = common.Scene(name, common.config['scenes'][name])
  app.run_scene()

@service()
def sleep():
  name = "sleep"
  app = common.Scene(name, common.config['scenes'][name])
  app.run_scene()

@service()
def morning():
  name = "morning"
  app = common.Scene(name, common.config['scenes'][name])
  app.run_scene()
