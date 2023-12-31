import bpy


from ..operators.copy_to_clipboard import MTRX_OT_copy_to_clipboard
from ..operators.generate_report import MTRX_OT_generate_report
from ..utils.path_or import path_or


class MTRX_PT_sidebar(bpy.types.Panel):
    """Display Producion Metrics"""
    bl_label = "Production Metrics"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        in_object_mode: bool = path_or(
            bpy, 'context.object.mode', None) == 'OBJECT'
        active_object: bool = context.active_object is not None
        return in_object_mode and active_object

    def draw(self, context: bpy.types.Context):
        col = self.layout.column(align=True)
        col.operator("metrics.setup_mm", icon="FIXED_SIZE")
        col.separator()
        col.prop(context.scene, "metrics_production_method")
        col.separator()
        col.prop(context.scene, "metrics_density")

        if (context.scene.metrics_production_method == 'WALLED'):
            col = self.layout.column(align=True)
            col.prop(context.scene, "metrics_wall_thickness")

        col.separator()
        col.operator(MTRX_OT_generate_report.bl_idname)

        box = self.layout.box()
        col = box.column(align=True)

        [col.label(text=line)
         for line in context.scene.metrics_report.splitlines()]

        col = self.layout.column(align=False)
        col.operator(MTRX_OT_copy_to_clipboard.bl_idname,
                     text=MTRX_OT_copy_to_clipboard.bl_label,
                     icon='COPYDOWN')
