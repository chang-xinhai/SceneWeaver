#!/usr/bin/env python3

import sys
print("Python executable:", sys.executable)
print("Python path:", sys.path[:3], "...")  # Show first 3 paths

try:
    import landlab
    print("✅ landlab imported successfully!")
    print("landlab version:", landlab.__version__)
    print("landlab location:", landlab.__file__)
except ImportError as e:
    print("❌ Failed to import landlab:", e)
    
try:
    import conda
    print("✅ conda module available")
except ImportError:
    print("❌ conda module not available")

# Check if we're in conda environment
import os
if 'CONDA_DEFAULT_ENV' in os.environ:
    print(f"✅ Conda environment: {os.environ['CONDA_DEFAULT_ENV']}")
else:
    print("❌ Not in conda environment") 