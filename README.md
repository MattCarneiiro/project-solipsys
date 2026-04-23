<div align="center">
  <h1>🧠 Solipsys</h1>
  <p><strong>The absolute foundation for knowledge systems and RAG (Retrieval-Augmented Generation).</strong></p>

  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/ChromaDB-Vector_Storage-orange.svg" alt="ChromaDB">
  <img src="https://img.shields.io/badge/SQLite-Ontology_Graph-lightgrey.svg" alt="SQLite">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</div>

---

## 🌌 What is Solipsys?

**Solipsys** is not just another wrapper for vector databases. It is a "dual-engine" core designed to manage human knowledge with surgical precision. It solves the classic problem of AI-based applications: the loss of structural context.

Instead of dumping everything into a vector black hole, Solipsys splits the brain in two:
1. **The Ontology Graph (SQLite):** Maintains logical organization, *Tags* (concepts), and hierarchical relationships (Parent Tag -> Child Tag).
2. **The Semantic Core (ChromaDB):** Transforms raw text and user highlights (*Anchors*) into mathematics, allowing for deep meaning-based searches, even when you forget how you categorized the information.

---

## ⚡ Key Features

- **Decoupled Memory:** Your tags and PDFs are not destroyed if the AI model changes or goes offline.
- **Source Auditing:** Differentiates user-generated knowledge (`USER`) from automatically inferred knowledge (`EGO`).
- **Sliding Window Chunking:** The native PDF parser slices documents while maintaining context cohesion, without cutting ideas in half.
- **The Physical Vault:** Manages secure copies of your PDFs. Never suffer from broken links or accidentally deleted files again.

---

## 🛠️ Installation

Clone this repository and install the essential dependencies in your virtual environment:

\`\`\`bash
# 1. Activate your venv (Recommended)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 2. Install dependencies
pip install -r requirements.txt
\`\`\`

---

## 🚀 Quick Start

The public API is designed to be clean and straightforward. Here is how you can ingest a PDF and search for knowledge in under 15 lines of code:

\`\`\`python
from solipsys import VaultClient, SemanticParser

# 1. Initialize the Vault (Creates databases automatically)
vault = VaultClient(base_path="./my_digital_brain")
parser = SemanticParser()

# 2. Digest a Document (Copies, slices, and vectorizes)
doc_id = parser.process_and_ingest(
    client=vault, 
    filepath="path/to/your_book.pdf",