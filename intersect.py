import bpy

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
