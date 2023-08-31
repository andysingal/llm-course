import argparse
import json
import os
import time
import openai
from tqdm import tqdm
from typing import Any
import logging

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--API_KEY", type=str)
    parser.add_argument("--model", type=str)
    parser.add_argument("-qa", "--qa_file")
    parser.add_argument("-k1", "--key_1")
    parser.add_argument("-k2", "--key_2")
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=256,
        help="maximum number of tokens produced in the output",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        help="The output dir."
    )

    return parser.parse_args()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def api_generation(
    messages: str,
    model: str,
    temperature: float,
    max_tokens: int,
    top_p: float,
):
    responses = [
        openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )
    ]
    time.sleep(3)   # Preventing rate limits
    return responses

def parse_score(review):
    try:
        score_pair = review.split("\n")[0]
        score_pair = score_pair.replace(",", " ")
        sp = score_pair.split(" ")
        if len(sp) == 2:
            return [float(sp[0]), float(sp[1])]
        else:
            raise Exception("Invalid score pair.")
    except Exception as e:
        logger.error(
            f"{e}\nContent: {review}\n" "You must manually fix the score pair."
        )
        return [-1, -1]


def gen_prompt(ques, ans1, ans2):

    sys_prompt = "You are a helpful and precise assistant for checking the quality of the answer."
    prompt_template = "[Question]\n{question}\n\n[The Start of Assistant 1's Answer]\n{answer_1}\n\n[The End of Assistant 1's Answer]\n\n[The Start of Assistant 2's Answer]\n{answer_2}\n\n[The End of Assistant 2's Answer]\n\n[System]\n{criteria}\n\n"
    criteria = "We would like to request your feedback on the performance of two AI assistants in response to the user question displayed above.\nPlease rate the helpfulness, relevance, accuracy, level of details of their responses. Each assistant receives an overall score on a scale of 1 to 10, where a higher score indicates better overall performance.\nPlease first output a single line containing only two values indicating the scores for Assistant 1 and 2, respectively. The two scores are separated by a space. In the subsequent line, please provide a comprehensive explanation of your evaluation, avoiding any potential bias and ensuring that the order in which the responses were presented does not affect your judgment."
    prompt = prompt_template.format(
        question=ques, answer_1=ans1, answer_2=ans2, criteria=criteria
    )
    return sys_prompt, prompt


def main():
    args = parse_args()

    openai.api_key = args.API_KEY

    qa_jsons = json.load(open(args.qa_file))
    message_list = []
    total_len = len(qa_jsons)
    question_idx_list = list(range(total_len))
    if("vicuna" in args.qa_file):
        prompt_key = 'text'
        dst = 'vicuna' # dst is used for saving the content
    elif("koala" in args.qa_file):
        prompt_key = 'prompt'
        dst = 'koala'
    elif("sinstruct" in args.qa_file):
        prompt_key = 'instruction'
        dst = 'sinstruct'

    for i in question_idx_list:
        instruction = qa_jsons[i][prompt_key]
        if("sinstruct" in args.qa_file):
            instances = qa_jsons[i]['instances']
            assert len(instances) == 1
            if  instances[0]['input']:
                ques = '{instruction} Input: {input}'.format(instruction=instruction,input=instances[0]['input'])
            else:
                ques = instruction
        else:
            ques = instruction


        ans1 = qa_jsons[i][args.key_1]
        ans2 = qa_jsons[i][args.key_2]
        
        sys_prompt, prompt = gen_prompt(ques, ans1, ans2)
        message = [
                    {"role": "system", "content": sys_prompt},
                    {
                        "role": "user",
                        "content": prompt,
                    },
        ]
        message_list.append(message)

    predictions = []
    pbar = tqdm(total=len(message_list))
    for i in range(len(message_list)):
        predictions.append(api_generation(
                messages=message_list[i],
                model=args.model,
                temperature=0.0,
                max_tokens=256,
                top_p=1.0,
            ))
        time.sleep(3)
        pbar.update(1)
    pbar.close()

    output_dir = args.output_dir
    output_review_file = args.key_1 + '-' + args.key_2 + '-' + dst + '.json'
    if os.path.isdir(output_dir) is not True:
        os.mkdir(output_dir)
    output_review_f = os.path.join(output_dir, output_review_file)

    with open(f"{output_review_f}", "x") as f:
        for idx, prediction in enumerate(predictions):
            review = prediction[0]['choices'][0]['message']['content']
            scores = parse_score(review)
            qa_jsons[idx]["review"] = review
            qa_jsons[idx]["score"] = scores
        json.dump(qa_jsons, f, indent=4)

if __name__ == "__main__":
    main()
