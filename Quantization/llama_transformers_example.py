import os
import time
import psutil
import random
import torch
import numpy as np
from torch.nn.parameter import Parameter

from transformers import AutoTokenizer, LlamaModel, LlamaForCausalLM, LlamaTokenizer, AutoConfig, AutoModelForCausalLM

# model_dir = "decapoda-research/llama-7b-hf"
model_dir = "/root/project/huggingface/llama-7b-hf/"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def set_random_seed(seed):
    random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)


def test_from_fp16():
    torch.set_printoptions(precision=6, sci_mode=False)
    torch.set_grad_enabled(False)
    set_random_seed(1)

    # model_name = '/root/data/models/2023/llama-13B-v1/'
    model_name = '/home/llama_13B_v1/'
    MAX_NEW_TOKENS = 32

    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    config = AutoConfig.from_pretrained(model_name)
    # config.num_hidden_layers = 1

    free_in_GB = int(torch.cuda.mem_get_info()[0]/1024**3)
    max_memory = f'{int(torch.cuda.mem_get_info()[0]/1024**3)-1}GB'

    n_gpus = torch.cuda.device_count()
    max_memory = {i: max_memory for i in range(n_gpus)}

    model = AutoModelForCausalLM.from_pretrained(model_name, config=config, torch_dtype=torch.float16)
    model.eval()

    from eetq.utils import eet_accelerator
    eet_accelerator(model, quantize=True, fused_attn=True, dev="cuda:0")
    model.to("cuda:0")
    # for k, v in model.state_dict().items():
    #     print(k, v.shape, v.dtype, v.device)
    # torch.save(model, "eetq_llama13B_model_fused_attn_v2.pt")

    text = '中国的首都在'
    kwargs = {
        "input_text": str(text),
        "max_new_tokens": int(MAX_NEW_TOKENS),
        "do_sample": bool(False),
        # "num_beams": 1,
        "temperature": float(0.75),
        "top_k": int(1),
        "top_p": float(0.7),
        "use_cache": bool(True),
    }

    inputs = tokenizer(kwargs["input_text"], return_tensors='pt')
    kwargs["inputs"] = inputs.input_ids.to('cuda:0')

    del kwargs["input_text"]

    # warm up
    generate_ids = model.generate(**kwargs)

    for i in range(1):
        print('i:', i)
        torch.cuda.synchronize()
        t1 = time.perf_counter()
        with torch.no_grad():
            generate_ids = model.generate(**kwargs)
        torch.cuda.synchronize()
        t2 = time.perf_counter()
        print("time:", t2 - t1)

    outputs_str = tokenizer.batch_decode(
        generate_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False)
    print("ori_str", outputs_str)

    print("***********************************")
    max_memory_allocated = torch.cuda.max_memory_allocated() / 1e9
    print('当前进程号: {}, 内存使用：{:.4f} GB'.format(os.getpid(), psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024))
    print("max GPU memory allocated: {:.4f} GB".format(max_memory_allocated))


def test_from_ckpt():
    from accelerate import init_empty_weights, load_checkpoint_and_dispatch
    torch.set_printoptions(precision=6, sci_mode=False)
    torch.set_grad_enabled(False)
    set_random_seed(1)

    model_name = '/root/data/models/2023/llama-13B-v1/'
    MAX_NEW_TOKENS = 32

    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    config = AutoConfig.from_pretrained(model_name)

    free_in_GB = int(torch.cuda.mem_get_info()[0]/1024**3)
    max_memory = f'{int(torch.cuda.mem_get_info()[0]/1024**3)-1}GB'

    n_gpus = torch.cuda.device_count()
    max_memory = {i: max_memory for i in range(n_gpus)}

    with init_empty_weights():
        model = AutoModelForCausalLM.from_pretrained(model_name, config=config, torch_dtype=torch.float16)
    
    from eetq.utils import eet_accelerator
    eet_accelerator(model, quantize=True, fused_attn=False, dev="cuda:0")
    print("***********************************")

    model = load_checkpoint_and_dispatch(model, "llama13B_eetq_dict.pt", device_map="auto", no_split_module_classes=["LlamaDecoderLayer"])
    # model.load_state_dict(torch.load("checkpoint_int8.pt", map_location="cpu"), strict=False)

    model.to("cuda:0")

    text = '中国的首都在'
    kwargs = {
        "input_text": str(text),
        "max_new_tokens": int(MAX_NEW_TOKENS),
        "do_sample": bool(False),
        "num_beams": 2,
        "temperature": float(0.75),
        "top_k": int(1),
        "top_p": float(0.7),
        "use_cache": bool(True),
    }

    inputs = tokenizer(kwargs["input_text"], return_tensors='pt')
    kwargs["inputs"] = inputs.input_ids.to('cuda:0')

    del kwargs["input_text"]

    # warm up
    generate_ids = model.generate(**kwargs)

    for i in range(1):
        # print('i:', i)
        torch.cuda.synchronize()
        t1 = time.perf_counter()
        with torch.no_grad():
            generate_ids = model.generate(**kwargs)
        torch.cuda.synchronize()
        t2 = time.perf_counter()
        print("time:", t2 - t1)

    outputs_str = tokenizer.batch_decode(
        generate_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False)
    print("ori_str", outputs_str)

    print("***********************************")
    max_memory_allocated = torch.cuda.max_memory_allocated() / 1e9
    print('当前进程号: {}, 内存使用：{:.4f} GB'.format(os.getpid(), psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024))
    print("max GPU memory allocated: {:.4f} GB".format(max_memory_allocated))

