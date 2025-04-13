# 📄 Arabic Biography Author Extractor

A Python-based (Streamlit) tool for extracting structured **author information** from **Arabic biography PDF files**. This project leverages PDF parsing and Arabic NLP techniques to extract names, birth/death dates, and other relevant biographical data for research and archival purposes.

---

## 🌟 Features

- ✅ Extracts text from Arabic PDF files (text-based)
- ✅ Identifies author names, birth/death dates, professions, and known works
- ✅ Handles right-to-left (RTL) Arabic script correctly
- ✅ Outputs structured data (JSON)
- ✅ Easily extensible for other metadata or text classification

---

## 🌟 Installation

Step 1: Clone the GitHub repo

Step 2: Make a virtual env -> py -m venv .venv (on gitbash)

Step 3: Activate .venv -> source .venv/Scripts/activate (on gitbash)

Step 4: pip install -r requirements.txt

Step 5: Add your Gemini api key in the .env file (I am using Gemini 1.5 Flash)

Step 6: streamlit run app.py

## 🌟 How to use

The application works in 2 steps. Firstly, parsing the whole document by author (the document is split into the total number of authors, each split contains data related to one author). In the second step, the data is sent to Gemini Multimodal to return JSON format data, as desired.

For every new document. We need to identify the pattern and then use that pattern to make splits. For example, for this specific document 004.pdf, we are using the following pattern.

/extractors/pdf_extractor.py

author_pattern = re.compile(r'(\d+)\s*-\s*(?![0-9\.\]\)\s])([^\n]+)')

🌟 Replace the "author_pattern" with your document-specific pattern. (Take help from ChatGPT)

Then from terminal, streamlit run app.py and the app will start processing. A folder named authors_data will be generated (as present in the repo). This folder will contain all one book's author data and an index file.
