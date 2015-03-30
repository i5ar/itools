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
import bmesh
import math
import mathutils
from bpy_extras import object_utils
from bpy.props import BoolProperty, FloatVectorProperty

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

my_str_classes = [ 'iSarPanel', 'iSwitchLanguage', 'iLanguage', 'iBoundingBoxMesh', 'iLink', 'iWipe', 'iOrthoCam', 'iConsole', 'iNtersect', 'iPoint', 'iGeometry', 'iPivotToSelected', 'iSeparate', 'iHole', 'iSelectionToCursor', 'iCreateOrientation', 'iBoundingBoxWindow' ]

is_lang = {}
handle_lang = True

it_dict = [ 'Strumenti', 'Cambia Lingua:', 'Inglese', 'Circoscrivi', 'Blender StackExchange', 'Pulisci Scena', 'Appendi Camera', 'Console', 'Intersezione', 'Inserisci Punto', 'Elimina Doppioni & Centra Origine', 'Pivot alla Selezione', 'Separa Tutto', 'Sottrai', 'Selezione al Cursore', 'Crea Orientazione alla Normale', 'Aggiungi Finestra & Circoscrivi' ]

en_dict = [ 'Toolset', 'Switch Language:', 'Italiano', 'Bounding Box Wire', 'Blender StackExchange', 'Wipe scene', 'Ortho Camera', 'Console', 'Intersect', 'Set Point', 'Remove Doubles & Center Origin', 'Pivot To Selected', 'Separate All', 'Hole', 'Selection To Cursor', 'Create Normal Orientation', 'Add Window & Bounding Box' ]

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
    global is_lang
    if handle_lang:
        is_lang = get_lang(lang_dict_it)
        handle_lang = False
    else:
        is_lang = get_lang(lang_dict_en)
        handle_lang = True

lang_dict_it = isar_make_lang(my_str_classes, it_dict)
lang_dict_en = isar_make_lang(my_str_classes, en_dict)
vert_max = 0
isar_lang_panel()

class iLanguage (bpy.types.Operator):
    """Language Switcher"""
    bl_idname = "object.isar_language"
    bl_label = "iSar English"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        isar_lang_panel()
        return {'FINISHED'}

# Bounding Box Mesh
class iBoundingBoxMesh (bpy.types.Operator):
    """Bounding Box Mesh"""
    bl_idname = "object.isar_bounding_boxers"
    bl_label = "iSar Bounding Box"
    bl_options = {'REGISTER', 'UNDO'}

    # Make a class with the method below
    @classmethod
    def poll(cls, context):
        '''Available with selected objects'''
        if len(context.selected_objects) == 0:
            return False
        return True

    def execute(self, context):
        # Pivot To Median Point
        bpy.context.space_data.pivot_point = 'MEDIAN_POINT'
        # Bound object
        objects = bpy.context.selected_objects
        i = 0
        self.deleting_child()
        for object in objects:
            self.bounding(i, object)
            i += 1
            # Make objects orientation Local so we can work easier with inclined walls
            bpy.context.space_data.transform_orientation = 'LOCAL'

        # Drop child object in outliner
        for object in objects:
            parent_name = object.name
            child_name = object.name + '_bounding_box'
            minuendo = bpy.data.objects[parent_name]
            sottraendo = bpy.data.objects[child_name]
            bpy.ops.object.select_all(action='DESELECT')
            minuendo.select = True
            sottraendo.select = True
            # Drop child object [10]
            # [10]: http://blender.stackexchange.com/questions/26108/how-do-i-parent-objects
            bpy.context.scene.objects.active = minuendo
            bpy.ops.object.parent_set()
            minuendo.select = True
            sottraendo.select = False

        # Snap to closest point to place the window
        bpy.context.scene.tool_settings.snap_target = 'CLOSEST'
        # Tip to scale the bounding box
        tip = 'You can constrain movement to the local axis by pressing twice either Shift Y or Ctrl Y.'
        self.report({'INFO'}, tip)
        return {'FINISHED'}

    # TODO rename minuendo and sottraendo
    def deleting_child(self):
        selected_objects = bpy.context.selected_objects
        list_parent_names = []
        for selected_object in selected_objects:
            parent_name = selected_object.name
            scene = bpy.context.scene
            # Delete the outliner child
            for ob in scene.objects:
                if ob.name.startswith(parent_name + '_bounding_box'):
                    bpy.ops.object.select_all(action='DESELECT')
                    ob.select = True
                    bpy.ops.object.delete()
            list_parent_names.append(parent_name)
        for parent_name in list_parent_names:
            minuendo = bpy.data.objects[parent_name]
            minuendo.select = True

    def bounding(self, i, obj):
        # Bound Box [1]
        # [1]: http://www.blender.org/api/blender_python_api_2_71_release/bpy.types.Object.html#bpy.types.Object.bound_box
        box = bpy.context.selected_objects[i].bound_box
        # Matrix World [2]
        # [2]: http://www.blender.org/api/blender_python_api_2_71_release/bpy.types.Object.html#bpy.types.Object.matrix_world
        mw = bpy.context.selected_objects[i].matrix_world	
        obName = (bpy.context.selected_objects[i].name + '_bounding_box')
        me = bpy.data.meshes.new(obName + '_mesh')
        # Three ways to create objects [3]
        # [3]: http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Three_ways_to_create_objects
        ob = bpy.data.objects.new(obName, me)
        ob.location = mw.translation
        ob.scale = mw.to_scale()
        ob.rotation_euler = mw.to_euler()
        ob.show_name = False
        # Wireframe the mesh so Enhanced 3D Cursor addon can trace the vertices but we can still look through
        ob.draw_type = 'WIRE'
        # Hide the mesh in render
        ob.hide_render = True
        # Link object to the scene
        bpy.context.scene.objects.link(ob)
        loc = []
        for ver in box:
            loc.append(mathutils.Vector((ver[0],ver[1],ver[2])))
        me.from_pydata(loc, [], [
		(0, 1, 2, 3),
		(4, 7, 6, 5),
		(0, 4, 5, 1),
		(1, 5, 6, 2),
		(2, 6, 7, 3),
		(4, 0, 3, 7)])
        # Geometry [4]
        # [4]: http://wiki.blender.org/index.php/Doc:2.6/Manual/Extensions/Python/Geometry
        me.update(calc_edges=True)
        # Make available object name and origin object name out of the method
        self.orName = bpy.context.selected_objects[i].name
        self.obName = bpy.context.selected_objects[i].name + '_bounding_box'
        return


