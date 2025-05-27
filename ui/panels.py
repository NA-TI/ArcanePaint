import bpy
from bpy.types import Panel

class ARCANEPAINT_PT_main_panel(Panel):
    bl_label = "ArcanePaint"
    bl_idname = "ARCANEPAINT_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ArcanePaint'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.arcane_paint_settings

        # Texture Setup
        box = layout.box()
        box.label(text="Texture Setup")
        box.prop(settings, "use_triplanar")
        box.prop(settings, "texture_scale")
        box.prop(settings, "blend_factor")
        
        # Apply Texture Projection
        box.operator("arcanepaint.apply_texture_projection")
        
        # Shader Settings
        box = layout.box()
        box.label(text="Shader Settings")
        box.prop(settings, "rim_light_intensity")
        box.prop(settings, "edge_highlight_intensity")
        
        # Paint Mode
        box = layout.box()
        box.label(text="Paint Mode")
        row = box.row()
        row.operator("paint.texture_paint_toggle", text="Toggle Paint Mode")
        
        # Layer Stack
        box = layout.box()
        box.label(text="Layer Stack")
        for i, layer in enumerate(settings.layers):
            row = box.row()
            row.prop(layer, "name", text="")
            row.prop(layer, "opacity", text="")
            row.operator("arcanepaint.remove_layer", text="", icon='X').layer_index = i
        
        box.operator("arcanepaint.add_layer", text="Add Layer")

class ARCANEPAINT_PT_paint_settings(Panel):
    bl_label = "Paint Settings"
    bl_idname = "ARCANEPAINT_PT_paint_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ArcanePaint'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'PAINT_TEXTURE'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.arcane_paint_settings

        # Brush Settings
        box = layout.box()
        box.label(text="Brush Settings")
        box.prop(settings, "brush_size")
        box.prop(settings, "brush_strength")
        box.prop(settings, "brush_texture")
        
        # Stroke Settings
        box = layout.box()
        box.label(text="Stroke Settings")
        box.prop(settings, "stroke_type")
        box.prop(settings, "stroke_randomness")
        box.prop(settings, "stroke_scale")

def register():
    bpy.utils.register_class(ARCANEPAINT_PT_main_panel)
    bpy.utils.register_class(ARCANEPAINT_PT_paint_settings)

def unregister():
    bpy.utils.unregister_class(ARCANEPAINT_PT_paint_settings)
    bpy.utils.unregister_class(ARCANEPAINT_PT_main_panel) 