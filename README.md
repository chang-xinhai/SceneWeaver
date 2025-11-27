<div align="center">
<img src="docs/images/sceneweaver.png" width="300"></img>
</div>

<h2 align="center">
  <b>SceneWeaver: All-in-One 3D Scene Synthesis with an Extensible and Self-Reflective Agent</b>
</h2>
 <div align="center" margin-bottom="6em">
  <a target="_blank" href="https://yandanyang.github.io/">Yandan Yang</a><sup>✶</sup>,
  <a target="_blank" href="https://buzz-beater.github.io/">Baoxiong Jia</a><sup>✶</sup>,
  <a target="_blank" href="https://hishujie.github.io/">Shujie Zhang</a>,
  <a target="_blank" href="https://siyuanhuang.com/">Siyuan Huang</a>

</div>
<br>
<div align="center">
    <!-- <a href="https://cvpr.thecvf.com/virtual/2023/poster/22552" target="_blank"> -->
    <a href="https://arxiv.org/abs/2509.20414" target="_blank"> 
      <img src="https://img.shields.io/badge/Paper-arXiv-green" alt="Paper arXiv"></a>
    <a href="https://scene-weaver.github.io" target="_blank">
      <img src="https://img.shields.io/badge/Page-SceneWeaver-blue" alt="Project Page"/></a>
</div>
<br>
<div style="text-align: center">
<img src="docs/images/teaser.jpg"  />
</div>


