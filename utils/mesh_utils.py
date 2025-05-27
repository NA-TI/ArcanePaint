import bpy
import bmesh
from mathutils import Vector
import numpy as np

def get_mesh_curvature(obj):
    """Calculate mesh curvature for each vertex"""
    if obj.type != 'MESH':
        return None
    
    # Create a bmesh from the object
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    
    # Calculate vertex normals if they don't exist
    if not hasattr(bm.verts, "normal"):
        bm.verts.ensure_lookup_table()
        bmesh.ops.triangulate(bm, faces=bm.faces)
        bm.normal_update()
    
    # Calculate curvature for each vertex
    curvature = np.zeros(len(bm.verts))
    for v in bm.verts:
        # Get connected vertices
        connected_verts = [e.other_vert(v) for e in v.link_edges]
        if not connected_verts:
            continue
        
        # Calculate normal differences
        normal_diffs = []
        for cv in connected_verts:
            normal_diff = (v.normal - cv.normal).length
            normal_diffs.append(normal_diff)
        
        # Average normal difference is our curvature estimate
        curvature[v.index] = sum(normal_diffs) / len(normal_diffs)
    
    bm.free()
    return curvature

def get_uv_seams(obj):
    """Find UV seams in the mesh"""
    if obj.type != 'MESH':
        return None
    
    # Create a bmesh from the object
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    
    # Get UV layer
    uv_layer = bm.loops.layers.uv.active
    if not uv_layer:
        bm.free()
        return None
    
    # Find edges that are UV seams
    seam_edges = []
    for edge in bm.edges:
        if len(edge.link_loops) != 2:
            continue
        
        # Get UV coordinates for both loops
        uv1 = edge.link_loops[0][uv_layer].uv
        uv2 = edge.link_loops[1][uv_layer].uv
        
        # If UVs are different, it's a seam
        if (uv1 - uv2).length > 0.0001:
            seam_edges.append(edge.index)
    
    bm.free()
    return seam_edges

def get_surface_area(obj):
    """Calculate surface area of the mesh"""
    if obj.type != 'MESH':
        return 0.0
    
    # Create a bmesh from the object
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    
    # Calculate total surface area
    area = 0.0
    for face in bm.faces:
        area += face.calc_area()
    
    bm.free()
    return area

def get_optimal_texture_scale(obj, target_texel_density=1024):
    """Calculate optimal texture scale based on surface area"""
    area = get_surface_area(obj)
    if area == 0.0:
        return 1.0
    
    # Calculate scale based on target texel density
    # This is a simplified calculation - you might want to adjust the formula
    scale = (target_texel_density / area) ** 0.5
    return max(0.1, min(10.0, scale))

def create_vertex_groups_from_curvature(obj, curvature, num_groups=5):
    """Create vertex groups based on curvature values"""
    if obj.type != 'MESH' or curvature is None:
        return
    
    # Remove existing curvature groups
    for vg in obj.vertex_groups:
        if vg.name.startswith("Curvature_"):
            obj.vertex_groups.remove(vg)
    
    # Create new vertex groups
    for i in range(num_groups):
        vg = obj.vertex_groups.new(name=f"Curvature_{i}")
        
        # Calculate weight for each vertex
        for v in obj.data.vertices:
            # Map curvature to group weight
            weight = (curvature[v.index] - min(curvature)) / (max(curvature) - min(curvature))
            group_index = int(weight * (num_groups - 1))
            
            if group_index == i:
                vg.add([v.index], 1.0, 'REPLACE')
            else:
                vg.add([v.index], 0.0, 'REPLACE') 