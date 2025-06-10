```py
$ git clone https://github.com/bytedance-seed/BAGEL.git
$ cd BAGEL
$ uv venv --python 3.10
$ source .venv/bin/activate
$ uv pip install -r requirements.txt
$ uv pip install flash_attn --no-build-isolation
```

```py
from huggingface_hub import snapshot_download

save_dir = "models/BAGEL-7B-MoT"
repo_id = "ByteDance-Seed/BAGEL-7B-MoT"
cache_dir = save_dir + "/cache"

snapshot_download(cache_dir=cache_dir,
local_dir=save_dir,
repo_id=repo_id,
local_dir_use_symlinks=False,
resume_download=True,
allow_patterns=["*.json", "*.safetensors", "*.bin", "*.py", "*.md", "*.txt"],
)
```
