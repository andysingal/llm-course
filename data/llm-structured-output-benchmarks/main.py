import pickle

import torch
import typer
import yaml
from loguru import logger
from tqdm import tqdm

from frameworks import factory, metrics

app = typer.Typer()


@app.command()
def run_benchmark(config_path: str = "config.yaml"):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"Using device: {device} for local models")
    
    with open(config_path, "r") as file:
        configs = yaml.safe_load(file)

    results = {}
    for config_key, config_values in configs.items():
        results[config_key] = {}

        for config in config_values:
            config_name = config["name"]
            n_runs = config["n_runs"]
            results[config_key][config_name] = {
                "predictions": [],
                "percent_successful": [],
                "accuracy": [],
            }

            framework_instance = factory(
                config_key, name=config_name, device=device, **config["init_kwargs"]
            )
            logger.info(f"Using {type(framework_instance)}")

            for row in tqdm(
                framework_instance.source_data.itertuples(),
                desc=f"Running {framework_instance.name}",
                total=len(framework_instance.source_data),
            ):
                # logger.info(f"Actual Text: {row.text}")
                # logger.info(f"Actual Labels: {set(row.labels)}")
                predictions, percent_successful, accuracy = framework_instance.run(
                    inputs={"text": row.text},
                    n_runs=n_runs,
                    expected_response=set(row.labels),
                )
                # logger.info(f"Predicted Labels: {predictions}")
                results[config_key][config_name]["predictions"].append(predictions)
                results[config_key][config_name]["percent_successful"].append(
                    percent_successful
                )
                results[config_key][config_name]["accuracy"].append(accuracy)

    # logger.info(f"Results:\n{results}")

    with open("results/results.pkl", "wb") as file:
        pickle.dump(results, file)


@app.command()
def generate_results(results_data_pickle_path: str  = "results/results.pkl"):
    with open(results_data_pickle_path, "rb") as file:
        results = pickle.load(file)

    # Reliability
    percent_successful = {   
        framework: value["multilabel_classification"]["percent_successful"]
        for framework, value in results.items()
    }
    logger.info(f"Reliability:\n{metrics.reliability_metric(percent_successful)}")

if __name__ == "__main__":
    app()
