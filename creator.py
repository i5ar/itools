import bpy

# Reset 3D View [6]
# [6]: http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/3D_interaction/Reset_3D_View
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

class iWipe(bpy.types.Operator):
    """Wipe Scene & Centre Cursor"""
    bl_idname = "object.isar_wipe"
    bl_label = "Wipe Scene & Centre Cursor"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        '''Delete MESH, CAMERA and LAMP in the context'''
        scene = bpy.context.scene
        for ob in scene.objects:
            if ob.type == 'MESH' or ob.type == 'CAMERA' or ob.type == 'LAMP':
                ob.select = True
            else:
                ob.select = False
        bpy.ops.object.delete()
        # Snap cursor to center or to specific location.
        bpy.ops.object.empty_add(type='PLAIN_AXES', radius=1, view_align=False, location=(0, 0, 0))
        #bpy.context.area.type = 'VIEW_3D'
        bpy.ops.view3d.snap_cursor_to_selected()
        # If this run from the Text Editor the context need to Go in VIEW_3D and get back to TEXT_EDITOR
        bpy.ops.object.delete(use_global=False)
        #bpy.context.area.type = 'TEXT_EDITOR'

        return {'FINISHED'}

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


class iAddon (bpy.types.Operator):
    """Enable Addon"""
    bl_idname = "object.isar_hack"
    bl_label = "iSar Hack"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Check enabled addon [10]
        # [10]: http://blender.stackexchange.com/questions/15638/how-to-distinguish-between-addon-is-not-installed-and-addon-is-not-enabled
        mod = None
        addon_name = "external_addon_name"                      # File name without extension or folder name
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

        # TODO Move method here
        self.report({'INFO'}, "Work in progress!")

        return {'FINISHED'}
