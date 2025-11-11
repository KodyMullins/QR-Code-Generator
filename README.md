# QR Code Generator

A modern, cross-platform QR code generator with support for URLs/text and WiFi networks.

## Features

- **URL/Text Mode**: Generate QR codes from any text or URL
- **WiFi Mode**: Generate QR codes for WiFi networks (auto-connect)
- **Modern UI**: Clean, professional interface built with PyQt6
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Preview & Save**: Preview QR codes before saving as PNG or JPEG

## Requirements

- Python 3.13 or higher
- `uv` package manager

## Installation

### 1. Install uv (if not already installed)

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Install Dependencies

Navigate to the project directory and run:

```bash
uv sync
```

This will automatically install all required dependencies:
- PyQt6
- qrcode
- pillow

## Running the Application

```bash
uv run python main.py
```

## Usage

### URL/Text Mode
1. Click "URL / Text Mode"
2. Enter your text or URL
3. Click "Preview QR Code"
4. Save the QR code to your computer

### WiFi Mode
1. Click "WiFi Mode"
2. Enter your WiFi network name (SSID)
3. Enter your WiFi password
4. Select security type (WPA/WPA2, WEP, or No Password)
5. Click "Preview QR Code"
6. Save the QR code - others can scan it to auto-connect to your WiFi!

## Building Standalone Executables (Optional)

To create standalone executables that don't require Python:

### Install PyInstaller
```bash
uv add --dev pyinstaller
```

### Build for Windows
```bash
uv run pyinstaller --onefile --windowed --name "QR-Code-Generator" main.py
```

### Build for Linux
```bash
uv run pyinstaller --onefile --windowed --name "QR-Code-Generator" main.py
```

The executable will be created in the `dist/` folder.

### Running the Executable

**Windows:**
1. Navigate to the `dist/` folder
2. Double-click `QR-Code-Generator.exe`

**Linux:**
1. Navigate to the `dist/` folder
2. Make the file executable (first time only):
   ```bash
   chmod +x QR-Code-Generator
   ```
3. Run the executable:
4. `./QR-Code-Generator`
   Or double-click the file in your file manager.


