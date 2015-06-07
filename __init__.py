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
    "tracker_url": "https://github.com/i5ar/isar_tools/",
    "category": "Object"}

import bpy
import addon_utils
from bpy.props import BoolProperty, FloatVectorProperty
from .creator import iOrthoCam, iWipe
from .bound import iBoundingBox, iBoundingBoxWindow
from .snap import iCreateOrientation, iPivotToSelected, iSelectionToCursor
from .console import iConsole

isar_str_classes = [ 'iSarPanel', 'iSwitchLanguage', 'iLanguage', 'iBoundingBox',
                     'iLink', 'iOrthoCam', 'iWipe', 'iConsole',
                     'iNtersect', 'iPoint', 'iGeometry', 'iPivotToSelected',
                     'iSeparate', 'iHole', 'iSelectionToCursor', 'iCreateOrientation',
                     'iBoundingBoxWindow', 'iLine' ]
isar_lang = {}
handle_lang = True

it_dict = [ 'Strumenti', 'Cambia Lingua:', 'Inglese', 'Circoscrivi',
            'Blender StackExchange', 'Appendi Camera', 'Pulisci Scena', 'Console',
            'Intersezione', 'Inserisci Punto', 'Elimina Doppioni & Centra Origine', 'Pivot alla Selezione',
            'Separa Tutto', 'Sottrai', 'Selezione al Cursore', 'Crea Orientazione alla Normale',
            'Aggiungi Finestra & Circoscrivi', 'Traccia Linea' ]

en_dict = [ 'Toolset', 'Switch Language:', 'Italiano', 'Bounding Box Wire',
            'Blender StackExchange', 'Ortho Camera', 'Wipe scene', 'Console',
            'Intersect', 'Set Point', 'Remove Doubles & Center Origin', 'Pivot To Selected',
            'Separate All', 'Hole', 'Selection To Cursor', 'Create Normal Orientation',
            'Add Window & Bounding Box', 'Line' ]

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

class iLine (bpy.types.Operator):
    """Add Window & Bounding Box Mesh"""
    bl_idname = "object.isar_line"
    bl_label = "iSar Line"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Check enabled addon [10]
        # [10]: http://blender.stackexchange.com/questions/15638/how-to-distinguish-between-addon-is-not-installed-and-addon-is-not-enabled
        mod = None
        addon_name = "snap_utilities_lite"                      # File name without extension or folder name
        if addon_name not in addon_utils.addons_fake_modules:   # Addons in directory
            print("\"%s\" addon is not installed." % addon_name)
            addon_status = "\"%s\" addon is not installed. This method require " % addon_name
            self.report({'INFO'}, addon_status)
        else:
            default, state = addon_utils.check(addon_name)
            if not state:
                try:
                    mod = addon_utils.enable(addon_name, default_set=False, persistent=False)
                except:
                    print("Could not enable \"%s\" addon on the fly." % addon_name )
            if state:
                print("Good, \"%s\" was already enabled." % addon_name )
        if mod:
            addon_status = 'Addon enabled and running!'
            self.report({'INFO'}, addon_status)

        # TODO Hack the line
        self.report({'INFO'}, "Work in progress!")

        return {'FINISHED'}

class iNtersect(bpy.types.Operator):
    """Intersect & Split All"""
    bl_idname = "object.isar_intersect"
    bl_label = "iSar Intersect"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if len(context.selected_objects) == 0:
            return False
        return True

    snippet = bpy.props.StringProperty(name='intersect', default='')

    def execute(self, context):
        self.report({'INFO'}, self.main())
        return {'FINISHED'}
    # TODO Surfaces intersection
    def main(self):
        snippet = 'Work in Progress!'
        return snippet

class iPoint(bpy.types.Operator):
    """Set Point"""
    bl_idname = "object.isar_point"
    bl_label = "iSar Point"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Deselect everything to prevent Origin to Geometry of more objects
        bpy.ops.object.select_all(action='DESELECT')
        # Get Cursor location
        location = bpy.context.scene.cursor_location
        verts = [location]
        name = 'Point'
        # Create mesh and object
        me = bpy.data.meshes.new(name+'Mesh')
        ob = bpy.data.objects.new(name, me)
        ob.show_name = False
        # Link object to scene
        scn = bpy.context.scene
        scn.objects.link(ob)
        # Make object active
        scn.objects.active = ob
        ob.select = True
        # Fill in the data
        me.from_pydata(verts, [], [])
        # Update mesh with new data
        me.update()
        # Get first item coordinates
        coordinates = me.vertices[0].co
        print('Vertex: '+str(coordinates))
        # Origin to Geometry of current object
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        # Toggle in Edit Mode and active the Vertex Select Mode
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}

