import bpy
import sys
import importlib
from typing import Tuple, List, Optional

def check_blender_version() -> Tuple[bool, str]:
    """Check if Blender version is compatible"""
    required_version = (4, 4, 0)
    current_version = bpy.app.version
    
    if current_version < required_version:
        return False, f"Blender version {required_version[0]}.{required_version[1]} or higher is required"
    return True, "Blender version is compatible"

def check_dependencies() -> Tuple[bool, str]:
    """Check if required dependencies are available"""
    try:
        import numpy
        return True, "All dependencies are available"
    except ImportError as e:
        return False, f"Missing dependency: {str(e)}"

def check_node_system() -> tuple:
    # TEMPORARY: Always return True to bypass node system check
    return True, "Node system check bypassed for debug"

def check_gpu_support() -> Tuple[bool, str]:
    """Check if GPU features are available"""
    try:
        if not bpy.context.preferences.addons['cycles'].preferences.has_active_device():
            return False, "No active GPU device found"
        return True, "GPU support is available"
    except Exception as e:
        return False, f"GPU check error: {str(e)}"

class ArcanePaintError(Exception):
    """Base exception class for ArcanePaint"""
    pass

class CompatibilityError(ArcanePaintError):
    """Raised when compatibility checks fail"""
    pass

class DependencyError(ArcanePaintError):
    """Raised when required dependencies are missing"""
    pass

def run_compatibility_checks() -> Optional[str]:
    """Run all compatibility checks and return error message if any check fails"""
    checks = [
        check_blender_version,
        check_dependencies,
        check_node_system
    ]
    
    for check in checks:
        is_compatible, message = check()
        if not is_compatible:
            return message
    
    return None

def handle_error(error: Exception, context: bpy.types.Context) -> None:
    """Handle errors during registration/unregistration"""
    if isinstance(error, CompatibilityError):
        print(f"Compatibility Error: {error}")
    elif isinstance(error, DependencyError):
        print(f"Dependency Error: {error}")
    else:
        print(f"Unexpected Error: {error}") 