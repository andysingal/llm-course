from typing import Dict, Union
from huggingface_hub import get_safetensors_metadata
import argparse
import sys

# Example: 
# python get_gpu_memory.py Qwen/Qwen2.5-7B-Instruct

# Dictionary mapping dtype strings to their byte sizes
bytes_per_dtype: Dict[str, float] = {
    "int4": 0.5,
    "int8": 1,
    "float8": 1,
    "float16": 2,
    "float32": 4,
}


def calculate_gpu_memory(parameters: float, bytes: float) -> float:
    """Calculates the GPU memory required for serving a Large Language Model (LLM).

    This function estimates the GPU memory needed using the formula:
    M = (P * 4B) / (32 / Q) * 1.18

    where:
    - M is the GPU memory in Gigabytes
    - P is the number of parameters in billions (e.g., 7 for a 7B model)
    - 4B represents 4 bytes per parameter
    - 32 represents bits in 4 bytes
    - Q is the quantization bits (e.g., 16, 8, or 4 bits)
    - 1.18 represents ~18% overhead for additional GPU memory requirements

    Args:
        parameters: Number of model parameters in billions
        bytes: Number of bytes per parameter based on dtype

    Returns:
        Estimated GPU memory required in Gigabytes

    Examples:
        >>> calculate_gpu_memory(7, bytes_per_dtype["float16"])
        13.72
        >>> calculate_gpu_memory(13, bytes_per_dtype["int8"])
        12.74
    """
    memory = round((parameters * 4) / (32 / (bytes * 8)) * 1.18, 2)
    return memory


def get_model_size(model_id: str, dtype: str = "float16") -> Union[float, None]:
    """Get the estimated GPU memory requirement for a Hugging Face model.

    Args:
        model_id: Hugging Face model ID (e.g., "facebook/opt-350m")
        dtype: Data type for model loading ("float16", "int8", etc.)

    Returns:
        Estimated GPU memory in GB, or None if estimation fails

    Examples:
        >>> get_model_size("facebook/opt-350m")
        0.82
        >>> get_model_size("meta-llama/Llama-2-7b-hf", dtype="int8")
        6.86
    """
    try:
        if dtype not in bytes_per_dtype:
            raise ValueError(
                f"Unsupported dtype: {dtype}. Supported types: {list(bytes_per_dtype.keys())}"
            )

        metadata = get_safetensors_metadata(model_id)
        if not metadata or not metadata.parameter_count:
            raise ValueError(f"Could not fetch metadata for model: {model_id}")

        model_parameters = list(metadata.parameter_count.values())[0]
        model_parameters = int(model_parameters) / 1_000_000_000  # Convert to billions
        return calculate_gpu_memory(model_parameters, bytes_per_dtype[dtype])

    except Exception as e:
        print(f"Error estimating model size: {str(e)}", file=sys.stderr)
        return None


def main():
    """Command-line interface for GPU memory estimation."""
    parser = argparse.ArgumentParser(
        description="Estimate GPU memory requirements for Hugging Face models"
    )
    parser.add_argument(
        "model_id", help="Hugging Face model ID (e.g., Qwen/Qwen2.5-7B-Instruct)"
    )
    parser.add_argument(
        "--dtype",
        default="float16",
        choices=bytes_per_dtype.keys(),
        help="Data type for model loading",
    )

    args = parser.parse_args()
    size = get_model_size(args.model_id, args.dtype)

    print(
        f"Estimated GPU memory requirement for {args.model_id}: {size:.2f} GB ({args.dtype})"
    )


if __name__ == "__main__":
    main()
