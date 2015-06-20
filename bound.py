import bpy
#import bmesh
import math
import mathutils
import addon_utils
#from bpy_extras import object_utils

# Bounding Box Mesh
class iBoundingBox (bpy.types.Operator):
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
            # Make objects orientation Local so we can work easier with not orthogonal walls
            bpy.context.space_data.transform_orientation = 'LOCAL'

        # Drop child object in outliner
        for object in objects:
            parent_name = object.name
            child_name = object.name + '_bounding_box'
            object_parent_name = bpy.data.objects[parent_name]
            object_child_name = bpy.data.objects[child_name]
            bpy.ops.object.select_all(action='DESELECT')
            object_parent_name.select = True
            object_child_name.select = True
            # Drop child object [1]
            # [1]: http://blender.stackexchange.com/questions/26108/how-do-i-parent-objects
            bpy.context.scene.objects.active = object_parent_name
            bpy.ops.object.parent_set()
            object_parent_name.select = True
            object_child_name.select = False

        # Snap to closest point to place the window
        bpy.context.scene.tool_settings.snap_target = 'CLOSEST'
        # Tip to scale the bounding box
        tip = 'You can constrain movement to the local axis by pressing twice either Shift Y or Ctrl Y.'
        self.report({'INFO'}, tip)

        return {'FINISHED'}

    # TODO Rename minuendo and sottraendo
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
            object_parent_name = bpy.data.objects[parent_name]
            object_parent_name.select = True

    def bounding(self, i, obj):
        # Bound Box [2]
        # [2]: http://www.blender.org/api/blender_python_api_2_71_release/bpy.types.Object.html#bpy.types.Object.bound_box
        box = bpy.context.selected_objects[i].bound_box
        # Matrix World [3]
        # [3]: http://www.blender.org/api/blender_python_api_2_71_release/bpy.types.Object.html#bpy.types.Object.matrix_world
        mw = bpy.context.selected_objects[i].matrix_world
        obName = (bpy.context.selected_objects[i].name + '_bounding_box')
        me = bpy.data.meshes.new(obName + '_mesh')
        # Three ways to create objects [4]
        # [4]: http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Three_ways_to_create_objects
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
        # Check enabled addon [5]
        # [5]: http://blender.stackexchange.com/questions/15638/how-to-distinguish-between-addon-is-not-installed-and-addon-is-not-enabled
        mod = None
        addon_name = "add_window"
        if addon_name not in addon_utils.addons_fake_modules:
            print("\"%s\" addon is not installed." % addon_name)
            addon_status = "\"%s\" addon is not installed. This method require Window Generator 3!" % addon_name
            self.report({'INFO'}, addon_status)
        else:
            default, state = addon_utils.check(addon_name)
            if not state:
                try:
                    mod = addon_utils.enable(addon_name, default_set=False, persistent=False)
                except:
                    print("Could not enable \"%s\" addon on the fly." % addon_name )
        if mod:
            addon_status = 'Window Generator 3 enabled and running!'
            self.report({'INFO'}, addon_status)

        # Bounding Box Mesh Wire Window
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
                    # List vertices coordinates from edge [6]
                    # [6]: http://blender.stackexchange.com/questions/27582/how-to-list-vertices-coordinates-from-edge/27583#27583
                    bpy.ops.object.mode_set(mode = 'OBJECT')
                    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
                    verts_indices = [i.index for i in object.data.vertices if i.select]
                    print('verts_indices = object.data.vertices = '+str(verts_indices)+('\n'))
                    list_v = []
                    for i in verts_indices:
                        local_co = object.data.vertices[i].co
                        print('local_co: '+str(local_co)+('\n'))
                        world_co = object.matrix_world * local_co
                        print('local_co: '+str(world_co)+('\n'))
                        list_v.append(world_co)
                    print(list_v)
                    bpy.ops.object.mode_set(mode = 'EDIT')
                    # Get the angle of an edge [8]
                    # [7]: http://www.blender.org/api/blender_python_api_2_62_2/mathutils.html#mathutils.Vector.angle
                    # [8]: http://blender.stackexchange.com/questions/32606/get-the-angle-of-an-edge/32611#32611
                    v0 = list_v[0]
                    v1 = list_v[1]
                    track = v0 - v1                         # Vector
                    theta = math.atan2(track[1], track[0])  # Float
                    # Angle in degrees
                    print('theta: '+str(math.degrees(theta)))
                    # Toggle mode
                    bpy.ops.object.editmode_toggle()
                    # Insert Window
                    bpy.ops.object.select_all(action='TOGGLE')
                    bpy.ops.window.run_action()
                    # Add Window Bounding Box
                    bpy.ops.object.isar_bounding_boxers()
                    # Rotate Window
                    bpy.ops.transform.rotate(value=theta, constraint_axis=(False, False, True))
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
