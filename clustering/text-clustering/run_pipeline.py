import argparse
import textwrap
import time

import numpy as np
import pandas as pd
from datasets import Dataset, load_dataset

from src.plot_utils import plot_distributions
from src.text_clustering import ClusterClassifier

INSTRUCTION_SINGLE_TOPIC = "The examples below are web samples from the same cluster, identify the topic they have in common, for example: Philosophy, Lifesyle, Linear Algebra, Biochemistry, Economics...\
Additionally determine if the topics in the examples \
are broadly suitable as college/school material, while being mindful to exclude any sensitive/inappropriate/irrelevant content, \
including but not limited to sex, explicit violence, ads & scams, and other non-academic subjects. Consider a wide range of content including scientific, \
educational, historical, cultural, and practical applications and give a rating of how educational these topics could be from 1 to 10, 1 being extremely un-educational \
and inapproriate for an education setting and 10 being highly educational. The output format should be like this: Topic: the_topic, Educational value rating: score."
INSTRUCTION_MULTIPLE_TOPICS = "Use three words total (comma separated)\
to describe general topics in above texts. Under no circumstances use enumeration. \
Example format: Tree, Cat, Fireman"


TEMPLATE_MULTIPLE_TOPICS = "<s>[INST]{examples}\n\n{instruction}[/INST]"
TEMPLATE_SINGLE_TOPIC = "<s>[INST]{instruction}\n\nExamples:\n{examples}\nRemember that the output format should be like this: Topic: the_topic, Educational value rating: score.[/INST]"


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_samples", type=int, default=100_000)
    parser.add_argument("--start", type=int, default=-1)
    parser.add_argument("--end", type=int, default=100_000)
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--save_load_path", type=str, default="./cc_100k")
    parser.add_argument(
        "--input_dataset",
        type=str,
        default="HuggingFaceFW/FW-12-12-2023-CC-2023-06",
        help="dataset with the samples to use for clustering",
    )
    parser.add_argument(
        "--data_subset",
        type=str,
        default=None,
        help="dataset subset",
    )
    parser.add_argument("--input_content", type=str, default="content")
    parser.add_argument(
        "--topic_mode",
        type=str,
        choices=["single_topic", "multiple_topics"],
        default="multiple_topics",
        help="Specify 'single_topic' to generate only one topic and score its educational value, or 'multiple_topics' to generate the 3 most relevant topics in the cluster.",
    )
    parser.add_argument(
        "--dbscan_eps",
        type=float,
        default=0.08,
        help="The maximum distance between two samples for them to be considered as in the neighborhood of each other.",
    )
    parser.add_argument(
        "--dbscan_min_samples",
        type=int,
        default=50,
        help="The number of samples in a neighborhood for a point to be considered as a core point.",
    )
    parser.add_argument(
        "--mode",
        choices=["run", "load", "infer"],
        default="run",
        help="Run the pipeline from scratch/load existing model to build hf datasets or to infer on new texts",
    )
    parser.add_argument(
        "--inference_repo_name",
        type=str,
        default="infer_fw_on_ultrachat",
        help="HF repo name for the clusters dataset in inference mode",
    )
    parser.add_argument(
        "--build_hf_ds",
        action="store_true",
        help="Builds HF datasets used for space visualization and pushes them to the hub",
    )
    parser.add_argument("--username", type=str, default="loubnabnl")
    return parser.parse_args()


def extract_res(example):
    summary = example["summary"]
    category = summary.split(". Educational")[0].strip()
    score = summary.split(" Educational score: ")[1].strip()
    return {"category": category, "educational_score": score}


def build_hf_data_clusters(cc, texts=None, labels=None):
    """
    Build an HF dataset containing information on each cluster.

    Args:
        cc: ClusterClassifier object.
        texts: list of texts used for inference mode.
        labels: list of cluster labels corresponding to the texts for inference mode.

    If `texts` and `labels` are not provided, the function will use the data available in `cc`
    to construct the dataset. Otherwise it will run in inference mode on texts.
    """
    cluster_data = []
    for cluster_id in cc.label2docs.keys():
        if cluster_id == -1:
            continue

        # inference mode
        if texts is not None and labels is not None:
            labels_array = np.array(labels)
            files_in_cluster = np.where(labels_array == cluster_id)[0]
            examples = [texts[doc_id] for doc_id in files_in_cluster]
        else:
            doc_ids = cc.label2docs[cluster_id]
            examples = [cc.texts[doc_id] for doc_id in doc_ids]

        cluster_info = {
            "cluster_id": cluster_id,
            "summary": cc.cluster_summaries[cluster_id],
            "examples": examples,
        }

        if not texts:
            cluster_info["position"] = cc.cluster_centers[cluster_id]

        cluster_data.append(cluster_info)

    return Dataset.from_pandas(pd.DataFrame(cluster_data))