class iBoundingBoxWindow (bpy.types.Operator):
    """Add Window & Bounding Box Mesh"""
    bl_idname = "object.isar_window_bounding_boxers"
    bl_label = "iSar Bounding Box Window"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        '''Bounding Box Mesh Wire Window'''

        if len(context.selected_objects) > 0:

            selected_objects = bpy.context.selected_objects # List
            active_object = bpy.context.active_object       # Item
            for selected_object in selected_objects:
                if selected_object.name.startswith("Window"):
                    bpy.ops.object.isar_bounding_boxers()

            if not active_object.name.startswith("Window"):
                object = bpy.context.object
                if object.mode == 'EDIT':
                    bpy.ops.view3d.snap_cursor_to_selected()
                    # List vertices coordinates from edge [8]
                    # [8]: http://blender.stackexchange.com/questions/27582/how-to-list-vertices-coordinates-from-edge/27583#27583
                    bpy.ops.object.mode_set(mode = 'OBJECT')
                    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
                    verts_indices = [i.index for i in object.data.vertices if i.select]
                    print('verts_indices = object.data.vertices = '+str(verts_indices)+('\n'))
                    list_v = []
                    for i in verts_indices:
                        local_co = object.data.vertices[i].co
                        print('local_co = object.data.vertices[i].co = '+str(local_co)+('\n'))
                        world_co = object.matrix_world * local_co
                        print('world_co = object.matrix_world * local_co = '+str(world_co)+('\n'))
                        list_v.append(world_co)
                    print(list_v)
                    bpy.ops.object.mode_set(mode = 'EDIT')

                    x = max( abs(list_v[0][0]), abs(list_v[1][0]) ) - min( abs(list_v[0][0]), abs(list_v[1][0]) )
                    y = max( abs(list_v[0][1]), abs(list_v[1][1]) ) - min ( abs(list_v[0][1]), abs(list_v[1][1]) )
                    if y > x:
                        division = x/y
                        # TODO Try to use abs() if something goes wrong
                        # TODO Cross quadrant intersection
                        if list_v[0][0] > list_v[1][0] and list_v[0][1] > list_v[1][1]:
                            angle = -math.atan(division) + math.radians(90)
                            print('y > x | a | '+ str(x) +' / '+ str(y) +' = '+ str(division) +' | '+ str(math.degrees(angle)))
                        elif list_v[0][0] < list_v[1][0] and list_v[0][1] > list_v[1][1]:
                            angle = math.atan(division) + math.radians(90)
                            print('y > x | b | '+ str(x) +' / '+ str(y) +' = '+ str(division) +' | '+ str(math.degrees(angle)))
                        elif list_v[0][0] > list_v[1][0] and list_v[0][1] < list_v[1][1]:
                            angle = -math.acos(division)
                            print('y > x | c | '+ str(x) +' / '+ str(y) +' = '+ str(division) +' | '+ str(math.degrees(angle)))
                        elif list_v[0][0] < list_v[1][0] and list_v[0][1] < list_v[1][1]:
                            angle = -math.atan(division) + math.radians(90)
                            print('y > x | d | '+ str(x) +' / '+ str(y) +' = '+ str(division) +' | '+ str(math.degrees(angle)))
                        else:
                            angle = -math.asin(division)
                            print('y > x | e | '+ str(x) +' / '+ str(y) +' = '+ str(division) +' | '+ str(math.degrees(angle)))
                    elif y <= x:
                        division = y/x
                        if list_v[0][0] > list_v[1][0] and list_v[0][1] > list_v[1][1]:
                            angle = math.atan(division)
                            print('y <= x | a | '+ str(y) +' / '+ str(x) +' = '+ str(division) +' | '+ str(math.degrees(angle)))
                        elif list_v[0][0] > list_v[1][0] and list_v[0][1] < list_v[1][1]:
                            angle = -math.atan(division)
                            print('y <= x | b | '+ str(y) +' / '+ str(x) +' = '+ str(division) +' | '+ str(math.degrees(angle)))
                        elif list_v[0][0] < list_v[1][0] and list_v[0][1] > list_v[1][1]:
                            angle = -math.atan(division)
                            print('y <= x | c | '+ str(y) +' / '+ str(x) +' = '+ str(division) +' | '+ str(math.degrees(angle)))
                        elif list_v[0][0] < list_v[1][0] and list_v[0][1] < list_v[1][1]:
                            angle = math.atan(division)
                            print('y <= x | d | '+ str(y) +' / '+ str(x) +' = '+ str(division) +' | '+ str(math.degrees(angle)))
                        else:
                            angle = -math.asin(division)
                            print('y <= x | e '+ str(y) +' / '+ str(x) +' = '+ str(division) +' | '+ str(math.degrees(angle)))

                    bpy.ops.object.editmode_toggle()
                    # Insert Window
                    bpy.ops.object.select_all(action='TOGGLE')
                    bpy.ops.window.run_action()
                    # Add Window Bounding Box
                    bpy.ops.object.isar_bounding_boxers()
                    # Rotete Window
                    bpy.ops.transform.rotate(value=angle, constraint_axis=(False, False, True))

                    bpy.context.scene.tool_settings.snap_target = 'CENTER'

                else:
                    bpy.ops.object.editmode_toggle()
                    cd = active_object.data
                    cd.vertices[0].select = True
                    bpy.ops.view3d.snap_cursor_to_selected()
                    bpy.ops.object.editmode_toggle()
                    # Insert Window
                    bpy.ops.object.select_all(action='TOGGLE')
                    bpy.ops.window.run_action()
                    # Add Window Bounding Box
                    bpy.ops.object.isar_bounding_boxers()
        else:
            bpy.ops.window.run_action()
        return {'FINISHED'}

