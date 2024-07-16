# 🔄 LangGPT: English-Hindi Translator

## Introduction

Welcome to the LangGPT project! Here, I have fine-tuned a pre-trained English-Hindi translator model using a custom dataset. This endeavor provided insights into the fundamentals of tokenizers, Hugging Face transformers, Hugging Face Hub, and Streamlit for app building. The project has been deployed using Streamlit Cloud and can be accessed via the link below.

Link: 
[LangGPT Streamlit](https://langgpt.streamlit.app/)

## Model - Helsinki-NLP/opus-mt-en-hi

I utilized a Hugging Face transformer model pre-trained for English-Hindi translations. Below are the benchmarks of the pre-trained model:

### Benchmarks of Pre-trained Model

| Test Set                        | BLEU | chr-F |
|---------------------------------|------|-------|
| newsdev2014.eng.hin             | 6.9  | 0.296 |
| newstest2014-hien.eng.hin       | 9.9  | 0.323 |
| Tatoeba-test.eng.hin            | 16.1 | 0.447 |

For more details, visit the model page: [Helsinki-NLP/opus-mt-en-hi](https://huggingface.co/Helsinki-NLP/opus-mt-en-hi)

## Dataset - cfilt/iitb-english-hindi

The IIT Bombay English-Hindi corpus contains parallel and monolingual Hindi corpora collected from various sources and developed at the Center for Indian Language Technology, IIT Bombay.

The dataset is structured as a list of dictionaries with English and Hindi translations labeled as `en` and `hi`.

Below is the data split provided by Hugging Face and the subset we used for fine-tuning our model.

| Type       | Rows Present | Rows Used |
|------------|--------------|-----------|
| Train      | 1.66M        | 100k      |
| Validation | 520          | 520       |
| Test       | 2.51k        | 500       |

For more information about the dataset: [cfilt/iitb-english-hindi](https://huggingface.co/datasets/cfilt/iitb-english-hindi)

## Steps Followed

1. Installed the necessary libraries.
2. Loaded the dataset from Hugging Face using the `load_dataset` module.
3. Loaded the tokenizer from the model checkpoint.
4. Preprocessed the dataset by converting the source and target text to tokens.
5. Loaded the pre-trained model from Hugging Face.
6. Defined the training parameters:
    ```python
    batch_size = 8
    num_samples = 100000  # Number of samples to select
    learning_rate = 2e-5
    weight_decay = 0.01
    num_epochs = 10
    ```
7. Prepared data collators.
8. Selected 100k rows from the training split due to resource constraints.
9. Defined the optimizer (`AdamWeightDecay`) and compiled the model.
10. Trained the model for `num_epochs` and saved it to a folder.
11. Loaded the saved model and evaluated the BLEU Score.
12. Pushed the tokenizer and model to Hugging Face and built an app using `Streamlit` utilizing the model from Hugging Face.

## Technologies Used

### Libraries
- 🤗 Transformers
- SentencePiece
- TensorFlow
- Datasets
- SacreBLEU

### Tools
- Hugging Face
- Streamlit
- Streamlit Cloud

## Results

The model was evaluated using the BLEU Score, a standard metric for language translation tasks.

| Test Set                        | BLEU Score |
|---------------------------------|------------|
| cfilt/iitb-english-hindi/test   | ~38        |

## Using the Repository

1. Clone the repository:
    ```sh
    git clone https://github.com/Srikar-V675/langgpt-pretrained.git
    ```
2. Change directory to the repository:
    ```sh
    cd langgpt-pretrained
    ```
3. Create directories for the model and tokenizer:
    ```sh
    mkdir model
    mkdir tokenizer
    ```
4. Run each cell from the `model-training.ipynb` Jupyter Notebook and update the location for saving the trained model:
    ```python
    # Old
    model.save_pretrained("langGPT/")

    # New
    model.save_pretrained("model/")
    ```
5. [Optional] Log in to Hugging Face Hub:
    ```sh
    huggingface-cli login
    ```
    **Note:** Obtain an access token from Hugging Face before running the command.
6. [Optional] Push the model to Hugging Face Hub by running `push_to_hub.py`:
    ```sh
    python push_to_hub.py
    ```
    **Note:** Update the `repo_name` variable to your Hugging Face repo name.
    ```python
    # Mine
    repo_name = "shinigami-srikar/langgpt-pretrained"

    # Yours
    repo_name = "your-username/your-repo-name"
    ```
7. Run the Streamlit app:
    ```sh
    streamlit run app.py
    ```
    **Note:** Update the `repo_name` in `app.py` to your Hugging Face Hub repo name.

Feel free to explore and enhance the project! 🚀