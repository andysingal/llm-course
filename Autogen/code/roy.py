import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import sys
import torch
from transformers import AutoModelForCausalLM, AutoModel, AutoTokenizer
from huggingface_hub import hf_hub_download
import faiss
import pandas as pd
from textwrap import indent, dedent
import re
import subprocess
import shlex
import venv
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from pygments.lexers.python import Python3Lexer
import argparse
import sys
from tqdm.auto import tqdm

DEBUG = True

def print_color(s, c=1):
    if DEBUG is True:
        print(f'\033[{31+c}m{s}\033[0m')

def trace_method(func):
    def wrapper(*args, **kwargs):
        input_str = args[0] if isinstance(args[0], str) else args[1]
        print_color(f"{func.__name__}() receives:\n{indent(input_str, '    ')}", 4)
        result = func(*args, **kwargs)
        if isinstance(result, str):
            print_color(f"{func.__name__}() returns:\n{indent(result, '    ')}", 3)
        else:
            print_color(f"{func.__name__}() returns an object of type: {type(result)}", 3)
        return result
    return wrapper
        
def extract_code_block(text_w_code, join_all = True):
    pattern = r'```(?:\s*(\w+?)\s*\n)?(.*?)```'
    matches = re.findall(pattern, text_w_code, re.DOTALL)
    if len(matches) < 1:
        return ''
    codes = [i[1] for i in matches]
    if join_all:
        code = '\n\n'.join(codes)
    else:
        code = codes[-1]
    return code
    
def trim_str(row, char_limit, variable_str, constant_str):
    if not (isinstance(row[variable_str], str) and isinstance(row[constant_str], str)):
        return ""
    if len(row[constant_str]) >= char_limit:
        return ""
    trimmed_length = char_limit - len(row[constant_str])
    return row[variable_str][:trimmed_length]

def process_markdown_data(df):
    df = df[~df['filepath'].str.contains('/zh/')]
    df['filepath'] = df['filepath'].str[7:]
    df['content'] = df['content'].str[:5000]
    df['retrieved_content'] = df.apply(lambda row: f"{row['filepath'].split('/')[-1]} ({row['filepath']}):\n'''\n{row['content']}...\n'''", axis=1)
    return df

def process_docstr_data(df):
    df = df[df['docstring'].str.contains('```')]
    df = df[~df['filepath'].apply(lambda x: x.split('/')[-1]).str.startswith('TF')]
    df.reset_index(drop=True, inplace=True)
    df['filepath'] = df['filepath'].str[7:].str.rstrip('/.')
    df['root_dir'] = df['filepath'].apply(lambda x: x.split('/')[0])
    df['retrieved_code'] = df['docstring'].apply(extract_code_block)
    df['docstring'] = df.apply(trim_str, args=(5000,'docstring','retrieved_code'), axis=1)
    df['retrieved_docstr'] = df.apply(lambda row: f"{row['type']} `{row['filepath'].split('/')[-1]}` ({row['filepath']}):\n'''\n{row['docstring']}...\n'''", axis=1)
    return df

def process_string(s):
    if '>>>' not in s:
        return s

    def replace_line_prefix(match):
        prefix = match.group(1)
        if prefix in [">>> ", "... "]:
            return ""
        return "# " + match.group(0)
    
    pattern = r"^(>>> |... |\S+.*$)"
    return re.sub(pattern, replace_line_prefix, s, flags=re.MULTILINE)

def edit_code_in_terminal(initial_text):
    kb = KeyBindings()
    result = {'text': initial_text}

    @kb.add('s-tab')
    def _(event):
        result['text'] = event.app.current_buffer.text
        event.app.exit()

    style = Style.from_dict({
        '': '#ffad00',
        'prompt': 'bg:#ff0000 #ffff00',
    })

    session = PromptSession(lexer=PygmentsLexer(Python3Lexer), key_bindings=kb, style=style)
    session.prompt('\n--- Press shift+tab when done ---\n', multiline=True, default=initial_text)
    
    result_text = result['text']

    return result_text

default_config_for_RM = {
    'markdown': {
        'filename_key': 'hfmd_20230927192215',
        'process_data': process_markdown_data
    },
    'huggingface': {
        'filename_key': 'hfds_20230927191331',
        'process_data': process_docstr_data
    },
}

