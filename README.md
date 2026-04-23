AI Research Assistant

I built this project to make it easier to search through documents without manually reading everything.

The idea is simple — you upload a file, ask a question, and the system finds the most relevant parts of that file using semantic search.


* What it does

You can:
- Upload a text file
- Ask a question about it
- Get back the most relevant section from the document

Instead of keyword matching, it uses embeddings to understand the meaning of your query and compare it with the document content.



* Why I built this

Tools like ChatGPT are great, but they are more general-purpose. I wanted to build something focused specifically on searching through user-provided documents.

This project is basically a small step toward how real-world systems handle document search internally — where the answers come strictly from your own data.


 * How it works (simple explanation)

- The uploaded file is read and converted into text  
- A small portion of that text is turned into an embedding  
- The embedding is stored in a database  
- When you ask a question, it’s also converted into an embedding  
- The system compares them and returns the closest match  



* Tech used

- FastAPI for backend
- HTML, CSS, JavaScript for frontend
- SQLite for database
- Embeddings + cosine similarity for search



 * How to run it

Clone the repo:
git clone https://github.com/Gayathri0601/ai-research-assistant.git
cd ai-research-assistant

Create virtual environment:
python -m venv venv
venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Run backend:
uvicorn main:app --reload

Run frontend:
cd frontend
python -m http.server 5500

Open this in browser:
http://127.0.0.1:5500


* Limitations

Right now it’s pretty basic:

- Only supports `.txt` files  
- Uses a small chunk of text (not full document processing)  
- No authentication or user accounts  
- UI is simple and focused on functionality  


* What I learned

This project helped me understand:
- How embeddings work in practice  
- How to connect frontend and backend  
- Handling file uploads and APIs  
- Debugging issues like CORS and routing  
- Structuring a full project from scratch  


 * What I would improve next

If I continue working on this, I would:
- Support PDFs and larger documents  
- Store and search multiple chunks instead of one  
- Add a chat-style interface  
- Improve ranking and accuracy  
- Deploy it for public use  


* Final thought

This isn’t meant to replace ChatGPT. It’s more about building a focused system that works on your own documents — which is something many real-world applications need.

