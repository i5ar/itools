import bpy

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
