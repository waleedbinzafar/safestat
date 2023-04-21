from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from flask import Flask, jsonify, request

app = Flask(__name__)
model_path = './models/transformers/' 
tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model = AutoModelForTokenClassification.from_pretrained(model_path, local_files_only=True)
nlp = pipeline("ner", model=model, tokenizer=tokenizer)

@app.route('/ner', methods=['POST'])
def predict():
    text = request.json['text']
    ner_results = nlp(text)

    loc_tokens = [ner for ner in ner_results if ner["entity"]=='I-LOC' or ner["entity"]=='B-LOC']
    token_groups = group_tokens(loc_tokens)
    words = [get_word_from_token_group(group) for group in token_groups]

    return jsonify(words)

def group_tokens(locs):
    locs_token_groups = []
    ind = -2
    group = []
    for loc in locs:
        if loc['index']!=ind+1:
            if len(group)>0:
                locs_token_groups.append(group)
            group=[]
        group.append(loc)
        ind=loc['index']
    locs_token_groups.append(group)

    return locs_token_groups

def get_word_from_token_group(token_group):
    prev_end = None
    word = ""
    for i, token in enumerate(token_group):
        if not prev_end:
            word = token['word']
        else:
            if token['start']==prev_end:
                word=word+token['word'].replace("#", "")
            else:
                word=word+" "+token['word']       
        prev_end = token['end']

    return word

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
