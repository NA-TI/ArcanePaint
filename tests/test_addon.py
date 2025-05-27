import bpy
import unittest
import sys
import os
from ..utils.compatibility import (
    check_blender_version,
    check_dependencies,
    check_node_system,
    check_gpu_support
)

class TestArcanePaintCompatibility(unittest.TestCase):
    def test_blender_version(self):
        """Test Blender version compatibility"""
        version_ok, msg = check_blender_version()
        self.assertTrue(version_ok, msg)

    def test_dependencies(self):
        """Test required dependencies"""
        deps_ok, missing = check_dependencies()
        self.assertTrue(deps_ok, f"Missing dependencies: {missing}")

    def test_node_system(self):
        """Test node system compatibility"""
        node_ok, msg = check_node_system()
        self.assertTrue(node_ok, msg)

    def test_gpu_support(self):
        """Test GPU support"""
        gpu_ok, msg = check_gpu_support()
        self.assertTrue(gpu_ok, msg)

class TestArcanePaintFunctionality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        # Create a test mesh
        bpy.ops.mesh.primitive_cube_add()
        cls.test_object = bpy.context.active_object

    def test_texture_projection(self):
        """Test texture projection operator"""
        # Apply texture projection
        bpy.ops.arcanepaint.apply_texture_projection()
        
        # Check if material was created
        self.assertIsNotNone(self.test_object.data.materials)
        
        # Check if nodes were created
        material = self.test_object.data.materials[0]
        self.assertTrue(material.use_nodes)
        self.assertTrue(len(material.node_tree.nodes) > 0)

    def test_shader_creation(self):
        """Test shader node group creation"""
        from ..shaders.painterly_shader import create_painterly_shader_node_group
        
        # Create shader node group
        node_group = create_painterly_shader_node_group()
        
        # Check if node group was created
        self.assertIsNotNone(node_group)
        
        # Check if required nodes exist
        required_nodes = ['NodeGroupInput', 'NodeGroupOutput', 'ShaderNodeBsdfPrincipled']
        for node_type in required_nodes:
            self.assertTrue(any(node.type == node_type for node in node_group.nodes))

    def test_mesh_utils(self):
        """Test mesh utility functions"""
        from ..utils.mesh_utils import (
            get_mesh_curvature,
            get_uv_seams,
            get_surface_area,
            get_optimal_texture_scale
        )
        
        # Test curvature calculation
        curvature = get_mesh_curvature(self.test_object)
        self.assertIsNotNone(curvature)
        self.assertEqual(len(curvature), len(self.test_object.data.vertices))
        
        # Test surface area calculation
        area = get_surface_area(self.test_object)
        self.assertGreater(area, 0)
        
        # Test texture scale calculation
        scale = get_optimal_texture_scale(self.test_object)
        self.assertGreater(scale, 0)
        self.assertLess(scale, 10)

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment"""
        # Remove test object
        bpy.data.objects.remove(cls.test_object)

def run_tests():
    """Run all tests"""
    # Create test suite
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestArcanePaintCompatibility))
    suite.addTest(unittest.makeSuite(TestArcanePaintFunctionality))
    
    # Run tests
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    run_tests() 