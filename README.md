# ArcanePaint - Blender Add-on

ArcanePaint is a powerful Blender add-on that creates seamless, hand-painted Arcane-style shading for 3D models. It provides advanced texture projection, GPU acceleration, and optimized performance features.

## Features

- **Seamless Texture Projection**: Triplanar mapping with UV blend support
- **GPU Acceleration**: Metal and OptiX support for faster processing
- **Performance Optimizations**: Multi-threading, memory management, and caching
- **Material Preview**: Enhanced material visualization
- **Geometry Nodes**: Advanced mesh operations support

## Visual Guide

### Before and After Examples

![Before and After Comparison](docs/images/before_after.png)
*Left: Original model. Right: After applying ArcanePaint shader*

### Interface Overview

![ArcanePaint Panel](docs/images/panel.png)
*The ArcanePaint panel in the 3D View sidebar*

### Texture Projection Settings

![Texture Projection Settings](docs/images/texture_settings.png)
*Texture projection settings panel with scale and blend controls*

### Performance Settings

![Performance Settings](docs/images/performance_settings.png)
*Performance optimization settings*

### GPU Acceleration

![GPU Settings](docs/images/gpu_settings.png)
*GPU acceleration settings and status*

## Requirements

- Blender 4.4 or higher
- Python 3.7 or higher
- NumPy 1.21.0 or higher
- GPU with Metal (macOS) or OptiX (NVIDIA) support (optional but recommended)

## Installation

1. Download the ArcanePaint add-on files
2. Open Blender
3. Go to Edit > Preferences > Add-ons
4. Click "Install" and select the ArcanePaint folder
5. Enable the add-on by checking its checkbox

## Usage

### Basic Workflow

1. Open Blender and create or import your 3D model
2. Select the model in the viewport
3. Open the ArcanePaint panel (N key > ArcanePaint tab)
4. Adjust the settings:
   - Scale: Adjust the texture scale (default: 1.0)
   - Blend Factor: Control the blend between UV and triplanar mapping (0.0 to 1.0)
   - Use GPU: Enable/disable GPU acceleration
   - Number of Threads: Set how many threads to use for processing (1-16)
5. Click "Apply Texture Projection"

![Basic Workflow](docs/images/workflow.gif)
*Step-by-step workflow demonstration*

### Performance Settings

The add-on automatically optimizes:
- Viewport performance
- Memory usage
- GPU acceleration
- Multi-threading

### Advanced Features

#### GPU Acceleration
The add-on automatically uses GPU features when available:
- Metal (on macOS)
- OptiX (on NVIDIA GPUs)
- Screen Space Reflections
- Custom shaders for better performance

#### Memory Management
The add-on automatically:
- Caches frequently used data
- Cleans up unused resources
- Manages GPU memory
- Optimizes viewport performance

## Tips for Best Performance

1. **GPU Usage**:
   - Enable GPU acceleration if you have a compatible GPU
   - Use Metal on macOS or OptiX on NVIDIA GPUs
   - Ensure your GPU drivers are up to date

2. **Thread Management**:
   - Set the number of threads based on your CPU
   - Default is 4 threads, adjust based on your system
   - More threads don't always mean better performance

3. **Texture Mapping**:
   - Use the blend factor to balance between UV and triplanar mapping
   - Higher blend factors favor triplanar mapping
   - Lower blend factors favor UV mapping

4. **Memory Optimization**:
   - Let the add-on handle memory management automatically
   - The add-on will clean up unused resources
   - Cache size is limited to prevent memory bloat

## Troubleshooting

### Common Issues

1. **Performance Issues**:
   - Reduce the number of threads
   - Disable GPU acceleration
   - Check if your model has proper UV maps
   - Ensure you have enough system memory

2. **GPU Acceleration Not Working**:
   - Check if your GPU is compatible
   - Update your GPU drivers
   - Verify Metal/OptiX support
   - Check Blender's GPU settings

3. **Memory Issues**:
   - Reduce the number of objects being processed
   - Clear unused data blocks
   - Restart Blender if memory usage is high
   - Check system memory availability

### Error Messages

- **"GPU not available"**: Your GPU is not compatible or drivers are outdated
- **"Memory limit exceeded"**: System memory is running low
- **"Thread count invalid"**: Number of threads is outside valid range
- **"UV map missing"**: Model needs UV maps for proper blending

## Development

### Project Structure

```
ArcanePaint/
├── __init__.py
├── operators/
│   └── texture_projection.py
├── ui/
│   └── panels.py
├── shaders/
│   └── painterly_shader.py
├── utils/
│   ├── performance.py
│   └── mesh_utils.py
└── tests/
    └── test_addon.py
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Building from Source

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run tests:
   ```bash
   python -m unittest tests/test_addon.py
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Blender Foundation for the amazing 3D software
- The Blender Python API community
- Contributors and testers of the add-on

## Support

For support, please:
1. Check the troubleshooting section
2. Search existing issues
3. Create a new issue if needed

## Version History

- 1.0.0: Initial release
  - Basic texture projection
  - GPU acceleration
  - Performance optimizations
  - Memory management