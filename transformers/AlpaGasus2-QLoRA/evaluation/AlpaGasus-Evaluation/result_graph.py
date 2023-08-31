import json
import matplotlib.pyplot as plt
%matplotlib inline
import numpy as np
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", type=str)
    parser.add_argument(
        "--output_dir",
        type=str,
        help="The output dir."
    )

    return parser.parse_args()

def result_process(file_path: str):
    nums = [252, 180, 80]   # length of each test set(koala, sinstruct, vicuna)
    test_set = ['sinstruct', 'koala', 'vicuna']
    models = ['alpaca2-alpagasus2-', 'alpagasus2-alpaca2-']
    result_judge = []
    for t in range(len(test_set)):
        number = nums[t]
        res = [0] * number
        result = {'win': 0, 'draw': 0, 'lose': 0}
        for m in range(len(models)):
            path = file_path + models[m] + test_set[t] + '.json'
            with open(path, 'r') as f:
                data = json.load(f)

            for i in range(len(data)):
                if m == 0:
                    alp, alpg = data[i]['score']
                    if int(alpg) > int(alp):
                        res[i] += 1
                    elif int(alpg) < int(alp):
                        res[i] -= 1
                else:
                    alpg, alp = data[i]['score']
                    if int(alpg) > int(alp):
                        res[i] += 1
                    elif int(alpg) < int(alp):
                        res[i] -= 1

        for n in range(len(res)):
            if res[n] >= 1:
                result['win'] += 1
            elif res[n] <= -1:
                result['lose'] += 1
            elif res[n] == 0:
                result['draw'] += 1

        upload = {'test_name': test_set[t]}
        upload.update(result)
        result_judge.append(upload)

    return result_judge

def graph(result_list: list[dict], output_dir: str, watch: bool):
    dataset = ('self-instruct', 'koala', 'vicuna')
    win_draw_lose = {
        'AlpaGasus2_Wins': np.array([0, 0, 0]),
        'Draw': np.array([0, 0, 0]),
        'Alpaca2_Wins': np.array([0, 0, 0]),
    }
    for i in range(len(result_list)):
        win_draw_lose['AlpaGasus2_Wins'][i] = result_list[i]['win']
        win_draw_lose['Draw'][i] = result_list[i]['draw']
        win_draw_lose['Alpaca2_Wins'][i] = result_list[i]['lose']
    
    height = 0.5  # the height of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()
    left = np.zeros(3)

    for judge, judge_count in win_draw_lose.items():
        p = ax.barh(dataset, judge_count, height, label=judge, left=left)
        left += judge_count

        ax.bar_label(p, label_type='center', fontsize=13)

    plt.xticks([])
    ax.set_title('13B: AlpaGasus2 vs Alpaca2')
    ax.legend()

    if watch:
        plt.show()  # watch=True, if you wanted to watch a result graph.
    else:
        output_path = output_dir + 'results.png'
        plt.savefig(output_path)   # watch=False, if you wanted to save a result graph.

def main():
    args = parse_args()

    graph(result_process(args.file_path), args.output_dir, watch=True)

if __name__ == "__main__":
    main()
