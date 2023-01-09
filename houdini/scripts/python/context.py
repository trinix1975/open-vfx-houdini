import collections
import copy
import os
import re
import sys
import traceback
import yaml

import hou

import ovfx # For access in callback functions inside source_context_scripts exec() scripts
import ovfx.loc
import ovfx.cfg
from ovfx import exceptions as ex


def source_context_scripts():
    """
    Call the context common.py script and other tools script in the same folder

    Since these are called as an exec, the current locals() namespace is available.
    This allows any local variable declared here to be accessed directly from those scripts.
    """

    if not hasattr(hou, 'ovfx'):
        hou.ovfx = {}
    hou.ovfx['rop'] = {}
    hou.ovfx['loc'] = {} # Get rid of all potential conflicting previous locations

    # Detect if we are in a different context
    is_new_context = True
    if 'previous_scene' in hou.ovfx:
        if hou.hipFile.path() == hou.ovfx['previous_scene']:
            is_new_context = False

    # Initialize the empty default location context.
    # This will be considered invalid because no real path should match the dummy tags
    hou.ovfx['loc']['scene'] = ovfx.loc.Location('/<some>/<dummy>/<folder>/<that>/<does>/<not>/<exist>')

    # Initialize the context based on the scene name
    if hou.hipFile.basename() != 'untitled.hip':
        # Loop through the different scene types (context types) from the configuration
        # and extract the context from the first one it finds that is a match
        loc = ovfx.cfg.location

        # Scene types list in the yaml configuration file
        scene_types = loc['ovfx']['software']['houdini']['scene_types']
        matched_context = False # To keep track whether we have found a context model that matches the current hip file
        for scene_type in scene_types:
            if not matched_context: # Keep trying as long as a valid context hasn't been found
                hou.ovfx['loc']['scene'] = ovfx.loc.Location(['ovfx', 'software', 'houdini', 'scene_types', scene_type])
                hou.ovfx['loc']['scene'].extract_frags(hou.hipFile.path(), expand=True)
                if hou.ovfx['loc']['scene'].valid():
                    matched_context = True

        # hou.ovfx['loc']['scene'].extract_frags(hou.hipFile.path())
        if is_new_context: # Don't show the info when we're simply saving on top of itself
            print(hou.ovfx['loc']['scene'].info(include_empty=False))

    # Loop through all files in the context folder and source them
    context_config_folder = '{}/houdini/utility'.format(os.getenv('OVFX_CONFIG_DIR'))
    for path in os.listdir(context_config_folder):
        # if os.path.basename(path) != 'common.py' and path[-3:] == '.py':
        if path[-3:] == '.py':
            path = '{dir}/{file}'.format(dir=context_config_folder, file=path)
            with open(path) as f:
                data = f.read()
            try:
                exec(data)
            except Exception as e:
                if not e.args:
                    e.args=('',)
                e.args = ('Script: {}'.format(path),) + e.args
                traceback.print_exc()

    hou.ovfx['previous_scene'] = hou.hipFile.path()
