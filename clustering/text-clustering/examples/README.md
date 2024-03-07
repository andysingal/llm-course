# Examples

## Cosmopedia experiments: clustering of web samples

Here you can find the commands we used during the selection of web samples for [Cosmopedia](https://huggingface.co/datasets/HuggingFaceTB/cosmopedia) prompts. 

Our goal was to find the topics in random web samples and their educational score. The topics were used in the creation of prompts for synthetic data generation and helped us understand the range of domains covered. Initially, we clustered **100,000 samples**, yielding **145 clusters**. Then we assigned **15 million samples** to these clusters using the inference mode of `text-clustering`; however, half of them did not fit into any cluster and were excluded from prompt creation.

For illustration, we will use  [AutoMathText](https://huggingface.co/datasets/math-ai/AutoMathText) here. In Cosmopedia we used samples from a web dataset like [RefineWeb](https://huggingface.co/datasets/tiiuae/falcon-refinedweb). 

We will run the clustering using `topic_mode` single with educational scores. This pipeline clusters files and prompts an LLM (by default [Mixtral-8x7B-Instruct-v0.1](https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1)) to find the topic of each cluster and give it an educational score. We plot the distribution of samples over topics and the distribution of the educational score and save the plots in the `save_load_path` folder. 

```bash
python run_pipeline.py --mode run \
  --save_load_path './web_samples_100k' \
  --input_dataset math-ai/AutoMathText \
  --data_subset "web-0.70-to-1.00" \
  --input_content text \
  --n_samples 100000 \
  --build_hf_ds \
  --topic_mode single_topic \
  --dbscan_eps 0.08 \
  --dbscan_min_samples 50
```


This detects 213 clusters that you can visualize in this [plot](https://huggingface.co/datasets/HuggingFaceTB/miscellaneous/blob/main/AMT_plots/topics_distpng.png) along with the [educational scores](https://huggingface.co/datasets/HuggingFaceTB/miscellaneous/blob/main/AMT_plots/educational_score.png) which is very high for this AutoMathText dataset.

When using general web datasets, you might want to filter out files with a lower quality by discarding clusters with a low educational score (e.g. Explicit Adult Content). You can check this [demo](https://huggingface.co/spaces/HuggingFaceTB/inspect_clusters_free_topics) for an example.


<div align="center">
    <img src="https://huggingface.co/datasets/HuggingFaceTB/miscellaneous/resolve/main/AMT_plots/topics_distpng.png" alt="clusters" width="1000" height="700">
    <p>The clusters of AutoMathText</p>
</div>
