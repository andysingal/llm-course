```py
# version_checker.py
import sys
import pkg_resources
from packaging import version

# Known compatible version combinations
COMPATIBLE_VERSIONS = {
    "0.20.0": {"transformers": ["4.30.0", "4.33.3"]},
    "0.25.0": {"transformers": ["4.36.0", "4.37.2"]},
    "0.26.0": {"transformers": ["4.38.0", "4.39.3"]},
    "0.27.0": {"transformers": ["4.40.0", "4.41.2"]},
}

def check_compatibility():
    """Check version compatibility"""
    try:
        diffusers_ver = pkg_resources.get_distribution("diffusers").version
        transformers_ver = pkg_resources.get_distribution("transformers").version
        
        print(f"✅ diffusers: {diffusers_ver}")
        print(f"✅ transformers: {transformers_ver}")
        
        # Get major and minor version
        diff_major_minor = ".".join(diffusers_ver.split(".")[:2])
        
        if diff_major_minor in COMPATIBLE_VERSIONS:
            compatible_transforms = COMPATIBLE_VERSIONS[diff_major_minor]["transformers"]
            
            # Check version range
            trans_ver = version.parse(transformers_ver)
            min_ver = version.parse(compatible_transforms[0])
            max_ver = version.parse(compatible_transforms[-1])
            
            if min_ver <= trans_ver <= max_ver:
                print(f"✅ Compatibility: OK")
                return True
            else:
                print(f"⚠️  Warning: transformers version is outside the recommended range")
                print(f"   Recommended: {compatible_transforms[0]} - {compatible_transforms[-1]}")
                print(f"   Current: {transformers_ver}")
                return False
        else:
            print(f"⚠️  Warning: No compatibility information for diffusers {diffusers_ver}")
            return False
            
    except pkg_resources.DistributionNotFound as e:
        print(f"❌ Error: {e.req} is not installed")
        sys.exit(1)

def get_recommended_versions():
    """Return recommended versions"""
    return {
        "stable": {
            "diffusers": "0.25.0",
            "transformers": "4.36.2",
            "accelerate": "0.25.0",
        },
        "latest": {
            "diffusers": "0.27.0",
            "transformers": "4.41.0",
            "accelerate": "0.28.0",
        }
    }

if __name__ == "__main__":
    print("="*50)
    print("Version Compatibility Check")
    print("="*50)
    
    if not check_compatibility():
        print("\nRecommended versions:")
        versions = get_recommended_versions()
        
        print("\nStable:")
        for pkg, ver in versions["stable"].items():
            print(f"  {pkg}=={ver}")
        
        print("\nLatest:")
        for pkg, ver in versions["latest"].items():
            print(f"  {pkg}=={ver}")
        
        print("\nExample install command:")
        stable = versions["stable"]
        print(f"  pip install diffusers=={stable['diffusers']} "
              f"transformers=={stable['transformers']} "
              f"accelerate=={stable['accelerate']}")
```

## How to use

```py
# main.py
from version_checker import check_compatibility

# Compatibility check
if not check_compatibility():
    print("Warning: A version compatibility issue has been detected")
    # Decide whether to continue

# Main code
import diffusers
import transformers
# ...
```


## Source
[source1](https://qiita.com/oggata/items/859af289b28cc7d2a02b)
