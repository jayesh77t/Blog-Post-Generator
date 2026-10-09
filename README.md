# AI Blog Generator (Outline -> Draft -> Polish Pipeline)



An interactive, multi-stage AI blog writing assistant built with **Streamlit**, **LangChain**, and **Groq**. This project uses a sequential three-step agentic pipeline to turn any topic into a natural, human-sounding blog post.



---



## Features



- **Multi-Stage Pipeline:** 

  1. **Outline Generation:** Structures hooks, section headings, and core key points.

  2. **Drafting:** Writes the initial content based on the outline using strict human-writing style guides.

  3. **Polishing:** Refines flow, adds a title, and ensures markdown compatibility.

- **Interactive UI:** Built with Streamlit, featuring a clean sidebar configuration, step-by-step status trackers, and tabbed result views.

- **Human-Style Guardrails:** Built-in prompt constraints that ban common AI buzzwords (*"delve", "game-changer", "seamless", etc.*) and force varied sentence lengths, contractions, and concrete examples.

- **Export Options:** Instantly download your final blog post as a `.md` file.



---



## Project Structure



```text

BLOG_PROJECT/

│
├── .venv/             # Virtual environment directory
├── Blog_Agent/
│   └── app.py         # Main Streamlit application
├── .env               # Environment variables (API keys)
├── .gitignore         # Git ignore file
├── README.md          # Project documentation
└── requirements.txt   # Python dependencies

```



---



## Tech Stack



- **Frontend & UI:** [Streamlit](https://streamlit.io/)

- **Orchestration:** [LangChain](https://www.langchain.com/)

- **LLM Engine:** [Groq API](https://groq.com/) (using ultra-fast inference models)



---



## Setup and Installation



### 1. Clone the Repository



```bash

git clone https://github.com/jayesh77t/Blog-Post-Generator.git

cd BLOG_PROJECT

```



### 2. Create and Activate a Virtual Environment



```bash

python -m venv .venv

# On Windows:

.venv\Scripts\activate

# On macOS/Linux:

source .venv/bin/activate

```



### 3. Install Dependencies



Make sure your `requirements.txt` includes the necessary packages:



```bash

pip install -r requirements.txt

```



*(If you need to generate one, ensure `streamlit`, `langchain`, `langchain-groq`, `langchain-core`, and `python-dotenv` are installed.)*



### 4. Configure Environment Variables



Create a `.env` file in the root directory and add your Groq API key and model name:



```env

GROQ_API_KEY=your_actual_groq_api_key_here

MODEL=openai/gpt-oss-20b

```



---



## Running the Application



Run the Streamlit app from your terminal:



```bash

streamlit run Blog_Agent/app.py

```



Open your browser at `http://localhost:8501` to use the application.



---



## How It Works



1. **Configure:** Enter your target blog topic and pick a tone (`direct`, `normal`, or `friendly`) in the sidebar.

2. **Generate:** Hit **Generate Blog Post** to trigger the LangChain sequential chain.

3. **Inspect:** Use the tabs to preview the final result, look at the intermediate outline and draft, or copy/download the raw markdown code.



---



## License



This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).