class iWipe(bpy.types.Operator):
    """Wipe Scene & Centre Cursor"""
    bl_idname = "object.isar_clean"
    bl_label = "Wipe Scene & Centre Cursor"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        # Delete MESH, CAMERA and LAMP in the context
        scene = bpy.context.scene
        for ob in scene.objects:
            if ob.type == 'MESH' or ob.type == 'CAMERA' or ob.type == 'LAMP':
                ob.select = True
            else: 
                ob.select = False
        bpy.ops.object.delete()

        # Snap cursor to center or to specific location. If this run from TEXT_EDITOR the context need to Go in VIEW_3D and get back to TEXT_EDITOR
        bpy.ops.object.empty_add(type='PLAIN_AXES', radius=1, view_align=False, location=(0, 0, 0))
        #bpy.context.area.type = 'VIEW_3D'
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.delete(use_global=False)
        #bpy.context.area.type = 'TEXT_EDITOR'

        return {'FINISHED'}

# Reset 3D View [5]
# [5]: http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/3D_interaction/Reset_3D_View
class iOrthoCam(bpy.types.Operator):
    """Ortho Camera"""
    bl_idname = "object.isar_ortho_cam"
    bl_label = "Ortho Camera"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0, 0, 10), rotation=(0, 0, 0))
        for obj in bpy.context.scene.objects:
            if obj.type == 'CAMERA':
                print(obj.data.type)
                obj.data.type = 'ORTHO'

        return {'FINISHED'}

class iConsole(bpy.types.Operator):
    """Toggle System Console"""
    bl_idname = "view.isar_console"
    bl_label = "iSar Toggle System Console"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.wm.console_toggle()

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
        # Remove Doubles [6]
        # [6]: http://bit.ly/1C0e79C
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

class iPivotToSelected(bpy.types.Operator):
    """Cursor To Selected & Pivot To Cursor"""
    bl_idname = "object.isar_origin_to_cursor"
    bl_label = "iSar Origin To 3D Cursor"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if len(context.selected_objects) == 0:
            return False
        return True

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.mode_set(mode='OBJECT')
        #bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.context.space_data.pivot_point = 'CURSOR'
        return {'FINISHED'}

