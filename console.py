import bpy

class iConsole(bpy.types.Operator):
    """Toggle System Console"""
    bl_idname = "view.isar_console"
    bl_label = "iSar Toggle System Console"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.wm.console_toggle()

        return {'FINISHED'}
