import pandas as pd


def reliability_metric(percent_successful: dict[str, list[float]]):
    df = pd.DataFrame(percent_successful)
    df.columns = [col.replace("Framework", "") for col in df.columns]

    reliability = df.describe().loc["mean", :].to_frame()
    reliability.columns = ["Reliability"]
    reliability.sort_values(by="Reliability", ascending=False, inplace=True)
    return reliability