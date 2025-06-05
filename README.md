# Face Analysis API

## Overview
A RESTful API for Alzheimer's Disease (AD) facial asymmetry analysis using computer vision and machine learning techniques.

## Features
- 🔍 **Automated face detection** using MediaPipe FaceMesh (468 landmarks)
- 📊 **Asymmetry classification** powered by XGBoost machine learning model
- 🖼️ **Visual analysis** with marked facial landmarks and symmetry lines
- 📦 **Multi-format support** for compressed image archives

## Input
Upload a compressed archive containing facial photographs:
- **Supported formats**: `.zip`, `.7z`, `.rar`
- **File size limit**: 50MB
- **Image formats**: JPG, JPEG, PNG, BMP, TIFF
- **Recommended**: 5-20 front-facing photos for optimal accuracy

## Output
Returns a JSON response with analysis results:

```json
{
  "success": true,
  "error": null,
  "asymmetry_classification_result": 0.85,
  "marked_figure": "data:image/jpeg;base64,/9j/4AAQ..."
}
```

## Project Structure
```
api/
├── data/
│   ├── .gitignore
│   ├── haarcascade_frontalface_default.xml
│   ├── symmetry_all_pairs.csv  # Facial symmetry mapping
│   └── XGBoost.json            # Pre-trained ML model
├── .gitignore                  
├── main.py                     # Application entry point
├── poetry.lock                 # Locked dependency versions
├── pyproject.toml              # Poetry dependencies
└── README.md
```

## Installation

### Prerequisites
- Python 3.11.x
- Intel RealSense SDK
- Arduino IDE (for LED functionality)
- Git

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/a7266165/AD-Sensor-Project.git
   cd AD-Sensor-Project
   ```

2. **Install Poetry for dependency management** (Skip if already installed)
   ```bash
   # Create poetry environment
   conda create -n poetry python=3.11
   
   # Activate the poetry environment
   conda activate poetry
   
   # Install poetry in this environment
   pip install poetry
   
   # Add poetry to PATH (optional but recommended)
   # For Windows:
   # Add the poetry installation path to your system PATH environment variable
   # Typical path: C:\Users\[YourUsername]\anaconda3\envs\poetry\Scripts
   
   # For macOS/Linux:
   # Add to your ~/.bashrc or ~/.zshrc:
   # export PATH="$HOME/anaconda3/envs/poetry/bin:$PATH"


3. **Create work environment and install dependencies**
   ```bash
   # Create project environment
   conda create -n env_AD_api python=3.11

   # Activate project environment
   conda activate env_AD_api

   # Using Poetry to install project dependencies 
   poetry install --no-root
   ```

## Hardware Requirements

- **Camera**: Intel RealSense D435/D415 or compatible
- **Arduino**: Arduino Uno/Mega with LED circuit (optional)
- **Computer**: not decide

