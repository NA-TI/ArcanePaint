import bpy
from bpy.types import Operator
from bpy.props import FloatProperty, BoolProperty, IntProperty
import mathutils
import bmesh
from mathutils import Vector
from ..utils.performance import (
    PerformanceCache,
    GPUBatchManager,
    ThreadPoolManager,
    optimize_viewport_performance,
    setup_material_preview,
    setup_geometry_nodes,
    optimize_memory_usage
)

class ARCANEPAINT_OT_apply_texture_projection(Operator):
    """Apply triplanar texture projection to selected objects"""
    bl_idname = "arcanepaint.apply_texture_projection"
    bl_label = "Apply Texture Projection"
    bl_options = {'REGISTER', 'UNDO'}
    
    scale: FloatProperty(
        name="Scale",
        description="Scale of the texture projection",
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
    
    use_gpu: BoolProperty(
        name="Use GPU Acceleration",
        description="Use GPU for faster processing",
        default=True
    )
    
    num_threads: IntProperty(
        name="Number of Threads",
        description="Number of threads to use for processing",
        default=4,
        min=1,
        max=16
    )
    
    def _process_object(self, obj: bpy.types.Object):
        """Process a single object with optimized settings"""
        # Create a new material if none exists
        if not obj.data.materials:
            mat = bpy.data.materials.new(name=f"{obj.name}_ArcanePaint")
            obj.data.materials.append(mat)
        else:
            mat = obj.data.materials[0]
        
        # Set up material preview
        setup_material_preview(bpy.context, mat)
        
        # Enable nodes
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        # Clear existing nodes
        nodes.clear()
        
        # Create triplanar mapping nodes
        mapping_x = nodes.new('ShaderNodeMapping')
        mapping_y = nodes.new('ShaderNodeMapping')
        mapping_z = nodes.new('ShaderNodeMapping')
        
        # Create texture coordinate nodes
        texcoord = nodes.new('ShaderNodeTexCoord')
        
        # Create separate XYZ nodes
        separate_xyz = nodes.new('ShaderNodeSeparateXYZ')
        
        # Create mix nodes for blending
        mix_xy = nodes.new('ShaderNodeMix')
        mix_xyz = nodes.new('ShaderNodeMix')
        
        # Position nodes
        texcoord.location = (-1200, 0)
        separate_xyz.location = (-1000, 0)
        mapping_x.location = (-800, 200)
        mapping_y.location = (-800, 0)
        mapping_z.location = (-800, -200)
        mix_xy.location = (-400, 100)
        mix_xyz.location = (-200, 0)
        
        # Connect nodes
        links.new(texcoord.outputs['Generated'], separate_xyz.inputs['Vector'])
        links.new(separate_xyz.outputs['X'], mapping_x.inputs['Vector'])
        links.new(separate_xyz.outputs['Y'], mapping_y.inputs['Vector'])
        links.new(separate_xyz.outputs['Z'], mapping_z.inputs['Vector'])
        
        # Set up mapping nodes
        for mapping in [mapping_x, mapping_y, mapping_z]:
            mapping.inputs['Scale'].default_value = (self.scale, self.scale, self.scale)
        
        # Connect mix nodes
        links.new(mapping_x.outputs['Vector'], mix_xy.inputs[1])
        links.new(mapping_y.outputs['Vector'], mix_xy.inputs[2])
        links.new(mapping_z.outputs['Vector'], mix_xyz.inputs[2])
        links.new(mix_xy.outputs['Vector'], mix_xyz.inputs[1])
        
        # Set blend factors
        mix_xy.blend_type = 'MIX'
        mix_xyz.blend_type = 'MIX'
        mix_xy.inputs[0].default_value = self.blend_factor
        mix_xyz.inputs[0].default_value = self.blend_factor
        
        # Create output node
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (0, 0)
        
        # Connect to output
        links.new(mix_xyz.outputs['Vector'], output.inputs['Surface'])
        
        # Set up geometry nodes for advanced mesh operations
        if self.use_gpu:
            setup_geometry_nodes(bpy.context, obj)
        
        # Cache mesh data for better performance
        PerformanceCache.get_mesh_data(obj)
    
    def execute(self, context):
        # Optimize viewport performance
        optimize_viewport_performance(context)
        
        # Get selected objects
        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        
        # Create thread pool manager
        thread_pool = ThreadPoolManager(max_workers=self.num_threads)
        
        # Process objects in parallel
        futures = []
        for obj in selected_objects:
            future = thread_pool.submit(self._process_object, obj)
            futures.append(future)
        
        # Wait for all processing to complete
        thread_pool.wait_all()
        
        # Optimize memory usage
        optimize_memory_usage()
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ARCANEPAINT_OT_apply_texture_projection)

def unregister():
    bpy.utils.unregister_class(ARCANEPAINT_OT_apply_texture_projection) 