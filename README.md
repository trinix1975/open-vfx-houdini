# Open VFX Houdini

Foundation for tools that uses the Open VFX Framework within Houdini.

## Description

This package is used to extract the context from the scene hip file name. This happens when a scene is opened and saved. Utility scripts placed in a dedicated folder will also be executed after the context is updated.

By itself it does not do much more than that. However, all Houdini tools that need access to the context would need to run on top of this package to get that information. The tools developed for Houdini use the [utility script](#utility-scripts) mechanism to initialize or configure their features.


## Installing

### Prerequisites
Open VFX Houdini needs the Open VFX framework installed and configured.

### Houdini Packages
The easiest way to have it configure within Houdini is to use the Houdini packages mechanism. The Open VFX Houdini Rop project comes with a sample project that uses a package file.


## Utility Scripts
Utility scripts are scripts needed by different tools built on top of the Open VFX Houdini package.

Those scripts are executed every time a scene context changes. This happens when a scene is opened or saved to a different context. Starting a new scene will also set the context to invalid.

All python scripts found in the following folder will be executed when the conditions above are met.

> OVFX_CONFIG_DIR/houdini/utility

### Example
The Open VFX Houdini Rop nodes need to have their paths initialized every time a context change. Because each studio has its own folder structure, a custom script is required per studio for each custom node type.

>### Warning
>Because any utility script that is placed in the OVFX_CONFIG_DIR/houdini/utility will execute after the context has been set, it is very important to make the utility script folder and utility scripts in read access only.

## Accessing Context
The following Python ovfx.loc.Location instance is updated every time the scene is saved and opened.

    hou.ovfx['loc']['scene']
 
Refer to the Python of the class for more detailed information but this object gives information about the context valid state, which shot number, project name, version etc.

It also provides utility methods to translate from a path with tags <> to the full expanded path based on the current context.

## Examples
Refer to the samples folder in Open VFX Houdini Rop for a concrete usage of the Open VFX Houdini project.