Note:

_standard_templates symlink to ../../custom_components/ui_lovelace_minimalist/__ui_minimalist__/ulm_templates/. 
  This only works because we've patched https://github.com/home-assistant/core/blob/master/homeassistant/util/yaml/loader.py#L260
  to include followlinks=True

  I should submit this to fix this old issue (https://github.com/home-assistant/core/issues/15778).

It's underscored so it gets loaded first.

The other directories here are all custom, but copy the file structure of the standard templates for organization.

Because they are loaded later they will override any standard templates.

