import bpy

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
