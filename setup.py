from setuptools import setup, find_packages

setup(
    name="solipsys",
    version="0.1.0",
    description="A dual-engine RAG core (SQLite + ChromaDB)",
    author="Seu Nome Biológico",
    packages=find_packages(), # Isso acha a pasta solipsys/ automaticamente
    install_requires=[
        "chromadb>=0.4.24",
        "pypdf>=4.1.0",
        "pydantic>=2.6.3"
    ],
)