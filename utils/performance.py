import bpy
import numpy as np
from typing import Dict, Any, Optional, List, Tuple, Set
import gpu
from gpu_extras.batch import batch_for_shader
import threading
import queue
import concurrent.futures
from functools import lru_cache
import time
import weakref
import gc
from collections import OrderedDict

class MemoryManager:
    """Advanced memory management system"""
    _instance = None
    _memory_threshold = 0.8  # 80% memory usage threshold
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemoryManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize memory manager"""
        self._tracked_objects: Set[weakref.ref] = set()
        self._last_cleanup = time.time()
        self._cleanup_interval = 300  # 5 minutes
    
    def track_object(self, obj: Any):
        """Track an object for memory management"""
        self._tracked_objects.add(weakref.ref(obj, self._object_finalized))
    
    def _object_finalized(self, ref):
        """Handle object finalization"""
        self._tracked_objects.discard(ref)
    
    def check_memory_usage(self) -> bool:
        """Check if memory usage is above threshold"""
        import psutil
        return psutil.virtual_memory().percent / 100 > self._memory_threshold
    
    def cleanup(self, force: bool = False):
        """Clean up memory if needed"""
        current_time = time.time()
        if force or (current_time - self._last_cleanup) > self._cleanup_interval:
            if self.check_memory_usage():
                gc.collect()
                self._cleanup_unused_data()
                self._last_cleanup = current_time
                return True
        return False
    
    def _cleanup_unused_data(self):
        """Clean up unused Blender data"""
        for data_type in [bpy.data.meshes, bpy.data.materials, bpy.data.textures, bpy.data.images]:
            for item in data_type:
                if item.users == 0:
                    data_type.remove(item)

class PerformanceCache:
    """Enhanced cache system for performance optimization"""
    _mesh_cache: OrderedDict[str, Any] = OrderedDict()
    _texture_cache: OrderedDict[str, Any] = OrderedDict()
    _shader_cache: OrderedDict[str, Any] = OrderedDict()
    _max_cache_size = 1000
    _memory_manager = MemoryManager()
    
    @classmethod
    def get_mesh_data(cls, obj: bpy.types.Object) -> Optional[Dict[str, Any]]:
        """Get cached mesh data or compute if not cached"""
        if obj.name in cls._mesh_cache:
            # Update access time
            data = cls._mesh_cache.pop(obj.name)
            cls._mesh_cache[obj.name] = data
            return data
        
        # Check memory usage
        cls._memory_manager.cleanup()
        
        # Compute and cache mesh data using numpy for better performance
        vertices = np.empty((len(obj.data.vertices), 3), dtype=np.float32)
        normals = np.empty((len(obj.data.vertices), 3), dtype=np.float32)
        
        # Use numpy's vectorized operations
        obj.data.vertices.foreach_get('co', vertices.ravel())
        obj.data.vertices.foreach_get('normal', normals.ravel())
        
        mesh_data = {
            'vertices': vertices,
            'normals': normals,
            'uvs': cls._get_uv_data(obj) if obj.data.uv_layers.active else None,
            'timestamp': time.time()
        }
        
        # Implement cache size management
        if len(cls._mesh_cache) >= cls._max_cache_size:
            cls._mesh_cache.popitem(last=False)  # Remove oldest item
        
        cls._mesh_cache[obj.name] = mesh_data
        cls._memory_manager.track_object(mesh_data)
        return mesh_data
    
    @staticmethod
    @lru_cache(maxsize=128)
    def _get_uv_data(obj: bpy.types.Object) -> np.ndarray:
        """Get UV data with caching"""
        if not obj.data.uv_layers.active:
            return None
        uvs = np.empty((len(obj.data.uv_layers.active.data), 2), dtype=np.float32)
        obj.data.uv_layers.active.data.foreach_get('uv', uvs.ravel())
        return uvs
    
    @classmethod
    def get_texture_data(cls, texture_name: str) -> Optional[Any]:
        """Get cached texture data or load if not cached"""
        if texture_name in cls._texture_cache:
            return cls._texture_cache[texture_name]
        
        texture = bpy.data.images.get(texture_name)
        if texture:
            # Use numpy's optimized array operations
            pixels = np.array(texture.pixels, dtype=np.float32)
            pixels = pixels.reshape(-1, 4)  # Reshape to RGBA format
            
            # Implement cache size management
            if len(cls._texture_cache) >= cls._max_cache_size:
                oldest_key = min(cls._texture_cache.items(), key=lambda x: x[1]['timestamp'])[0]
                cls._texture_cache.pop(oldest_key)
            
            cls._texture_cache[texture_name] = {
                'pixels': pixels,
                'timestamp': time.time()
            }
            return pixels
        return None

class GPUBatchManager:
    """Manager for GPU-accelerated operations"""
    def __init__(self):
        self.shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch = None
        self._vertex_buffer = None
        self._index_buffer = None
    
    def create_batch(self, vertices: np.ndarray, indices: np.ndarray):
        """Create a GPU batch for rendering with optimized buffer management"""
        # Convert to float32 for better GPU performance
        vertices = vertices.astype(np.float32)
        indices = indices.astype(np.uint32)
        
        # Create vertex buffer
        self._vertex_buffer = gpu.types.GPUVertBuf(
            format="3f",
            len=len(vertices),
            data=vertices.tobytes()
        )
        
        # Create index buffer
        self._index_buffer = gpu.types.GPUIndexBuf(
            type="TRIS",
            seq=indices
        )
        
        # Create batch with optimized buffers
        self.batch = batch_for_shader(
            self.shader, 'TRIS',
            {"pos": self._vertex_buffer},
            indices=self._index_buffer
        )
    
    def draw(self, color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)):
        """Draw the batch with optimized state management"""
        if self.batch:
            self.shader.bind()
            self.shader.uniform_4f("color", *color)
            self.batch.draw(self.shader)
    
    def __del__(self):
        """Clean up GPU resources"""
        if self._vertex_buffer:
            self._vertex_buffer.free()
        if self._index_buffer:
            self._index_buffer.free()

class GPUAccelerator:
    """Advanced GPU acceleration system"""
    def __init__(self):
        self._compute_shader = None
        self._vertex_shader = None
        self._fragment_shader = None
        self._initialize_shaders()
    
    def _initialize_shaders(self):
        """Initialize GPU shaders"""
        # Compute shader for parallel processing
        compute_code = """
        #version 430
        layout(local_size_x=256) in;
        
        layout(std430, binding=0) buffer InputBuffer {
            float data[];
        } input_buffer;
        
        layout(std430, binding=1) buffer OutputBuffer {
            float data[];
        } output_buffer;
        
        void main() {
            uint idx = gl_GlobalInvocationID.x;
            if (idx < input_buffer.data.length()) {
                output_buffer.data[idx] = input_buffer.data[idx] * 2.0;
            }
        }
        """
        
        # Vertex shader for geometry processing
        vertex_code = """
        #version 330
        layout(location=0) in vec3 position;
        layout(location=1) in vec3 normal;
        layout(location=2) in vec2 uv;
        
        out vec3 v_normal;
        out vec2 v_uv;
        
        uniform mat4 modelViewMatrix;
        uniform mat4 projectionMatrix;
        
        void main() {
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            v_normal = normal;
            v_uv = uv;
        }
        """
        
        # Fragment shader for rendering
        fragment_code = """
        #version 330
        in vec3 v_normal;
        in vec2 v_uv;
        
        out vec4 fragColor;
        
        uniform sampler2D texture;
        uniform vec3 lightDir;
        
        void main() {
            vec3 normal = normalize(v_normal);
            float diffuse = max(dot(normal, lightDir), 0.0);
            vec4 texColor = texture2D(texture, v_uv);
            fragColor = texColor * diffuse;
        }
        """
        
        try:
            self._compute_shader = gpu.types.GPUShader(compute_code)
            self._vertex_shader = gpu.types.GPUShader(vertex_code)
            self._fragment_shader = gpu.types.GPUShader(fragment_code)
        except Exception as e:
            print(f"Shader initialization failed: {e}")
    
    def process_data(self, input_data: np.ndarray) -> np.ndarray:
        """Process data using GPU compute shader"""
        if self._compute_shader is None:
            return input_data
        
        # Create GPU buffers
        input_buffer = gpu.types.GPUVertBuf(
            format="f",
            len=len(input_data),
            data=input_data.tobytes()
        )
        
        output_buffer = gpu.types.GPUVertBuf(
            format="f",
            len=len(input_data)
        )
        
        # Bind buffers
        self._compute_shader.bind()
        self._compute_shader.uniform_1i("input_buffer", 0)
        self._compute_shader.uniform_1i("output_buffer", 1)
        
        # Dispatch compute shader
        self._compute_shader.dispatch(
            group_count_x=(len(input_data) + 255) // 256
        )
        
        # Read back results
        output_data = np.empty_like(input_data)
        output_buffer.read(output_data)
        
        # Clean up
        input_buffer.free()
        output_buffer.free()
        
        return output_data

class ThreadPoolManager:
    """Enhanced thread pool manager with priority queue"""
    def __init__(self, max_workers: int = None):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self._futures: List[concurrent.futures.Future] = []
        self._priority_queue = queue.PriorityQueue()
        self._memory_manager = MemoryManager()
    
    def submit(self, fn, *args, priority: int = 0, **kwargs) -> concurrent.futures.Future:
        """Submit a task to the thread pool with priority"""
        # Check memory usage before submitting
        self._memory_manager.cleanup()
        
        # Add task to priority queue
        self._priority_queue.put((priority, (fn, args, kwargs)))
        
        # Process highest priority task
        if not self._priority_queue.empty():
            _, (fn, args, kwargs) = self._priority_queue.get()
            future = self.executor.submit(fn, *args, **kwargs)
            self._futures.append(future)
            return future
        return None
    
    def wait_all(self):
        """Wait for all submitted tasks to complete"""
        concurrent.futures.wait(self._futures)
        self._memory_manager.cleanup(force=True)
    
    def __del__(self):
        """Clean up thread pool resources"""
        self.executor.shutdown(wait=True)

def optimize_viewport_performance(context: bpy.types.Context):
    """Enhanced viewport performance optimization"""
    # Enable GPU acceleration
    context.scene.cycles.device = 'GPU'
    context.scene.cycles.use_adaptive_sampling = True
    context.scene.cycles.adaptive_threshold = 0.01
    context.scene.cycles.adaptive_min_samples = 16
    
    # Enable GPU compute features
    if hasattr(context.scene.cycles, 'use_metal'):
        context.scene.cycles.use_metal = True
    if hasattr(context.scene.cycles, 'use_optix'):
        context.scene.cycles.use_optix = True
    
    # Optimize viewport settings
    for area in context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    # Enable viewport optimization
                    space.shading.use_scene_lights = True
                    space.shading.use_scene_world = True
                    space.shading.studio_light = 'Default'
                    space.shading.studiolight_rotate_z = 0
                    space.shading.studiolight_intensity = 1.0
                    space.shading.studiolight_background_alpha = 0.0
                    
                    # Enable viewport optimizations
                    space.shading.use_scene_lights_render = True
                    space.shading.use_scene_world_render = True
                    space.shading.use_scene_material = True
                    space.shading.use_scene_textures = True
                    
                    # Optimize viewport display
                    space.shading.type = 'RENDERED'
                    space.shading.use_scene_material = True
                    space.shading.use_scene_textures = True
                    space.shading.use_scene_world = True
                    space.shading.use_scene_lights = True
                    
                    # Enable GPU features
                    if hasattr(space.shading, 'use_gpu'):
                        space.shading.use_gpu = True
                    if hasattr(space.shading, 'use_ssr'):
                        space.shading.use_ssr = True
                    if hasattr(space.shading, 'use_ssr_refraction'):
                        space.shading.use_ssr_refraction = True

def setup_material_preview(context: bpy.types.Context, material: bpy.types.Material):
    """Set up material preview with optimized settings"""
    # Enable material preview
    material.preview_render_type = 'FLAT'
    material.preview_render_method = 'AUTO'
    
    # Set up preview settings
    material.use_nodes = True
    material.use_preview_world = True
    
    # Optimize preview settings
    material.preview_render_engine = 'CYCLES'
    material.preview_render_samples = 128
    material.preview_render_use_denoising = True
    
    # Additional optimizations
    material.preview_render_use_scene_lights = True
    material.preview_render_use_scene_world = True
    material.preview_render_use_scene_material = True
    material.preview_render_use_scene_textures = True

def setup_geometry_nodes(context: bpy.types.Context, obj: bpy.types.Object):
    """Set up geometry nodes with optimized settings"""
    # Create geometry nodes modifier
    mod = obj.modifiers.new(name="ArcanePaint_Geometry", type='NODES')
    
    # Create node group
    node_group = bpy.data.node_groups.new(type="GeometryNodeTree", name="ArcanePaint_Geometry")
    mod.node_group = node_group
    
    # Add input and output nodes
    inputs = node_group.nodes.new('NodeGroupInput')
    outputs = node_group.nodes.new('NodeGroupOutput')
    
    # Add required input sockets
    node_group.inputs.new('NodeSocketGeometry', "Geometry")
    node_group.inputs.new('NodeSocketFloat', "Scale")
    node_group.inputs.new('NodeSocketFloat', "Blend Factor")
    
    # Add required output sockets
    node_group.outputs.new('NodeSocketGeometry', "Geometry")
    
    # Optimize node group settings
    node_group.use_custom_color = True
    node_group.color = (0.8, 0.8, 0.8)
    
    return mod

def optimize_memory_usage():
    """Enhanced memory usage optimization"""
    # Clear unused data blocks
    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)
    
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)
    
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    
    # Clear GPU memory
    gpu.state.reset()
    
    # Force garbage collection
    gc.collect()
    
    # Clear numpy memory
    np.get_include()
    
    # Clear shader cache
    if hasattr(gpu, 'shader'):
        gpu.shader.from_builtin('3D_UNIFORM_COLOR').bind()
        gpu.shader.from_builtin('3D_UNIFORM_COLOR').unbind() 