def build_hf_data_files(cc):
    """
    Build an HF dataset containing information on each file and the cluster they belong to
    """

    df = pd.DataFrame(
        data={
            "X": cc.projections[:, 0],
            "Y": cc.projections[:, 1],
            "labels": cc.cluster_labels,
            "content_display": [textwrap.fill(txt[:1024], 64) for txt in cc.texts],
        }
    )
    return Dataset.from_pandas(df)


def build_and_push(cc, args):
    """Build HF files & clusters datasts and push them to the hub"""
    print("Building HF datasets...")
    ds = build_hf_data_clusters(cc)
    ds = ds.map(extract_res)
    data_clusters = build_hf_data_files(cc)
    print(f"Files dataset {ds}\nClusters dataset {data_clusters}")

    repo_name = args.save_load_path.split("/")[-1]
    print(f"Pushing to the hub at {repo_name}...")
    ds.push_to_hub(f"{args.username}/{repo_name}", private=True)
    data_clusters.push_to_hub(f"{args.username}/{repo_name}_clusters", private=True)


def main():
    args = get_args()

    template = (
        TEMPLATE_MULTIPLE_TOPICS
        if args.topic_mode == "multiple_topics"
        else TEMPLATE_SINGLE_TOPIC
    )
    instruction = (
        INSTRUCTION_MULTIPLE_TOPICS
        if args.topic_mode == "multiple_topics"
        else INSTRUCTION_SINGLE_TOPIC
    )
    print(f"Using {args.topic_mode} for topic labeling")
    cc = ClusterClassifier(
        embed_device=args.device,
        topic_mode=args.topic_mode,
        summary_template=template,
        summary_instruction=instruction,
        dbscan_eps=args.dbscan_eps,
        dbscan_min_samples=args.dbscan_min_samples,
    )

    if args.mode == "run":
        # Run a new pipeline on texts
        dataset_args = (args.input_dataset, args.data_subset) if args.data_subset else (args.input_dataset,)
        ds = load_dataset(*dataset_args, split="train", token=True).shuffle(
            seed=42
        )

        print(ds)
        indexes = (
            range(args.start, args.end) if args.start > 0 else range(args.n_samples)
        )
        text_start = f" starting from {args.start}" if args.start > 0 else ""
        print(f"Processing {len(indexes)} samples{text_start}")

        texts = ds.select(indexes)[args.input_content]

        _, _, summaries = cc.fit(texts)
        print(f"10 example Summaries:\n{[e for e in summaries.values()][:10]}")

        cc.save(args.save_load_path)
        print(f"Saved clusters in {args.save_load_path}.")

        if args.build_hf_ds:
            build_and_push(cc, args)

        ds_path = f"{args.username}/{args.save_load_path.split('/')[-1]}"
        if args.topic_mode == "single_topic":
            plot_distributions(ds_path, image_path=args.save_load_path)
            print("📊 Saved plots for educational score and files distribution.")

    elif args.mode == "infer":
        # Run inference mode on texts using an existing pipeline
        cc.load(args.save_load_path)
        indexes = (
            range(args.start, args.end) if args.start >= 0 else range(args.n_samples)
        )
        text_start = f" starting from {args.start}" if args.start >= 0 else ""
        print(
            f"Running inference on {len(indexes)} samples{text_start} of {args.input_dataset} using clusters in {args.save_load_path}."
        )
        dataset_args = (args.input_dataset, args.data_subset) if args.data_subset else (args.input_dataset,)
        ds = load_dataset(*dataset_args, split="train", token=True)
        texts = ds.select(indexes)[args.input_content]

        start_time = time.time()
        cluster_labels, _ = cc.infer(texts, top_k=1)

        ds = build_hf_data_clusters(cc, texts, cluster_labels)
        print(f"Total time is {(time.time() - start_time)/60}min")
        target_repo = f"{args.username}/{args.inference_repo_name}"
        print(f"Samples with clusters: {ds}")
        print(f"Pushing to hub at {target_repo}...")
        ds.push_to_hub(f"{target_repo}", private=True)

    else:
        # Load existing pipeline
        if args.build_hf_ds:
            cc.load(args.save_load_path)
            build_and_push(cc, args)
            ds_path = f"{args.username}/{args.save_load_path.split('/')[-1]}"
            if args.topic_mode == "single_topic":
                plot_distributions(ds_path, image_path=args.save_load_path)
                print("📊 Saved plots for educational score and files distribution.")
        else:
            print("Using mode=load but build_hf_ds is False, nothing to be done.")

    print("Done 🎉")


if __name__ == "__main__":
    main()
