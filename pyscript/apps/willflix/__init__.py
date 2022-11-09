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

for name, scene in common.config['scenes'].items():
  common.Scene(name, scene)