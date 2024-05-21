from memory_profiler import profile
from flask import Flask, render_template, request, jsonify
import ssl
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from syllapy import count as syllable_count
import nltk

app = Flask(__name__)


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context



def extract_main_content(soup):
  
    main_content = soup.find('div', class_='content')  
    if not main_content:
        main_content = soup.find('div', id='main')      

        
    if not main_content:
        div_tags = soup.find_all('div')
        max_text_length = 0
        for div in div_tags:
            text_length = len(div.get_text(strip=True))
            if text_length > max_text_length:
                max_text_length = text_length
                main_content = div

    

    text_content = "\n".join([element.strip() for element in main_content.stripped_strings])
    return text_content


@app.route('/')
def index():
    return render_template('index1.html')

@profile
@app.route('/analyze', methods=['POST'])
def analyze_text():
    url = request.form['url']

    if not url:
        return jsonify({'error': 'Please enter a valid URL'})

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        main_content_text = extract_main_content(soup)
        if main_content_text is None:
            return jsonify({'error': 'Failed to extract main content from the URL'})
        
        output_file_path = "extracted_text.txt"
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(f"Text Content:\n\n{main_content_text}")

        blob = TextBlob(main_content_text)

        # Sentiment Analysis
        positive_score = blob.sentiment.polarity
        negative_score = -positive_score
        polarity_score = blob.sentiment.polarity
        subjectivity_score = blob.sentiment.subjectivity

        # Word and Sentence Metrics
        word_count = len(blob.words)
        sentence_count = len(blob.sentences)
        avg_sentence_length = word_count / sentence_count
        avg_words_per_sentence = len(blob.words) / len(blob.sentences)

        syllable_count_values = [syllable_count(word) for word in blob.words]

        # Percentage of Complex Words
        complex_word_count = sum(1 for count in syllable_count_values if count > 2)
        percentage_complex_words = (complex_word_count / word_count) * 100

        # FOG Index
        fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

        # Personal Pronouns
        personal_pronouns = sum(1 for word, pos in blob.tags if pos == 'PRP')

        # Average Word Length
        avg_word_length = sum(len(word) for word in blob.words) / word_count

        # Named Entity Recognition (NER)
        named_entities = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(main_content_text)))

        # Part-of-Speech (POS) Taggin
        pos_tags = nltk.pos_tag(blob.words)

        # Readability Metrics
        flesch_reading_ease = 206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (sum(syllable_count_values) / word_count)
        flesch_kincaid_grade_level = 0.39 * (word_count / sentence_count) + 11.8 * (sum(syllable_count_values) / word_count) - 15.59

        

        # Determine the appropriate age group based on readability metrics
        
        def get_age_group(fog_index, flesch_reading_ease, flesch_kincaid_grade_level, avg_word_length):
            age_group_ranges = {
                (0, 12): "The content is suitable for children.",
                (13, 18): "The content is suitable for teenagers.",
                (19, 30): "The content is suitable for young adults.",
                (31, 50): "The content is suitable for adults.",
                (51, 70): "The content is suitable for middle-aged individuals.",
                (71, 100): "The content is suitable for seniors.",
                (13, 30): "The content is suitable for teenagers and young adults.",
                (31, 100): "The content is suitable for adults and seniors."
            }

            # Determine age group based on multiple readability metrics and analysis criteria
            if fog_index < 10 and flesch_reading_ease > 80 and avg_word_length < 5:
                return age_group_ranges[(0, 12)]
            elif fog_index < 15 and flesch_reading_ease > 70 and avg_word_length < 7:
                return age_group_ranges[(13, 18)]
            elif flesch_reading_ease > 60 and avg_word_length < 10:
                return age_group_ranges[(19, 30)]
            elif flesch_reading_ease > 50 and avg_word_length < 14:
                return age_group_ranges[(31, 50)]
            elif flesch_reading_ease > 45 and avg_word_length < 18:
                return age_group_ranges[(51, 70)]
            elif flesch_reading_ease > 40:
                return age_group_ranges[(71, 100)]
            elif flesch_kincaid_grade_level < 25 and flesch_reading_ease > 20:
                return age_group_ranges[(13, 30)]  # Adjust age group for easier readability level
            else:
                return age_group_ranges[(31, 100)]  


        age_group_statement = get_age_group(fog_index, flesch_reading_ease, flesch_kincaid_grade_level, avg_word_length)

        # Prepare the analysis results including the age group statement
        analysis_results = {
            'positive_score': positive_score,
            'negative_score': negative_score,
            'polarity_score': polarity_score,
            'subjectivity_score': subjectivity_score,
            'avg_sentence_length': avg_sentence_length,
            'avg_words_per_sentence': avg_words_per_sentence,
            'complex_word_count': complex_word_count,
            'percentage_complex_words': percentage_complex_words,
            'fog_index': fog_index,
            'personal_pronouns': personal_pronouns,
            'avg_word_length': avg_word_length,
            'flesch_reading_ease': flesch_reading_ease,
            'flesch_kincaid_grade_level': flesch_kincaid_grade_level,
            'age_group_statement': age_group_statement  # Include the age group statement in the results
        }

        return jsonify({'success': True, 'analysis_results': analysis_results})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True,port=8000)
