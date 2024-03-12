from youtube_transcript_api import YouTubeTranscriptApi
from deepmultilingualpunctuation import PunctuationModel
from transformers import pipeline

video_id = "8-Ymdc6EdKw"
transcripts = YouTubeTranscriptApi.get_transcript(video_id, languages=('en-US',))

text = []
for transcript in transcripts:
    current_line = transcript['text']
    if "[Music]" not in current_line:
        text.append(current_line)

data = PunctuationModel().restore_punctuation(" ".join(text))
data = data.split(".")

print(data)
final_result = 0
line_no = 1
classifier = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
results = classifier(data)
for result in results:
    if result['label'] == 'POSITIVE':
        final_result = final_result + result['score']
    else:
        final_result = final_result - result['score']
    print(f"label: {result['label']} with score : {round(result['score'], 4)}")
    line_no = line_no + 1

print(f"Total lines : {len(results)}")
print(f"Final Result = {final_result}")
final_result = final_result / len(results)

print(f"Avg result = {final_result}")

