import bpy

def initialize_node_system():
    """Minimal node system check"""
    return True

def cleanup_node_system():
    """Clean up any test materials"""
    try:
        if "ArcanePaint_Test" in bpy.data.materials:
            bpy.data.materials.remove(bpy.data.materials["ArcanePaint_Test"])
    except:
        pass 