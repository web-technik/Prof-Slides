# Prof Slide System

The installer will complete `skill/` The file package (including reference 
materials and rendering scripts) should be copied to the standard used by 
AI coding tools in the directory `prof-present-system/`.

When using `--force`, the target `prof-present-system` directory will be completely replaced, 
rather than incrementally overwritten.

## Installation Start

Clone the repository before executing any installation commands：

```powershell
git clone https://github.com/aistechnik/prof-present-system.git
cd prof-present-system
```

## Automatic installation

```powershell
python installer/install.py --opencode --force
```

To install to the project directory, please use `--project --target C:\path\to\project`.
When `--project` is not used, the installer will install to the detected global skills directory.

## Rendering dependency

```powershell
python installer/install.py --render-deps
```

This command explicitly invokes `winget` on Windows to install LibreOffice and Poppler.
The installer does not silently install desktop applications in the background.

If you only need to check the environment without modifying anything：

```powershell
python installer/install.py --check
```