<!-- This is the official repository of [**PhyScene: Physically Interactable 3D Scene Synthesis for Embodied AI**](https://arxiv.org/abs/2211.05272). -->


For more information, please visit our [**project page**](https://scene-weaver.github.io).

## Table of Contents

- [Requirements](#requirements)
- [Quick Start Guide](#quick-start-guide)
- [Installation](#️-installation--dependencies)
- [LLM API Configuration](#-llm-api-configuration)
- [Usage](#usage)
- [Custom Parameters](#custom-parameters)
- [Available Tools](#available-tools)
- [Assets](#-assets)
- [Generated Folder Structure](#generated-folder-structure)
- [Evaluation](#evaluate)
- [Export](#export-to-usd-for-isaac-sim)
- [Citation](#-citation)

## Requirements
- Linux machine
- Conda (Miniconda or Anaconda)
- Python 3.8+ (for planner) / Python 3.10+ (for executor)

## Quick Start Guide

Follow these steps to quickly get SceneWeaver running:

```bash
# 1. Clone the repository
git clone https://github.com/Scene-Weaver/SceneWeaver.git
cd SceneWeaver

# 2. Set up your API key (choose one method)
# Method A: Create key.txt file
echo "your-openrouter-api-key" > Pipeline/key.txt

# Method B: Set environment variable
export OPENROUTER_API_KEY="your-openrouter-api-key"

# 3. Create and activate conda environment
conda env create -n sceneweaver -f environment_sceneweaver.yml
conda activate sceneweaver

# 4. Generate your first scene
cd Pipeline
python main.py --prompt "Design me a bedroom." --cnt 1 --basedir ./output/
```

## ⚙️ Installation & Dependencies

### Step 1: Clone the Repository

```bash
cd ~/workspace  # or your preferred directory
git clone https://github.com/Scene-Weaver/SceneWeaver.git
cd SceneWeaver
```

### Step 2: Set Up LLM API

SceneWeaver supports multiple LLM backends. Choose one of the following:

#### Option A: OpenRouter (Recommended)
OpenRouter provides access to multiple AI models through a single API.

1. Get your API key from [OpenRouter](https://openrouter.ai/)
2. Configure the API key using one of these methods:

```bash
# Method 1: Create key.txt file
echo "your-openrouter-api-key" > Pipeline/key.txt

# Method 2: Set environment variable
export OPENROUTER_API_KEY="your-openrouter-api-key"
```

#### Option B: OpenAI Direct
```bash
# Set environment variables
export LLM_API_TYPE="openai"
export OPENAI_API_KEY="your-openai-api-key"
echo "your-openai-api-key" > Pipeline/key.txt
```

#### Option C: Azure OpenAI
```bash
# Set environment variables
export LLM_API_TYPE="azure"
echo "your-azure-api-key" > Pipeline/key.txt
```

Then update `Pipeline/config/config.json`:
```json
{
    "llm": {
        "api_type": "azure",
        "model": "gpt-4o",
        "base_url": "https://your-azure-endpoint.openai.azure.com/",
        "api_key": "key.txt",
        "max_tokens": 8096,
        "temperature": 0.3,
        "api_version": "2024-02-01"
    }
}
```

### Step 3: Create Conda Environments

#### SceneWeaver's Planner Environment:
```bash
# Create the environment
conda env create -n sceneweaver -f environment_sceneweaver.yml
conda activate sceneweaver
```

#### SceneWeaver's Executor Environment (for Infinigen):
```bash
conda create --name infinigen python=3.10.14
conda activate infinigen

# Install required packages
pip install bpy==3.6.0
pip install gin-config frozendict shapely trimesh tqdm
pip install opencv-python matplotlib imageio scipy
pip install scikit-learn psutil scikit-image submitit
pip install python-fcl pandas geomdl Rtree
```

Then, install Infinigen using one of the options below:
```bash
# Minimal installation (recommended for Blender UI usage)
INFINIGEN_MINIMAL_INSTALL=True bash scripts/install/interactive_blender.sh

# Normal install
bash scripts/install/interactive_blender.sh

# Enable OpenGL GT
INFINIGEN_INSTALL_CUSTOMGT=True bash scripts/install/interactive_blender.sh
```

More details can be found in the [official Infinigen documentation](https://github.com/princeton-vl/infinigen/blob/main/docs/Installation.md#installing-infinigen-as-a-blender-python-script).

## 🔧 LLM API Configuration

The LLM configuration is stored in `Pipeline/config/config.json`. Here's the structure:

```json
{
    "llm": {
        "api_type": "openrouter",
        "model": "openai/gpt-4o",
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": "key.txt",
        "max_tokens": 8096,
        "temperature": 0.3,
        "api_version": ""
    }
}
```

### Configuration Parameters:

| Parameter | Description | Example Values |
|-----------|-------------|----------------|
| `api_type` | LLM provider | `openrouter`, `openai`, `azure` |
| `model` | Model identifier | `openai/gpt-4o`, `openai/gpt-4-turbo`, `anthropic/claude-3-opus` |
| `base_url` | API endpoint | `https://openrouter.ai/api/v1` |
| `api_key` | Path to key file or direct key | `key.txt` |
| `max_tokens` | Maximum response tokens | `8096` |
| `temperature` | Response randomness (0-1) | `0.3` |
| `api_version` | API version (Azure only) | `2024-02-01` |

### Available Models via OpenRouter:

- `openai/gpt-4o` - GPT-4 Omni (recommended)
- `openai/gpt-4-turbo` - GPT-4 Turbo
- `openai/gpt-4o-mini` - GPT-4 Omni Mini (faster, cheaper)
- `anthropic/claude-3-opus` - Claude 3 Opus
- `anthropic/claude-3-sonnet` - Claude 3 Sonnet
- `google/gemini-pro` - Google Gemini Pro

## Usage

### Mode 1: Run with Blender in the Background

```bash
cd Pipeline
conda activate sceneweaver
python main.py --prompt "Design me a bedroom." --cnt 1 --basedir ./output/
```

After completion, check the generated scene in `./output/`. The intermediate scenes from each step are saved in `record_files/`. You can open the `.blend` files in Blender to inspect results.

### Mode 2: Run with Blender in the Foreground (Interactive)

This mode allows you to watch the scene generation in real-time.

**Terminal 1** - Start Infinigen with Blender:
```bash
cd SceneWeaver
conda activate infinigen
python -m infinigen.launch_blender -m infinigen_examples.generate_indoors_vis \
    --save_dir debug/ -- --seed 0 --task coarse --output_folder debug/ \
    -g fast_solve.gin overhead.gin studio.gin \
    -p compose_indoors.terrain_enabled=False
```

**Terminal 2** - Launch SceneWeaver agent:
```bash
cd SceneWeaver/Pipeline
conda activate sceneweaver
python main.py --prompt "Design me a bedroom." --cnt 1 --basedir ./output/ --socket True
```

Watch the scene being built in the Blender window!

## Custom Parameters

### Command Line Arguments

```bash
python main.py [OPTIONS]
```

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--prompt` | str | "Design me a bedroom." | Your scene description |
| `--cnt` | int | 1 | Number of scenes to generate |
| `--basedir` | str | "./output/" | Output directory path |
| `--socket` | str | "False" | Enable Blender foreground mode |

### Example Prompts

```bash
# Simple room types
python main.py --prompt "Design me a living room."
python main.py --prompt "Design me a kitchen."
python main.py --prompt "Design me an office."

# Detailed descriptions
python main.py --prompt "Design me a cozy bedroom with a king-size bed and two nightstands."
python main.py --prompt "Design me a modern living room with a large sofa and coffee table."

# Multiple scenes
python main.py --prompt "Design me a bedroom." --cnt 3 --basedir ./batch_output/
```

### Environment Variables

You can customize SceneWeaver behavior using environment variables:

```bash
# LLM Configuration
export LLM_API_TYPE="openrouter"  # Options: openrouter, openai, azure
export LLM_BASE_URL="https://openrouter.ai/api/v1"
export OPENROUTER_API_KEY="your-api-key"

# Tool Paths (for optional tools)
export TABLETOP_DIGITAL_COUSINS_DIR="~/workspace/Tabletop-Digital-Cousins"
export SD_DIR="~/workspace/sd3.5"
export CONDA_INIT_PATH="$(conda info --base)/etc/profile.d/conda.sh"
```

## Available Tools

SceneWeaver uses a modular tool system. You can customize available tools in `Pipeline/app/agent/scenedesigner.py`.

### Initializer Tools:
- [x] **LLM (GPT)** - Generate initial scene layouts using language models
- [x] **Dataset (MetaScenes)** - Use pre-built scene layouts
- [x] **Model (PhyScene/DiffuScene/ATISS)** - Use ML-generated layouts

### Implementer Tools:
- [x] **Visual (SD + Tabletop Digital Cousin)** - Generate and reconstruct 3D objects
- [x] **LLM** - Add objects using language model suggestions
- [x] **Rule** - Apply rule-based object placement

### Modifier Tools:
- [x] **Update Layout/Rotation/Size** - Adjust object properties
- [x] **Add Relation** - Define spatial relationships
- [x] **Remove Objects** - Clean up unwanted objects

## 🛒 Assets

SceneWeaver supports multiple asset sources:

### MetaScenes
For scene datasets, we use MetaScenes assets directly with mesh and layout information.

### 3D FUTURE
For ML models (PhyScene/DiffuScene/ATISS), download 3D FUTURE from [HuggingFace](https://huggingface.co/datasets/yangyandan/PhyScene/blob/main/dataset/3D-FUTURE-model.zip).

### Infinigen
Procedurally generated assets for common categories (bed, sofa, plate, etc.).

### Objaverse
For unsupported categories (clock, laptop, washing machine), we use Objaverse.

#### Setup OpenShape Pipeline:
1. Build the `idesign` conda env from [IDesign](https://github.com/atcelen/IDesign)
2. Run inference code to download OpenShape
3. Test: `bash SceneWeaver/run/retrieve.sh debug/`

#### Setup Holodeck Pipeline:
1. Build conda env from [Holodeck](https://github.com/allenai/Holodeck)
2. Download required data
3. Update `ABS_PATH_OF_HOLODECK` in `digital_cousins/models/objaverse/constants.py`

## Generated Folder Structure

```
output/
  Scene_Name/                         # folder for each scene
    |-- args/                         # saved args info
    |   └── args_{iter}.json
    |-- pipeline/                     # agent info
    |   |-- acdc_output/              # tabletop scene output
    |   |-- {tool}_results_{iter}.json
    |   |-- eval_iter_{iter}.json
    |   |-- grade_iter_{iter}.json
    |   |-- memory_{iter}.json
    |   |-- metric_{iter}.json
    |   |-- roomtype.txt
    |   └── trajs_{iter}.json
    |-- record_files/                 # intermediate scene files
    |   |-- scene_{iter}.blend
    |   |-- metric_{iter}.json
    |   |-- name_map_{iter}.json
    |   └── *.pkl files
    |-- record_scene/                 # visualizations
    |   |-- layout_{iter}.json
    |   |-- render_{iter}.jpg
    |   |-- render_{iter}_bbox.png
    |   └── render_{iter}_marked.jpg
    |-- args.json
    |-- objav_cnts.json
    |-- objav_files.json
    └── roominfo.json
```

## Evaluate

```bash
python evaluation_ours.py
```

## Export to USD for Isaac Sim

```bash
python -m infinigen.tools.export \
    --input_folder BLENDER_FILE_FOLDER \
    --output_folder USD_SAVE_FOLDER \
    -f usdc -r 1024 --omniverse
```

## 🪧 Citation

If you find our work useful in your research, please consider citing:

```bibtex
@inproceedings{yang2025sceneweaver,
          title={SceneWeaver: All-in-One 3D Scene Synthesis with an Extensible and Self-Reflective Agent},
          author={Yang, Yandan and Jia, Baoxiong and Zhang, Shujie and Huang, Siyuan},
          booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
          year={2025}
        }
```

## 👋🏻 Acknowledgements

The code of this project is adapted from [Infinigen](https://github.com/princeton-vl/infinigen/tree/main). We sincerely thank the authors for open-sourcing their awesome projects. 
