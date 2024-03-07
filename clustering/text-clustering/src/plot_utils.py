import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datasets import load_dataset


def get_size(ds):
    return len([e for i in range(len(ds)) for e in ds[i]["examples"]])


def extract_score(example):
    summary = example["summary"]
    category = summary.split(". Educational")[0].strip()
    score = summary.split(" Educational score: ")[1].strip()
    return {"category": category, "educational_score": score}


def plot_distributions(ds_path, image_path="."):
    """Plot distribution of educational score of topics & distribution of samples accross topics"""
    ds = load_dataset(ds_path, split="train", num_proc=2, token=os.getenv("HF_TOKEN"))
    ds = ds.map(extract_score)
    print(ds["category"])
    ds = ds.filter(lambda x: x["educational_score"] not in ["None", ""])
    # distribution of scores
    df = ds.to_pandas()
    df["educational_score"] = pd.to_numeric(df["educational_score"], errors="coerce")
    df.dropna(subset=["educational_score"], inplace=True)

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.histplot(df["educational_score"], kde=False, bins=10)
    plt.title("Distribution of Educational Scores")
    plt.xlabel("Educational Score")
    plt.ylabel("Frequency")
    plt.savefig(f"{image_path}/educational_score.png", bbox_inches="tight")

    # distribution of samples
    df = ds.to_pandas().explode("examples")
    sorted_filtered_ds = df.groupby(by="category").size().sort_values(ascending=False)
    category_df = sorted_filtered_ds.reset_index()
    category_df.columns = ["category", "number_files"]
    print(f"Saving csv in {image_path}!")
    category_df.to_csv(f"{image_path}/df_categories_count.csv")

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(25, 20))

    barplot = sns.barplot(
        x="number_files", y="category", data=category_df, palette="Blues_d", ci=None
    )

    plt.xlabel("Number of Examples")
    plt.ylabel("Categories")
    plt.title("Histogram of Categories and their number of FW files")
    plt.tight_layout(pad=1.0)
    plt.show()
    plt.savefig(f"{image_path}/topics_distpng", bbox_inches="tight", dpi=200)