class iSelectionToCursor(bpy.types.Operator):
    """Origin To Cursor"""
    bl_idname = "object.isar_selection_to_cursor"
    bl_label = "iSar Origin To 3D Cursor"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if len(context.selected_objects) == 0:
            return False
        return True

    def execute(self, context):
        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
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
        # Boolean Modifiers [7]
        # [7]: http://bit.ly/1DO4y2l
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
            # Object Modifiers [8]
            # [8]: http://www.blender.org/api/blender_python_api_2_57_release/bpy.types.ObjectModifiers.html#bpy.types.ObjectModifiers.new
            boo = obj_A.modifiers.new('isar_boolean', 'BOOLEAN')
            boo.object = obj_B
            boo.operation = 'DIFFERENCE'
            # Apply modifier
            #bpy.ops.object.modifier_apply(apply_as='DATA', modifier="isar_boolean")
            #bpy.context.scene.objects.unlink(obj_B)

        return {'FINISHED'}

class iCreateOrientation(bpy.types.Operator):
    """Create Normal Orientation"""
    bl_idname = "object.isar_create_orientation"
    bl_label = "iSar Create Orientation"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if len(context.selected_objects) == 0:
            return False
        return True

    def execute(self, context):
        bpy.context.space_data.transform_orientation = 'NORMAL'
        bpy.ops.transform.create_orientation(name="Normal Ridge", use_view=False, use=True, overwrite=True)
        bpy.ops.mesh.select_mode(type="VERT")
        return {'FINISHED'}

class iSarPanel(bpy.types.Panel):
    """iSar Panel"""
    bl_idname = "panel.isar"
    bl_label = 'iSar Tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Tools'
    bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):
        global maxim
        global is_lang

        layout = self.layout

        # Label row
        row = layout.row()
        row.label(text=is_lang['iSwitchLanguage'])
        row.operator('object.isar_language', text=is_lang['iLanguage'])

        # Multiple rows & columns
        col = layout.column(align=True)
        col.operator("object.isar_clean", icon="WORLD", text=is_lang['iWipe'])
        row = col.row(align=True)
        row.operator("object.isar_ortho_cam", icon="OUTLINER_OB_CAMERA", text=is_lang['iOrthoCam'])

        # Multiple rows & columns
        col = layout.column(align=True)
        col.operator('object.isar_point', icon="LAYER_USED", text=is_lang['iPoint'])
        row = col.row(align=True)
        row.operator('object.isar_origin_geometry', icon="MESH_DATA", text=is_lang['iGeometry'])
        row = col.row(align=True)
        row.operator("object.isar_bounding_boxers", icon="MESH_CUBE", text=is_lang['iBoundingBoxMesh'])
        row.operator('object.isar_hole', icon="MOD_BOOLEAN", text=is_lang['iHole'])
        row = col.row(align=True)
        row.operator("object.isar_window_bounding_boxers", icon="MOD_LATTICE", text=is_lang['iBoundingBoxWindow'])



        col = layout.column(align=True)
        col.operator('object.isar_create_orientation', icon="MANIPUL", text=is_lang['iCreateOrientation'])
        row = col.row(align=True)
        row.operator("object.isar_origin_to_cursor", icon="CURSOR", text=is_lang['iPivotToSelected'])
        row.operator("object.isar_selection_to_cursor", icon="ARROW_LEFTRIGHT", text=is_lang['iSelectionToCursor'])

        # Simple row
        row = layout.row(align=True)
        row.operator("object.isar_separate", icon="MOD_SOLIDIFY", text=is_lang['iSeparate'])
        row.operator("object.isar_intersect", icon="MOD_BEVEL", text=is_lang['iNtersect'])

        split = layout.split()
        col = split.column(align=False)
        col.operator("view.isar_console", icon="CONSOLE", text=is_lang['iConsole'])

        # Simple column
        split = layout.split()
        col = split.column(align=True)
        col.operator('wm.url_open', icon="LINK", text=is_lang['iLink']).url = 'http://blender.stackexchange.com/'


my_classes = [ iSarPanel, iLanguage, iBoundingBoxMesh, iWipe, iOrthoCam, iConsole, iNtersect, iPoint, iGeometry, iPivotToSelected, iSeparate, iHole, iSelectionToCursor, iCreateOrientation, iBoundingBoxWindow ]

def register():
    global handle_lang
    for my_class in my_classes:
        bpy.utils.register_class(my_class)
    print(isar_ascii_logo)

def unregister():
    reversed_classes = reversed(my_classes)
    for my_class in reversed_classes:
        bpy.utils.unregister_class(my_class)
    del reversed_classes

if __name__ == "__main__":
    register()
