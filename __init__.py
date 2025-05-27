bl_info = {
    "name": "ArcanePaint",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (4, 4, 0),
    "location": "View3D > Sidebar > ArcanePaint",
    "description": "Create Arcane-style painterly shading for 3D models",
    "warning": "",
    "doc_url": "",
    "category": "Material",
}

import bpy
from bpy.props import (
    StringProperty,
    BoolProperty,
    FloatProperty,
    EnumProperty,
    PointerProperty,
    CollectionProperty,
)
from bpy.types import (
    Panel,
    Operator,
    PropertyGroup,
)

# Import local modules
from . import operators
from . import ui
from . import shaders
from . import utils
from .utils.compatibility import (
    run_compatibility_checks,
    handle_error,
    CompatibilityError,
    DependencyError
)

# Property Groups
class ArcanePaintLayer(PropertyGroup):
    """Layer settings for ArcanePaint"""
    name: StringProperty(
        name="Name",
        default="Layer"
    )
    opacity: FloatProperty(
        name="Opacity",
        default=1.0,
        min=0.0,
        max=1.0
    )

class ArcanePaintSettings(PropertyGroup):
    """Settings for the ArcanePaint add-on"""
    use_triplanar: BoolProperty(
        name="Use Triplanar Mapping",
        description="Enable triplanar texture projection",
        default=True
    )
    
    texture_scale: FloatProperty(
        name="Texture Scale",
        description="Scale of the brush textures",
        default=1.0,
        min=0.1,
        max=10.0
    )
    
    blend_factor: FloatProperty(
        name="Blend Factor",
        description="Blend between UV and triplanar mapping",
        default=0.5,
        min=0.0,
        max=1.0
    )
    
    rim_light_intensity: FloatProperty(
        name="Rim Light Intensity",
        description="Intensity of the rim lighting effect",
        default=1.0,
        min=0.0,
        max=5.0
    )
    
    edge_highlight_intensity: FloatProperty(
        name="Edge Highlight Intensity",
        description="Intensity of the edge highlighting effect",
        default=1.0,
        min=0.0,
        max=5.0
    )
    
    brush_size: FloatProperty(
        name="Brush Size",
        description="Size of the paint brush",
        default=1.0,
        min=0.1,
        max=100.0
    )
    
    brush_strength: FloatProperty(
        name="Brush Strength",
        description="Strength of the paint brush",
        default=1.0,
        min=0.0,
        max=1.0
    )
    
    brush_texture: StringProperty(
        name="Brush Texture",
        description="Texture to use for the brush",
        default=""
    )
    
    stroke_type: EnumProperty(
        name="Stroke Type",
        description="Type of brush stroke",
        items=[
            ('SOLID', "Solid", "Solid stroke"),
            ('TEXTURE', "Texture", "Textured stroke"),
            ('RANDOM', "Random", "Random stroke")
        ],
        default='SOLID'
    )
    
    stroke_randomness: FloatProperty(
        name="Stroke Randomness",
        description="Amount of randomness in the stroke",
        default=0.0,
        min=0.0,
        max=1.0
    )
    
    stroke_scale: FloatProperty(
        name="Stroke Scale",
        description="Scale of the stroke texture",
        default=1.0,
        min=0.1,
        max=10.0
    )
    
    layers: CollectionProperty(
        type=ArcanePaintLayer,
        name="Layers"
    )

# Registration
classes = (
    ArcanePaintLayer,
    ArcanePaintSettings,
)

def register():
    try:
        print("\n=== ArcanePaint Registration Start ===")
        print(f"Addon path: {__file__}")
        
        # Run compatibility checks
        print("\nRunning compatibility checks...")
        error_msg = run_compatibility_checks()
        if error_msg:
            print(f"Compatibility check failed: {error_msg}")
            return
        
        print("\nRegistering property groups...")
        # Register property groups
        for cls in classes:
            try:
                bpy.utils.register_class(cls)
                print(f"✓ Registered class: {cls.__name__}")
            except Exception as e:
                print(f"✗ Error registering class {cls.__name__}: {e}")
                print(f"  Error type: {type(e)}")
                import traceback
                print(f"  Traceback: {traceback.format_exc()}")
                continue
        
        print("\nRegistering scene properties...")
        # Register scene properties
        try:
            bpy.types.Scene.arcane_paint_settings = PointerProperty(type=ArcanePaintSettings)
            print("✓ Registered scene properties")
        except Exception as e:
            print(f"✗ Error registering scene properties: {e}")
            print(f"  Error type: {type(e)}")
            import traceback
            print(f"  Traceback: {traceback.format_exc()}")
            return
        
        print("\nRegistering modules...")
        # Register modules in correct order
        try:
            print("\nRegistering utils...")
            utils.register()  # Register utils first
            print("✓ Utils registered")
            
            print("\nRegistering shaders...")
            shaders.register()  # Register shaders before operators
            print("✓ Shaders registered")
            
            print("\nRegistering operators...")
            operators.register()
            print("✓ Operators registered")
            
            print("\nRegistering UI...")
            ui.register()
            print("✓ UI registered")
            
            print("\nAll modules registered successfully")
        except Exception as e:
            print(f"✗ Error registering modules: {e}")
            print(f"  Error type: {type(e)}")
            import traceback
            print(f"  Traceback: {traceback.format_exc()}")
            try:
                unregister()
            except:
                pass
            return
        
        print("\n=== ArcanePaint Registration Complete ===")
        
    except Exception as e:
        print(f"\n✗ Unexpected error during registration: {e}")
        print(f"  Error type: {type(e)}")
        import traceback
        print(f"  Traceback: {traceback.format_exc()}")
        try:
            unregister()
        except:
            pass
        return

def unregister():
    try:
        # Unregister modules in reverse order
        ui.unregister()
        operators.unregister()
        shaders.unregister()
        utils.unregister()
        
        # Unregister scene properties
        del bpy.types.Scene.arcane_paint_settings
        
        # Unregister property groups
        for cls in reversed(classes):
            bpy.utils.unregister_class(cls)
            
        # Clean up node system
        from .utils.node_system import cleanup_node_system
        cleanup_node_system()
            
    except Exception as e:
        handle_error(e, bpy.context)
        raise

if __name__ == "__main__":
    register() 