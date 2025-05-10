# Legal AI Assistant

This project is a multimodal legal AI assistant for Indian law, featuring retrieval-augmented generation (RAG), text-to-image (T2I), and text-to-speech (T2S) capabilities. It includes a custom fine-tuned Llama 3.2-1B model, trained using synthetic and real legal Q\&A data.

---

## Features

* **Legal RAG Assistant**: Answers legal questions using both Pinecone and FAISS vector databases, with Gemini or local LLMs for generation.
* **Text-to-Image (T2I)**: Generates images from text prompts using Stable Diffusion XL via Hugging Face API.
* **Text-to-Speech (T2S)**: Converts text to speech and transcribes speech to text using Google Cloud APIs.
* **Custom Fine-tuned LLM**: Llama 3.2-1B model fine-tuned on synthetic and real Indian legal Q\&A pairs.
* **Legal Data Scraping**: Automated scraping and PDF compilation of IPC sections from devgan.in.

---

## Directory Structure

```
project/
├── setup/
│   ├── test_stream/
│   │   ├── t2i_stream.py         # Streamlit T2I demo
│   │   ├── t2s_stream.py         # Streamlit T2S demo
│   │   └── faiss_create.py       # FAISS index creation
│   ├── lawyer_gpt_faiss.index    # FAISS index file
│   ├── lawyer_gpt_metadata.pkl   # FAISS metadata
│   ├── pine_setup.py             # Pinecone index setup
│   ├── research_paper.pdf        # Scraped IPC sections
│   └── webscrape.py              # Legal data scraper
├── app.py                        # Main Streamlit app
├── app2.py                       # Alternate app interface
├── t2i.py                        # T2I utility
├── t2s.py                        # T2S utility
├── requirements.txt              # Dependencies
├── Copy_of_Meta_Synthetic_Data_Llama3_2_(3B).ipynb # Fine-tuning notebook
├── techrag-fd5b10f7f09e.json     # Google Cloud credentials
└── README.md                     # This file
```

---

## Data Sources

* **Pinecone RAG**: viber1/indian-law-dataset
* **FAISS RAG**: nisaar/Lawyer\_GPT\_India
* **Synthetic/Fine-tune**: Locally generated and real Q\&A pairs in JSON format

---

## Synthetic Data Kit Workflow (Meta)

The Synthetic Data Kit enables local generation of high-quality Q\&A pairs for LLM fine-tuning:

1. **Ingest**: Convert legal PDFs (e.g., `research_paper.pdf`) to plain text.
2. **Chunk**: Split long documents into manageable text chunks.
3. **Generate QA**: Use the Synthetic Data Kit to generate Q\&A pairs from each chunk:

   ```bash
   synthetic-data-kit create chunk.txt --num-pairs 25 --type "qa"
   ```
4. **Format**: Save generated pairs in OpenAI/Alpaca-style JSON for LLM training.
5. **(Optional) Curate**: Filter and prune low-quality QAs using built-in tools.
6. **Load**: Combine all JSONs into a Hugging Face dataset for fine-tuning.

Example Q\&A JSON:

```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the punishment for theft under IPC?"},
    {"role": "assistant", "content": "Section 378. Punishment: 3 years and/or fine."}
  ]
}
```

---

## Fine-tuning with Unsloth

* **Model**: unsloth/Llama-3.2-1B-Instruct (1B parameters, 4-bit quantized)
* **Library**: Unsloth for efficient LoRA/QLoRA fine-tuning
* **Training**:

  * 3 epochs, batch size 8, AdamW optimizer
  * Only LoRA adapters updated (1–10% of parameters)
* **Saving**:

  * Adapters pushed to Hugging Face Hub
  * Full model can be merged and exported to GGUF/q4\_k\_m for llama.cpp or VLLM inference
* **Notebook Link** https://colab.research.google.com/drive/1L7PV34blo-YzlXRuxuEZHbttyFq3Kr0N?usp=sharing
---

## Setup & Usage

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare Data**

   * Run `webscrape.py` to generate `research_paper.pdf`
   * Run `pine_setup.py` and `faiss_create.py` to build vector stores

3. **Run Apps**

   ```bash
   streamlit run app.py          # Main legal assistant
   streamlit run t2i_stream.py   # Text-to-image demo
   streamlit run t2s_stream.py   # Text-to-speech demo
   ```

4. **Model Inference**

   * Use Gemini API by default in `app.py`
   * For local inference, load the LoRA adapters with Unsloth or Transformers and use the chat template format

---

## Security

* Store all API keys and credentials securely (not in code)
* Use environment variables for sensitive information in production

---

## Acknowledgments

* Meta Synthetic Data Kit
* Unsloth team
* Hugging Face Datasets
* Stability AI & Google Cloud
* Indian law open data contributors

For more details, see the fine-tuning notebook and code comments.
