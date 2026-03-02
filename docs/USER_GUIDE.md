# User Guide

Welcome to the Document-Based RAG System. This guide will help you understand how to use the system to query your documents effectively.

## Getting Started

### 1. Preparing Your Documents
The system supports the following formats:
- **PDF**: Standard portable documents.
- **DOCX**: Microsoft Word documents.
- **TXT**: Plain text files.

*Note: Ensure files are under 20MB for optimal processing.*

### 2. Uploading Documents
When you upload a document, the system performs several steps:
1. **Parsing**: It reads the text from your file.
2. **Indexing**: It breaks the text into small pieces and "memorizes" them in a searchable database.
3. **Isolation**: Your documents are tagged with your unique User ID, ensuring no one else can see or query your data.

### 3. Asking Questions
Once your document is indexed (usually within a few seconds for small files), you can ask questions in plain English.

**Tips for better answers:**
- **Be Specific**: Instead of "What does it say about money?", try "What was the net profit mentioned in the Q3 summary?"
- **Use Filters**: If you have many documents but only want answers from one specific file, use the document filter option in your query.

### 4. Understanding the Response
Every answer provided by the system includes **Sources**. 
- **Answer**: The AI-generated response based on your documents.
- **Sources**: A list of documents and page numbers where the information was found. This allows you to verify the facts yourself.

## Troubleshooting

### Why is the system saying it can't find information?
- **Processing Time**: If you just uploaded a large document, wait a few seconds for indexing to complete.
- **User ID Mismatch**: Ensure you are using the same User ID for both uploading and querying.
- **Context**: The AI only knows what is in the documents you uploaded. If the information isn't there, it will inform you that it cannot find the answer.

### Error: "File format not supported"
Ensure your file ends in `.pdf`, `.docx`, or `.txt`. Scanned images inside PDFs may not be readable unless they contain a text layer (OCR).