class VirtualEnvironment:
    def __init__(self, venv_path='venv4gen'):
        self.venv_path = venv_path
        try:
            if not os.path.exists(self.venv_path):
                venv.EnvBuilder(with_pip=True).create(self.venv_path)
            if os.name == 'nt':
                self.python_executable = os.path.join(venv_path, "Scripts", "python.exe")
                self.pip_executable = os.path.join(venv_path, "Scripts", "pip.exe")
            else:
                self.python_executable = os.path.join(venv_path, "bin", "python")
                self.pip_executable = os.path.join(venv_path, "bin", "pip")
        except:
            print("Warning: Failed to create or locate virtual environment. Using default system python and pip.")
            self.python_executable = "python"
            self.pip_executable = "pip"

    def _run_sh(self, command):
        replacements = {
            "python": self.python_executable,
            "pip": self.pip_executable,
            "pip3": self.pip_executable,
        }
        command_parts = shlex.split(command)
        command_parts = [replacements.get(part, part) for part in command_parts]
        adjusted_command = ' '.join(shlex.quote(part) for part in command_parts)

        try:
            output = subprocess.run(
                adjusted_command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            ).stdout.decode()
        except subprocess.CalledProcessError as error:
            output = str(error.stdout.decode()).strip()
        return output
    
    def _run_py(self, code_string, script_name="script.py"):
        lines_with_exclamation = re.findall(r'^!(.*)$', code_string, re.MULTILINE)
        code_string = re.sub(r'^(!)', r'#\1', code_string, flags=re.MULTILINE)
        with open(script_name, 'w') as f:
            f.write(code_string)
        lines_with_exclamation.append(f"python {script_name}")
        return '\n' +  '\n'.join([self._run_sh(s) for s in lines_with_exclamation]) + '\n'
    
    def execute(self, code_string, is_python=True):
        code_string = extract_code_block(code_string)
        if is_python is True:
            return self._run_py(code_string)
        return '\n' + '\n'.join([self._run_sh(s) for s in code_string.splitlines()]) + '\n'
        
class RM:
    def __init__(self, configs=default_config_for_RM, model_id="BAAI/bge-small-en", query_instruction='Represent this sentence for searching relevant passages: '):
        self.configs = configs
        self.resources = {}
        for src, config in self.configs.items():
            self._init_filenames(src)
            self._load_resources(src)
        self._init_model(model_id, query_instruction) 

    def _init_filenames(self, src):
        config = self.configs[src]
        filename_key = config['filename_key']
        fn_index = f'index_{filename_key}.index'
        fn_df = f'df_{filename_key}.csv'
        self.resources[src] = {
            "fn_index": fn_index,
            "fn_df": fn_df
        }

    def _load_resources(self, src):
        res = self.resources[src]
        for fn_i in [res["fn_index"], res["fn_df"]]:
            hf_hub_download(
                repo_id="Accede/vecDB",
                filename=fn_i,
                repo_type='dataset',
                local_dir='.'
            )
        res["index"] = faiss.read_index(res["fn_index"])
        res["df"] = pd.read_csv(res["fn_df"])

    def _init_model(self, model_id, query_instruction):
        self.QUERY_INST = query_instruction
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModel.from_pretrained(model_id, device_map='cpu')
        self.device = torch.device('cpu')
        self.model.to(self.device)
        self.model.eval()
        
    @torch.no_grad()
    def _encode_queries(self, queries):
        query_formatted = [self.QUERY_INST + queries] if isinstance(queries, str) else ['{}{}'.format(self.QUERY_INST, q) for q in queries]
        query_tokenized = self.tokenizer(query_formatted, padding=True, truncation=True, return_tensors='pt').to(self.device)
        last_hidden_states = self.model(**query_tokenized, return_dict=True).last_hidden_state
        embeddings = last_hidden_states[:, 0, :]
        embeddings = torch.nn.functional.normalize(embeddings, dim=-1)
        return embeddings.cpu().numpy()
    
    def retrieve(self, user_request, n_topk=3, src='huggingface'):
        config = self.configs[src]
        res = self.resources[src]
        index = res["index"]
        df = res["df"]
        q_embeddings = self._encode_queries([user_request])
        scores, indices = index.search(q_embeddings, n_topk*30)
        df_topk = df.iloc[indices[0]]
        process_func = config.get('process_data')
        if process_func:
            df_topk = process_func(df_topk)
        df_topk = df_topk.iloc[:n_topk]
        df_topk['user_request'] = user_request
        return df_topk.reset_index(drop=True)

