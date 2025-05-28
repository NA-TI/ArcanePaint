<p align="center">
  <h1 align="center">🎨 ArcanePaint - Blender Add-on</h1>
  <p align="center"><em>Seamless Arcane-style shading, GPU acceleration, and optimized performance for Blender 4.4+</em></p>

  <p align="center">
    <img src="https://img.shields.io/badge/blender-4.4%2B-orange" alt="Blender 4.4+"/>
    <img src="https://img.shields.io/badge/gpu-acceleration-blue" alt="GPU Acceleration"/>
    <img src="https://img.shields.io/badge/python-3.7%2B-yellow" alt="Python 3.7+"/>
    <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License"/>
    <img src="https://img.shields.io/badge/last%20update-2024-blue" alt="Last Update"/>
  </p>
</p>

---

## 🌐 About

**ArcanePaint** is a powerful Blender add-on for creating seamless, hand-painted Arcane-style shading on 3D models. It features advanced texture projection, GPU acceleration, and performance optimizations for artists and technical users alike.

---

### 🧰 Tools & Technologies

<p align="center">
  <img src="https://img.shields.io/badge/Blender-4.4%2B-orange?logo=blender&logoColor=white" alt="Blender"/>
  <img src="https://img.shields.io/badge/Python-3.7%2B-yellow?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/NumPy-1.21%2B-blue?logo=numpy&logoColor=white" alt="NumPy"/>
  <img src="https://img.shields.io/badge/Metal/OptiX-GPU-blue" alt="Metal/OptiX"/>
  <img src="https://img.shields.io/badge/Geometry%20Nodes-advanced-lightgrey" alt="Geometry Nodes"/>
</p>

---

## ⚙️ Features

- 🖌️ **Seamless Texture Projection**: Triplanar mapping with UV blend support
- 🚀 **GPU Acceleration**: Metal (macOS) & OptiX (NVIDIA) support
- ⚡ **Performance Optimizations**: Multi-threading, memory management, and caching
- 👁️ **Material Preview**: Enhanced material visualization
- 🧩 **Geometry Nodes**: Advanced mesh operations

---

## 🖼️ Visual Guide

<!-- Replace the image paths below with your actual screenshots if available -->
<p align="center">
  <img src="docs/images/before_after.png" width="400"/>
  <br><em>Left: Original model. Right: After applying ArcanePaint shader</em>
</p>

<p align="center">
  <img src="docs/images/panel.png" width="400"/>
  <br><em>The ArcanePaint panel in the 3D View sidebar</em>
</p>

<p align="center">
  <img src="docs/images/texture_settings.png" width="400"/>
  <br><em>Texture projection settings panel with scale and blend controls</em>
</p>

<p align="center">
  <img src="docs/images/performance_settings.png" width="400"/>
  <br><em>Performance optimization settings</em>
</p>

<p align="center">
  <img src="docs/images/gpu_settings.png" width="400"/>
  <br><em>GPU acceleration settings and status</em>
</p>

---

## 🖥️ Requirements

- Blender 4.4 or higher
- Python 3.7 or higher
- NumPy 1.21.0 or higher
- GPU with Metal (macOS) or OptiX (NVIDIA) support (optional but recommended)

---

## 🚀 Installation

1. Download the ArcanePaint add-on files
2. Open Blender
3. Go to Edit > Preferences > Add-ons
4. Click "Install" and select the ArcanePaint zip file
5. Enable the add-on by checking its checkbox

---

## 📝 Usage

### Basic Workflow

1. Open Blender and create or import your 3D model
2. Select the model in the viewport
3. Open the ArcanePaint panel (N key > ArcanePaint tab)
4. Adjust the settings:
   - **Scale**: Adjust the texture scale (default: 1.0)
   - **Blend Factor**: Control the blend between UV and triplanar mapping (0.0 to 1.0)
   - **Use GPU**: Enable/disable GPU acceleration
   - **Number of Threads**: Set how many threads to use for processing (1-16)
5. Click "Apply Texture Projection"

<!-- Replace with your actual workflow GIF if available -->
<p align="center">
  <img src="docs/images/workflow.gif" width="400"/>
  <br><em>Step-by-step workflow demonstration</em>
</p>

---

### Performance & Advanced Features

- **GPU Acceleration**: Metal (macOS), OptiX (NVIDIA), custom shaders, and screen space reflections
- **Memory Management**: Automatic caching, cleanup, and GPU memory optimization
- **Thread Management**: Multi-threading for faster processing

---

## 💡 Tips for Best Performance

- Enable GPU acceleration if you have a compatible GPU
- Adjust thread count based on your CPU (default: 4)
- Use blend factor to balance between UV and triplanar mapping
- Let the add-on handle memory management automatically

---

## 🛠️ Troubleshooting

**Common Issues:**
- Performance: Lower thread count, disable GPU, check UV maps, ensure enough memory
- GPU: Check compatibility, update drivers, verify Metal/OptiX support
- Memory: Reduce objects, clear unused data, restart Blender

**Error Messages:**
- "GPU not available": GPU not compatible or drivers outdated
- "Memory limit exceeded": System memory is running low
- "Thread count invalid": Number of threads is outside valid range
- "UV map missing": Model needs UV maps for proper blending

---

## 🗂️ Project Structure

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

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 🏗️ Building from Source

```bash
git clone <repo-url>
pip install -r requirements.txt
python -m unittest tests/test_addon.py
```

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🙏 Acknowledgments

- Blender Foundation
- Blender Python API community
- Contributors and testers

---

## 🆘 Support

- Check the troubleshooting section
- Search existing issues
- Create a new issue if needed

---

## 🕒 Version History

- 1.0.0: Initial release (texture projection, GPU acceleration, performance optimizations, memory management)