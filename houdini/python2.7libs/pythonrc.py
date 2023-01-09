import os

import context
import hou

msg = '\nSourcing OpenVFX Houdini Toolkit\n'
msg += 'Package Location: {}\n'.format(os.getenv('OVFX_CONFIG_DIR'))
print(msg)


def update_context(event_type):
    if event_type in (hou.hipFileEventType.AfterClear, hou.hipFileEventType.AfterLoad, hou.hipFileEventType.BeforeSave):
        tmp_scene = hou.hipFile.name()
        # As opposed to a AfterLoad event, the AfterClear event doesn't rename the scene to what
        # it's going to be when the event is finished executing. We have to force a rename.
        if event_type == hou.hipFileEventType.AfterClear:
            hou.hipFile.setName('untitled.hip') # Setting the hip name manually
        context.source_context_scripts()
        hou.hipFile.setName(tmp_scene) # Reverting to the original name so a later event AfterLoad would not be untitled

hou.hipFile.addEventCallback(update_context)
