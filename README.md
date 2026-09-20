# AI Guardian: Privacy-First Prompt Optimizer

A robust, Streamlit-based AI application that automatically upgrades user prompts into highly structured, expert-level instructions while strictly detecting and masking Personally Identifiable Information (PII) before it ever reaches the LLM. 

## 🚀 Features

* **Advanced PII Anonymization:** Utilizes Microsoft Presidio to detect and mask Emails, Phone Numbers, and Names.
* **Custom Password Detection:** Implements a custom Shannon Entropy algorithm (threshold ≥ 2.0) combined with strict alphanumeric and symbol checks to instantly catch exposed passwords while ignoring harmless typos.
* **LLM Safety Filter Bypass:** Intelligently replaces sensitive data with safe placeholders (like `[REDACTED]`) to protect privacy without triggering open-source LLM security refusals.
* **Zero-Hallucination Execution:** Operates at `temperature=0.0` for highly deterministic, consistent, and template-free prompt generation.
* **One-Shot Optimization:** Forces the LLM to deliver a complete, high-quality generalized response immediately, bypassing conversational stalling or user interrogation.

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **NLP & Privacy:** Microsoft Presidio (`presidio-analyzer`, `presidio-anonymizer`), spaCy
* **LLM Integration:** LangChain / LLM APIs (e.g., Groq)
* **Core Language:** Python 

## 📂 Project Structure

* `app.py`: The main Streamlit user interface and application loop.
* `agent.py`: Contains the core LLM execution engine and custom Presidio PII masking logic.
* `prompts.py`: Houses the strict system meta-prompts that enforce formatting and prevent title generation.
* `models.py`: Defines the data models and schemas used throughout the application.

## ⚙️ Installation & Setup

**1. Clone the repository**
```bash
git clone [https://github.com/yourusername/ai-guardian.git](https://github.com/yourusername/ai-guardian.git)
cd ai-guardian
2. Create and activate a virtual environment

Bash
# For Windows:
python -m venv .venv
.venv\Scripts\activate

# For Mac/Linux:
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
With the virtual environment activated, install the required packages and the spaCy language model:

Bash
pip install streamlit presidio-analyzer presidio-anonymizer spacy langchain python-dotenv pydantic
python -m spacy download en_core_web_lg
4. Set up environment variables
Create a .env file in the root directory and add your necessary API keys:

Code snippet
API_KEY=your_api_key_here
5. Run the application

Bash
streamlit run app.py
🧠 How it Works
Input: The user submits a raw, unoptimized prompt.

Sanitize: The mask_pii function scans for sensitive data (Emails, Passwords, etc.) and replaces them with safe [REDACTED] tags.

Optimize: The sanitized text is wrapped in a strict System Meta-Prompt, turning it into an expert-level request without asking the user for more information.

Execute: The final, safe, and highly structured prompt is executed at temperature=0.0, returning a precise, professional, and template-free response.

🔮 Future Scope (v2.0)
Regional PII Expansion: Integration of custom ML models or regional datasets to accurately detect non-Western identities (e.g., Indian name recognition), replacing the default spaCy limitations.

Expanded Masking: Adding support for financial data (Credit Cards, Bank Accounts) and physical addresses.

Model Scaling: Supporting additional LLM providers and localized deployment options.

👤 Author
Aishwari Bambale
