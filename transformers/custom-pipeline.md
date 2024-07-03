```py
%%writefile agri_custom_pipeline.py

from transformers import AutoTokenizer, BertForSequenceClassification, Pipeline
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import numpy as np
import warnings
import string
import torch
import nltk
import re

# Download necessary NLTK packages
nltk.download('averaged_perceptron_tagger')
nltk.download("stopwords")
nltk.download('wordnet')
nltk.download('punkt')

# Supress warning
warnings.filterwarnings('ignore')

# pre-processing modules
class RemovePunctuation:
    """
    class to remove the corresponding punctuation from the list of punctuations
    """

    def __init__(self):
        """
        :param empty: None
        """
        self.punctuation = string.punctuation

    def __call__(self, punctuations):
        """
        Apply the transformations above.
        :param punctuation: take the single punctuation(in my case '?')
        :return: transformed punctuation list, excluding the '?'
        """
        if type(punctuations) == str:
            punctuations = list(punctuations)
        for punctuation in punctuations:
            self.punctuation = self.punctuation.translate(str.maketrans('', '', punctuation))
        return self.punctuation


# Accessing the remove_punctuation object
remove_punctuation = RemovePunctuation()


def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # Default to Noun if the part of speech is not recognized


class ProcessText(object):

    @staticmethod
    def remove_punctuation_text(text):
        """custom function to remove the punctuation"""
        res = (re.findall(r'\w+|[^\s\w]+', text))
        name = []
        for word in res:
            clean_word = word.translate(str.maketrans('', '', remove_punctuation("")))
            if clean_word != "":
                name.append(clean_word)

        return " ".join(name)

    @staticmethod
    def remove_stopwords(text):
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text)
        filtered_words = [word for word in words if word.lower() not in stop_words]
        return ' '.join(filtered_words)

    @staticmethod
    def lower_casing(text):
        text_lower = text.lower()

        return text_lower


    @staticmethod
    def lemmatize_text(text):
        lemmatizer = WordNetLemmatizer()
        words = word_tokenize(text)
        tagged_words = nltk.pos_tag(words)
        lemmatized_words = [lemmatizer.lemmatize(word, pos=get_wordnet_pos(tag)) for word, tag in tagged_words]
        return ' '.join(lemmatized_words)

    @staticmethod
    def remove_duplicates_and_sort(text):
        # Split the text into individual words
        words = text.split()

        # Create a set to store unique words (which automatically removes duplicates)
        unique_words = set(words)

        # Sort the unique words based on their original order in the text
        sorted_unique_words = sorted(unique_words, key=lambda x: words.index(x))

        # Join the sorted unique words back into a string with space as separator
        sorted_text = ' '.join(sorted_unique_words)

        return sorted_text

    @staticmethod
    def remove_numbers(text):
        # Use regex to replace all numbers with an empty string
        cleaned_text = re.sub(r'\d+', '', text)
        return cleaned_text

    @staticmethod
    def include_words_with_len_greater_than_2(text):
        # Split the text into words
        words = text.split()

        # Filter out words with length greater than 2
        filtered_words = [word for word in words if len(word) > 2]

        # Join the filtered words back into a text
        cleaned_text = ' '.join(filtered_words)

        return cleaned_text

    def __call__(self, text):
        # remove any punctuation
        text = self.remove_punctuation_text(text)

        # Covert text into lower case
        text = self.lower_casing(text)

        # Stopwords such as "is", "the", etc that coney no meaning are removed
        text = self.remove_stopwords(text)

        # Lemmatization is done for converting words to their base or root form, considering their context and part of speech.
        text = self.lemmatize_text(text)

        # Since words are independent to one another in our problem scenario we can sort the text by word and remove any kind of duplicacy
        text = self.remove_duplicates_and_sort(text)

        cleaned_text = self.include_words_with_len_greater_than_2(self.remove_numbers(text))

        return cleaned_text


# custom inference pipeline
class AgriClfPipeline(Pipeline):
    def _sanitize_parameters(self, **kwargs):
        preprocess_kwargs = {}
        if "text" in kwargs:
            preprocess_kwargs["text"] = kwargs["text"]
        return preprocess_kwargs, {}, {}

    def preprocess(self, text, **kwargs):
        textPre_processing = ProcessText()  
        processed_description = textPre_processing(text)
        try:
            if type(processed_description) == str:
                tokenizer = AutoTokenizer.from_pretrained("divyanshu94/agriBERT_clfModel")
                processed_description = str(processed_description)
                predToken = tokenizer.encode(processed_description, add_special_tokens=True)

                max_len = 155
                padded_predToken = np.array([predToken + [0]*(max_len-len(predToken))])
                predAttention_mask = np.where(padded_predToken != 0, 1, 0)

                input_idsPred = torch.tensor(padded_predToken)
                attention_maskPred = torch.tensor(predAttention_mask)

                return {"input_idsPred": input_idsPred, "attention_maskPred": attention_maskPred}
        except Exception as error:
            print("{}".format(str(error)))
            return -1

    def _forward(self, model_inputs):
        input_idsPred = model_inputs["input_idsPred"]
        attention_maskPred = model_inputs["attention_maskPred"]
        self.model = self.model.to("cuda")  # Ensure model is on CUDA if available

        with torch.no_grad():
            output = self.model(input_idsPred.to("cuda"), token_type_ids=None, attention_mask=attention_maskPred.to("cuda"))
        prediction = 1 if np.argmax(output.logits.cpu().numpy()).flatten().item() == 1 else 0

        return {"logits": "agri" if prediction == 1 else "non-agri"}

    def postprocess(self, model_outputs, **kwargs):
        return model_outputs["logits"]

 ```
## Register the Pipeline
```py
from agri_custom_pipeline import AgriClfPipeline
from transformers import BertForSequenceClassification
from transformers.pipelines import PIPELINE_REGISTRY

# Register your custom pipeline
PIPELINE_REGISTRY.register_pipeline(
    "agri-classification",
    pipeline_class = AgriClfPipeline,
    pt_model = BertForSequenceClassification
)
```


```py
agri_classifier = pipeline("agri-classification", model="divyanshu94/agriBERT_clfModel")
agri_classifier("<your input text goes here>")
```

### Uploading to HuggingFace Hub 
```py
from huggingface_hub import Repository

repo = Repository("agriBERT_clfModel", clone_from="divyanshu94/agriBERT_clfModel")
classifier.save_pretrained("agriBERT_clfModel")

```

Resources:
1. [Custom-pipeline](https://ddimri.medium.com/building-and-sharing-custom-pipelines-with-the-hugging-face-hub-f50faf6135c5)
2. [How to create a custom pipeline?](https://huggingface.co/docs/transformers/v4.42.0/add_new_pipeline)