class LM:
    def __init__(self, model_id = 'TheBloke/WizardCoder-Python-7B-V1.0-GPTQ'):
        self.model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto", revision="main")
        self.model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)

    @torch.no_grad()
    def _beam(self, input_txt, root_kv=None, result_kv_fn=None, max_new_tokens=300, num_beams=3, save_kv=False, pass_token = []):
        if root_kv is None:
            perInput_input_ids = self.tokenizer(input_txt, add_special_tokens=True, return_tensors='pt').input_ids.to(self.model.device)
            perInput_output_tokens = []
        else:
            perInput_input_ids = self.tokenizer(input_txt, add_special_tokens=False, return_tensors='pt').input_ids[:, 1:].to(self.model.device)
            perInput_output_tokens = perInput_input_ids[0].tolist()
        perInput_key_values = self.model(perInput_input_ids, use_cache=True, past_key_values=root_kv).past_key_values
        beams = [(perInput_input_ids, perInput_output_tokens, 0.0, perInput_key_values)]
        best_cc = (None, None, float('-inf'), None)
        for i in range(max_new_tokens):
            new_beams = []
            for beam in beams:
                beam_input_ids, beam_output_tokens, beam_score, beam_kv = beam
                _new_outputs = self.model(beam_input_ids[:, -1:], use_cache=True, past_key_values=beam_kv)
                _new_logits = _new_outputs.logits[:, -1, :]
                new_kv = _new_outputs.past_key_values
                topk = torch.topk(_new_logits, num_beams)
                for next_token_id, next_score in zip(topk.indices[0], topk.values[0]):
                    if next_token_id in pass_token:
                        continue
                    new_input_ids = torch.cat((beam_input_ids, next_token_id.unsqueeze(0).unsqueeze(0)), dim=1)
                    new_output_tokens = beam_output_tokens + [next_token_id.item()]
                    new_score = ((beam_score * len(beam_output_tokens)) + next_score.item()) / len(new_output_tokens)

                    if next_token_id == self.tokenizer.eos_token_id:
                        if sum(token_id_i in {28956, 7521} for token_id_i in beam_output_tokens) % 2 == 0:
                            if new_score > best_cc[2]:
                                best_cc = (beam_input_ids, beam_output_tokens, new_score, beam_kv)
                    else:
                        if (new_output_tokens[-3:] != [13]*3) and (new_output_tokens[-4:] != [13, 30004, 13, 13]) and (new_output_tokens[-4:] != [13, 30004, 13, 30004]):
                            new_beam = (new_input_ids, new_output_tokens, new_score, new_kv)
                            new_beams.append(new_beam)
                            new_beams = sorted(new_beams, key=lambda x: x[2], reverse=True)[:num_beams]
            beams = new_beams
            if best_cc[2] > beams[0][2]:
                break

        best_beam = max([best_cc]+beams, key=lambda x: x[2])
        decoded_output = self.tokenizer.decode(best_beam[1])
        if save_kv is True:
            torch.save(best_beam[3], result_kv_fn)
        return decoded_output

    @torch.no_grad()
    def _greedy(self, input_txt, past_kv, max_new_tokens=300, until=[28956, 7521]):
        input_ids = self.tokenizer(input_txt, add_special_tokens=False, return_tensors='pt').input_ids.to(self.model.device)
        next_token_id = input_ids[:,-1:]
        generated_tokens = []
        for _ in range(max_new_tokens):
            outputs = self.model(next_token_id, past_key_values=past_kv)
            next_token_id = outputs.logits[:, -1, :].argmax(dim=1)
            past_kv = outputs.past_key_values
            next_token_id = next_token_id.unsqueeze(0)
            next_token_id_item = next_token_id.item()
            generated_tokens.append(next_token_id_item)
            if next_token_id_item in until:
                break
        decoded_output = self.tokenizer.decode(generated_tokens)
        return decoded_output
    
    @torch.no_grad()
    def generate(self, input_txt):
        o_beam = self._beam(input_txt, result_kv_fn = 'tmp_kv', save_kv=True, max_new_tokens=500)
        torch.cuda.empty_cache()
        if o_beam.count('```') == 0:
            o_open = self._beam('\n```', root_kv=torch.load('tmp_kv'), result_kv_fn = 'tmp_kv', save_kv=True, max_new_tokens=400)
            torch.cuda.empty_cache()
            o_beam += o_open
        if o_beam.count('```') % 2 != 0:
            o_close = self._greedy(o_beam, torch.load('tmp_kv'), until=[28956, 7521])
            torch.cuda.empty_cache()
            o_beam += o_close
        o_beam = o_beam.replace('\r', '')
        return o_beam
    
class Roy:
    def __init__(self, config=None):
        if config is None:
            config = {}
            
        self.template = config.get('template', "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{instruction}\n\n### Response:")
        
        self._venv = None
        self._lm = None
        self._rm = None

        self.execute = trace_method(config.get('execute', self.venv.execute))
        self.generate = trace_method(config.get('generate', self.lm.generate))
        self.retrieve = trace_method(config.get('retrieve', self.rm.retrieve))

    @property
    def venv(self):
        if self._venv is None:
            self._venv = VirtualEnvironment()
        return self._venv

    @property
    def lm(self):
        if self._lm is None:
            self._lm = LM()
        return self._lm

    @property
    def rm(self):
        if self._rm is None:
            self._rm = RM()
        return self._rm

    @trace_method
    def format(self, instruction, data={}):
        template = self.template.format(instruction=instruction)
        if isinstance(data, pd.DataFrame):
            return data.apply(lambda row: template.format(**row), axis=1).tolist()
        elif isinstance(data, (dict, pd.Series)):
            return template.format(**data)
        else:
            raise ValueError("Unsupported data type. Data must be a dict, Series, or DataFrame.")
