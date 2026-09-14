# ContextGraph-PoC

\# ContextGraph Proof of Concept



This repository contains a proof of concept for ContextGraph.



ContextGraph is an application that will allow users to upload files and organize information into a knowledge graph. The saved information can later be accessed by AI applications through MCP.



\## Proof of Concept



This program:



1\. Reads information from a text file.

2\. Sends the information to Graphiti.

3\. Uses Google Gemini to find important information and relationships.

4\. Stores the knowledge graph in Neo4j.

5\. Searches the graph and returns saved information.



\## Technologies



\- Python

\- Graphiti

\- Neo4j

\- Google Gemini

\- MCP (planned next step)



\## Requirements



\- Windows 11

\- Python

\- Neo4j Desktop

\- Gemini API key



\## Setup



Create a virtual environment:



```powershell

python -m venv .venv

