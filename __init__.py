# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "iSar Tools",
    "author": "iSar",
    "version": (0, 1, 5),
    "blender": (2, 7, 3),
    "location": "object",
    "description": "architecture workflow",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "https://github.com/i5ar/itools/",
    "category": "Object"}

import bpy
import addon_utils
from bpy.props import BoolProperty, FloatVectorProperty
from .creator import iOrthoCam, iWipe, iPoint, iAddon, iGeometry
from .bound import iBoundingBox, iBoundingBoxWindow, iHole
from .snap import iCreateOrientation, iPivotToSelected, iSelectionToCursor
from .console import iConsole
from .separator import iSeparate
from .intersect import iNtersect
from .roof import iRoof

isar_ascii_logo = '''\

              ::::::::  ::::::::        :::::::::
           :::::::::::  :::::::::::   :::::::::::
          ::::                  :::: ::::
          :::                    ::: :::
          :+++:                :+++: :+:
            :+++:            :+++:   :+:
 +#+          +###+        +###+     +#+
 +#+            +###+    +###+   #+  +#+
 ###              +##+  +##+     ##+ ###
 ###              +###  ###+     ### ###
 +###+           +###+  +###+  +###+ ###
   ##################    #########   ###
     ##############        #####     ###
'''

isar_str_classes = [ 'iSarPanel', 'iSwitchLanguage', 'iLanguage', 'iBoundingBox',
                     'iLink', 'iOrthoCam', 'iWipe', 'iConsole',
                     'iNtersect', 'iPoint', 'iGeometry', 'iPivotToSelected',
                     'iSeparate', 'iHole', 'iSelectionToCursor', 'iCreateOrientation',
                     'iBoundingBoxWindow', 'iAddon', 'iRoof' ]
isar_lang = {}
handle_lang = True

it_dict = [ 'Strumenti', 'Cambia Lingua:', 'Inglese', 'Circoscrivi',
            'Blender StackExchange', 'Appendi Camera', 'Pulisci Scena', 'Console',
            'Intersezione', 'Inserisci Punto', 'Elimina Doppioni & Centra Origine', 'Pivot alla Selezione',
            'Separa Tutto', 'Sottrai', 'Selezione al Cursore', 'Crea Orientazione alla Normale',
            'Aggiungi Finestra & Circoscrivi', 'Abilita Addon', 'Tegole da Superficie WIP' ]

en_dict = [ 'Toolset', 'Switch Language:', 'Italiano', 'Bounding Box Wire',
            'Blender StackExchange', 'Ortho Camera', 'Wipe scene', 'Console',
            'Intersect', 'Set Point', 'Remove Doubles & Center Origin', 'Pivot To Selected',
            'Separate All', 'Hole', 'Selection To Cursor', 'Create Normal Orientation',
            'Add Window & Bounding Box', 'Enable Addon', 'Roof Tile WIP' ]

bpy.types.Scene.nt_main_panel = BoolProperty(
    name="show main panel",
    description="",
    default = False)

def isar_make_lang(classes, names):
    dict = {}
    for i, c in enumerate(classes):
        dict[str(c)] = names[i]
    return dict

def get_lang(lang_dict):
    lang = lang_dict
    return lang

def isar_lang_panel():
    global handle_lang
    global isar_lang
    if handle_lang:
        isar_lang = get_lang(lang_dict_it)
        handle_lang = False
    else:
        isar_lang = get_lang(lang_dict_en)
        handle_lang = True

lang_dict_it = isar_make_lang(isar_str_classes, it_dict)
lang_dict_en = isar_make_lang(isar_str_classes, en_dict)
isar_lang_panel()

class iLanguage (bpy.types.Operator):
    """Language Switcher"""
    bl_idname = "object.isar_language"
    bl_label = "iSar English"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        isar_lang_panel()

        return {'FINISHED'}

class iSarPanel(bpy.types.Panel):
    """iSar Panel"""
    bl_idname = "panel.isar"
    bl_label = 'iSar Tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'iSar'            # Tools name
    bl_options = {'DEFAULT_CLOSED'} # Panel option
    def draw(self, context):
        global isar_lang
        layout = self.layout
        row = layout.row()
        row.label(text=isar_lang['iSwitchLanguage'])
        row.operator('object.isar_language', text=isar_lang['iLanguage'])
        col = layout.column(align=True)
        col.operator("object.isar_wipe", icon="WORLD", text=isar_lang['iWipe'])
        row = col.row(align=True)
        row.operator("object.isar_ortho_cam", icon="OUTLINER_OB_CAMERA", text=isar_lang['iOrthoCam'])
        row = col.row(align=True)
        row.operator('object.isar_point', icon="LAYER_USED", text=isar_lang['iPoint'])
        row = col.row(align=True)
        row.operator('object.isar_origin_geometry', icon="MESH_DATA", text=isar_lang['iGeometry'])
        #row = col.row(align=True)
        #row.operator("object.isar_hack", icon="VIEWZOOM", text=isar_lang['iAddon'])
        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("object.isar_bounding_boxers", icon="MESH_CUBE", text=isar_lang['iBoundingBox'])
        row.operator('object.isar_hole', icon="MOD_BOOLEAN", text=isar_lang['iHole'])
        row = col.row(align=True)
        row.operator("object.isar_window_bounding_boxers", icon="MOD_LATTICE", text=isar_lang['iBoundingBoxWindow'])
        row = col.row(align=True)
        row.operator("object.isar_tile", icon="MOD_BUILD", text=isar_lang['iRoof'])
        col = layout.column(align=True)
        col.operator('object.isar_create_orientation', icon="MANIPUL", text=isar_lang['iCreateOrientation'])
        row = col.row(align=True)
        row.operator("object.isar_origin_to_cursor", icon="CURSOR", text=isar_lang['iPivotToSelected'])
        row.operator("object.isar_selection_to_cursor", icon="ARROW_LEFTRIGHT", text=isar_lang['iSelectionToCursor'])
        row = layout.row(align=True)
        row.operator("object.isar_separate", icon="MOD_SOLIDIFY", text=isar_lang['iSeparate'])
        row.operator("object.isar_intersect", icon="MOD_BEVEL", text=isar_lang['iNtersect'])
        split = layout.split()
        col = split.column(align=False)
        col.operator("view.isar_console", icon="CONSOLE", text=isar_lang['iConsole'])
        split = layout.split()
        col = split.column(align=True)
        col.operator('wm.url_open', icon="LINK", text=isar_lang['iLink']).url = 'http://blender.stackexchange.com/'

isar_classes = [ iSarPanel, iLanguage, iBoundingBox, iWipe, iOrthoCam, iConsole, iNtersect, iPoint, iGeometry, iPivotToSelected, iSeparate, iHole, iSelectionToCursor, iCreateOrientation, iBoundingBoxWindow, iAddon, iRoof ]

def register():
    global handle_lang
    for isar_class in isar_classes:
        bpy.utils.register_class(isar_class)
    print(isar_ascii_logo)

def unregister():
    reversed_classes = reversed(isar_classes)
    for isar_class in reversed_classes:
        bpy.utils.unregister_class(isar_class)
    del reversed_classes

if __name__ == "__main__":
    register()
