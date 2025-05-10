import torch

# Prints the file path where the installed Torch module is located.
print(f"Torch is installed at: {torch.__file__}")

# Prints the directory where Torch Hub stores cached models.
print(f"Torch Hub directory: {torch.hub.get_dir()}")

import os

# Checks if the Torch Hub cache directory exists and prints the result.
cache_dir = os.path.expanduser("~/.cache/torch/hub")
exists = os.path.exists(cache_dir)
print(f"Does the Torch Hub cache directory exist? {exists} (Expected path: {cache_dir})")
