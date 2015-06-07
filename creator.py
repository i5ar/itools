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