class iGeometry(bpy.types.Operator):
    """Remove Doubles & Origin to Geometry"""
    bl_idname = "object.isar_origin_geometry"
    bl_label = "Remove Doubles & Origin to Geometry"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if len(context.selected_objects) == 0:
            return False
        return True

    def execute(self, context):
        # Remove Doubles [7]
        # [7]: http://bit.ly/1C0e79C
        #obj = bpy.data.objects
        #for ob in obj:
            #if ob.type == 'MESH':
        #bpy.context.scene.objects.active = ob
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles(threshold=0.0001, use_unselected=False)
        # Force edges
        #bpy.ops.mesh.select_mode(type="EDGE")
        bpy.ops.object.mode_set(mode='OBJECT')
        # Origin to Geometry
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

        return {'FINISHED'}

class iSeparate(bpy.types.Operator):
    """Separate All"""
    bl_idname = "object.isar_separate"
    bl_label = "iSar Separate All"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if len(context.selected_objects) == 0:
            return False
        return True

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        #bpy.ops.mesh.subdivide(number_cuts=3)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.inset(thickness=0, use_individual=True)
        bpy.ops.mesh.delete(type='FACE')
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

        return {'FINISHED'}

class iHole(bpy.types.Operator):
    """Hole"""
    bl_idname = "object.isar_hole"
    bl_label = "iSar Hole"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if len(context.selected_objects) == 0:
            return False
        return True

    def execute(self, context):
        # Boolean Modifiers [8]
        # [8]: http://bit.ly/1DO4y2l
        bpy.ops.object.mode_set(mode='OBJECT')
        obj_A = bpy.context.scene.objects.active
        # List objects already used in the modifier of the obj_A
        objs_modifiers = []
        for modifier in obj_A.modifiers:
            if modifier.type == "BOOLEAN":
                # Checks if modifier has any object specified and append name
                if modifier.object:
                    objs_modifiers.append(modifier.object.name)
        # List objects to use as modifiers
        objs = []
        for ob in bpy.context.scene.objects:
            if ob.name.endswith("_bounding_box") and ob.name not in objs_modifiers:
                objs.append(ob.name)
                # Hide Bounding Box
                #ob.hide = True
        for ob in objs:
            obj_B = bpy.context.scene.objects.get(ob)
            # Object Modifiers [9]
            # [9]: http://www.blender.org/api/blender_python_api_2_57_release/bpy.types.ObjectModifiers.html#bpy.types.ObjectModifiers.new
            boo = obj_A.modifiers.new('isar_boolean', 'BOOLEAN')
            boo.object = obj_B
            boo.operation = 'DIFFERENCE'
            # Apply modifier
            #bpy.ops.object.modifier_apply(apply_as='DATA', modifier="isar_boolean")
            #bpy.context.scene.objects.unlink(obj_B)

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
        col = layout.column(align=True)
        col.operator('object.isar_point', icon="LAYER_USED", text=isar_lang['iPoint'])
        row = col.row(align=True)
        row.operator("object.isar_line", icon="GREASEPENCIL", text=isar_lang['iLine'])
        row = col.row(align=True)
        row.operator('object.isar_origin_geometry', icon="MESH_DATA", text=isar_lang['iGeometry'])
        row = col.row(align=True)
        row.operator("object.isar_bounding_boxers", icon="MESH_CUBE", text=isar_lang['iBoundingBox'])
        row.operator('object.isar_hole', icon="MOD_BOOLEAN", text=isar_lang['iHole'])
        row = col.row(align=True)
        row.operator("object.isar_window_bounding_boxers", icon="MOD_LATTICE", text=isar_lang['iBoundingBoxWindow'])
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

isar_classes = [ iSarPanel, iLanguage, iBoundingBox, iWipe, iOrthoCam, iConsole, iNtersect, iPoint, iGeometry, iPivotToSelected, iSeparate, iHole, iSelectionToCursor, iCreateOrientation, iBoundingBoxWindow, iLine ]

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
