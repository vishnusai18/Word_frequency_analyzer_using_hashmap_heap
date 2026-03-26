# MSML606 HW3 Extra Credit Project
## Analyzing Word Frequency Patterns in AI and Human Text Using Hashing

### Overview
This project analyzes word frequency patterns in AI-generated and human-written text using hashing.  
A custom hash table is used for efficient word counting, and Python's `heapq` library with `heapify` is used for top-k, least-k, and threshold-based retrieval.

### Dataset
- Hugging Face dataset: `NabeelShar/ai_and_human_text`

### Features
- Preprocesses noisy real-world text
- Counts words using a custom hash map
- Finds top-k and least frequent words
- Lets users choose `k` in the Streamlit app for either `Top K` results or words with frequency `At Least K`
- Compares AI-generated vs human-written vocabulary patterns
- Optional Streamlit interface for visualization

### Files
- `hash_map.py` – custom hash table implementation
- `data_analysis.py` – loads dataset, preprocesses text, performs analysis
- `app.py` – Streamlit frontend
- `outputs/results.json` – saved results

### How to Run
1. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
2. run the main backened:
   ```bash
   python3 data_analysis.py
3. run the frontend streamlit:
   ```bash
   streamlit run app.py
   
   
   