def test_lora():
    torch.set_printoptions(precision=6, sci_mode=False)
    torch.set_grad_enabled(False)
    set_random_seed(1)

    # model_name = '/root/data/models/2023/llama-13B-v1/'
    model_name = "/home/llama_13B_v1"
    MAX_NEW_TOKENS = 32

    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    config = AutoConfig.from_pretrained(model_name)
    # config.num_hidden_layers = 1

    model = AutoModelForCausalLM.from_pretrained(model_name, config=config, torch_dtype=torch.float16)
    model.eval()

    from eetq.utils import eet_accelerator
    from peft import PeftConfig, PeftModel, get_peft_model, LoraConfig, TaskType
    # lora
    lora_rank = 8
    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM, inference_mode=True,
        peft_type="LORA",
        r=lora_rank,
        target_modules=["q_proj", "k_proj", "v_proj"],
        lora_alpha=32, lora_dropout=0.1
    )
    model = get_peft_model(model, peft_config)
    # print(model)
    model = model.merge_and_unload()

    import peft.tuners.lora as lora
    eet_accelerator(model, quantize=True, fused_attn=False, dev="cuda:0")
    model.to("cuda:0")


    text = '中国的首都在'
    kwargs = {
        "input_text": str(text),
        "max_new_tokens": int(MAX_NEW_TOKENS),
        "do_sample": bool(False),
        # "num_beams": 1,
        "temperature": float(0.75),
        "top_k": int(1),
        "top_p": float(0.7),
        "use_cache": bool(True),
    }

    inputs = tokenizer(kwargs["input_text"], return_tensors='pt')
    kwargs["inputs"] = inputs.input_ids.to('cuda:0')

    del kwargs["input_text"]

    # warm up
    generate_ids = model.generate(**kwargs)

    for i in range(1):
        print('i:', i)
        torch.cuda.synchronize()
        t1 = time.perf_counter()
        with torch.no_grad():
            generate_ids = model.generate(**kwargs)
        torch.cuda.synchronize()
        t2 = time.perf_counter()
        print("time:", t2 - t1)

    outputs_str = tokenizer.batch_decode(
        generate_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False)
    print("ori_str", outputs_str)

    # save
    # torch.save(model, "eetq_llama13B_model.pt")

    print("***********************************")
    max_memory_allocated = torch.cuda.max_memory_allocated() / 1e9
    print('当前进程号: {}, 内存使用：{:.4f} GB'.format(os.getpid(), psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024))
    print("max GPU memory allocated: {:.4f} GB".format(max_memory_allocated))    

def test_load():
    torch.set_printoptions(precision=6, sci_mode=False)
    torch.set_grad_enabled(False)
    set_random_seed(1)

    model_name = '/root/data/models/2023/llama-13B-v1/'
    #model_name = "/home/llama_13B_v1"
    MAX_NEW_TOKENS = 32

    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    config = AutoConfig.from_pretrained(model_name)

    from eetq.utils import eet_accelerator
    # from peft import PeftConfig, PeftModel, get_peft_model, LoraConfig, TaskType

    model = torch.load("eetq_llama13B_model_fused_attn_v2.pt", map_location="cuda:0")
    # model = torch.load("eetq_llama13B_model.pt",map_location="cuda:0")
    # model = torch.load("/project/tgi_0907/text-generation-inference/model_llama7b.pt", map_location="auto")

    model.to("cuda:0")

    text = '中国的首都在'
    kwargs = {
        "input_text": str(text),
        "max_new_tokens": int(MAX_NEW_TOKENS),
        "do_sample": bool(False),
        # "num_beams": 2,
        "temperature": float(0.75),
        "top_k": int(1),
        "top_p": float(0.7),
        "use_cache": bool(True),
    }

    inputs = tokenizer(kwargs["input_text"], return_tensors='pt')
    kwargs["inputs"] = inputs.input_ids.to('cuda:0')

    del kwargs["input_text"]

    # warm up
    generate_ids = model.generate(**kwargs)

    for i in range(1):
        print('i:', i)
        torch.cuda.synchronize()
        t1 = time.perf_counter()
        with torch.no_grad():
            generate_ids = model.generate(**kwargs)
        torch.cuda.synchronize()
        t2 = time.perf_counter()
        print("time:", t2 - t1)

    outputs_str = tokenizer.batch_decode(
        generate_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False)
    print("ori_str", outputs_str)


    print("***********************************")
    max_memory_allocated = torch.cuda.max_memory_allocated() / 1e9
    print('当前进程号: {}, 内存使用：{:.4f} GB'.format(os.getpid(), psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024))
    print("max GPU memory allocated: {:.4f} GB".format(max_memory_allocated))        

if __name__ == "__main__":
    # test_from_fp16()
    # test_from_ckpt()
    # test_lora()
    test_load()
