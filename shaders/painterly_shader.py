import bpy
from bpy.types import NodeTree, Node, NodeSocket
from bpy.props import FloatProperty, BoolProperty
from ..utils.node_system import initialize_node_system, cleanup_node_system

class PainterlyShaderNodeTree(NodeTree):
    """Painterly shader node tree type"""
    bl_idname = 'PainterlyShaderNodeTree'
    bl_label = "Painterly Shader"
    bl_icon = 'NODETREE'

class PainterlyShaderNode(Node):
    """Base class for painterly shader nodes"""
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'PainterlyShaderNodeTree'

def create_painterly_shader_node_group():
    """Create the main painterly shader node group"""
    try:
        # Check if node group already exists
        if "ArcanePaint_PainterlyShader" in bpy.data.node_groups:
            return bpy.data.node_groups["ArcanePaint_PainterlyShader"]
        
        # Create a new node group
        node_group = bpy.data.node_groups.new(type="ShaderNodeTree", name="ArcanePaint_PainterlyShader")
        
        # Create group inputs
        group_inputs = node_group.nodes.new("NodeGroupInput")
        node_group.inputs.new("NodeSocketColor", "Base Color")
        node_group.inputs.new("NodeSocketFloat", "Rim Light Intensity")
        node_group.inputs.new("NodeSocketFloat", "Edge Highlight Intensity")
        
        # Create group outputs
        group_outputs = node_group.nodes.new("NodeGroupOutput")
        node_group.outputs.new("NodeSocketShader", "Shader")
        
        # Create the main shader nodes
        principled_bsdf = node_group.nodes.new("ShaderNodeBsdfPrincipled")
        output_node = node_group.nodes.new("ShaderNodeOutputMaterial")
        
        # Create rim lighting nodes
        fresnel = node_group.nodes.new("ShaderNodeFresnel")
        mix_shader = node_group.nodes.new("ShaderNodeMix")
        emission = node_group.nodes.new("ShaderNodeEmission")
        
        # Position nodes
        group_inputs.location = (-600, 0)
        principled_bsdf.location = (-200, 0)
        fresnel.location = (-400, -200)
        mix_shader.location = (0, 0)
        emission.location = (-200, -200)
        group_outputs.location = (200, 0)
        output_node.location = (400, 0)
        
        # Connect nodes
        node_group.links.new(group_inputs.outputs["Base Color"], principled_bsdf.inputs["Base Color"])
        node_group.links.new(group_inputs.outputs["Rim Light Intensity"], fresnel.inputs["IOR"])
        node_group.links.new(fresnel.outputs["Fac"], mix_shader.inputs["Factor"])
        node_group.links.new(principled_bsdf.outputs["BSDF"], mix_shader.inputs[1])
        node_group.links.new(emission.outputs["Emission"], mix_shader.inputs[2])
        node_group.links.new(mix_shader.outputs["Shader"], output_node.inputs["Surface"])
        node_group.links.new(output_node.outputs["Material Output"], group_outputs.inputs["Shader"])
        
        return node_group
    except Exception as e:
        print(f"Error creating painterly shader node group: {e}")
        return None

def register():
    try:
        # Register node tree type
        bpy.utils.register_class(PainterlyShaderNodeTree)
        bpy.utils.register_class(PainterlyShaderNode)
        
        # Create the node group after registration
        create_painterly_shader_node_group()
    except Exception as e:
        print(f"Error registering painterly shader: {e}")
        unregister()
        raise

def unregister():
    try:
        # Remove the node group if it exists
        if "ArcanePaint_PainterlyShader" in bpy.data.node_groups:
            bpy.data.node_groups.remove(bpy.data.node_groups["ArcanePaint_PainterlyShader"])
        
        # Unregister classes
        bpy.utils.unregister_class(PainterlyShaderNode)
        bpy.utils.unregister_class(PainterlyShaderNodeTree)
    except Exception as e:
        print(f"Error unregistering painterly shader: {e}") 