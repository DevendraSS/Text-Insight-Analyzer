# Text-Insight-Analyzer

# Overview
The Text Insight Analyzer is a Flask web application designed to perform comprehensive web content analysis using various Natural Language Processing (NLP) techniques. Users can input a URL to extract the main content from a web page and obtain detailed analysis results, including sentiment scores, readability metrics, word and sentence statistics, and more.

# Features
Web Content Extraction: Extracts main content from web pages using BeautifulSoup.
Sentiment Analysis: Analyzes the sentiment of the text using TextBlob.
Readability Assessment: Computes readability metrics like Flesch Reading Ease, Flesch-Kincaid Grade Level, and Gunning Fog Index.
Word and Sentence Metrics: Provides word count, sentence count, average sentence length, and average words per sentence.
Syllable Counting: Counts syllables in the text using syllapy.
Complex Word Analysis: Identifies and calculates the percentage of complex words.
Part-of-Speech Tagging and Named Entity Recognition: Uses nltk for POS tagging and NER.
Personal Pronouns Counting: Counts personal pronouns using POS tags.
Age Group Assessment: Determines suitable age groups based on readability metrics and average word length.
Performance Profiling: Profiles memory usage of API endpoints using memory_profiler.

# Technologies and Libraries Used
Backend: Flask, requests, BeautifulSoup, TextBlob, syllapy, nltk, memory_profiler
Frontend: HTML, CSS, JavaScript
Styling: Google Fonts (Roboto), Custom CSS for responsive and user-friendly design

# Example Analysis
The analysis includes the following details:

Sentiment Scores: Positive, Negative, Polarity, and Subjectivity.
Readability Metrics: Flesch Reading Ease, Flesch-Kincaid Grade Level, Fog Index.
Word and Sentence Statistics: Word Count, Sentence Count, Average Sentence Length, Complex Word Percentage.
Additional Metrics: Personal Pronouns, Average Word Length, Named Entities.
