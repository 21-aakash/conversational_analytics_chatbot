# SQL Chat Using LangChain

## Description
This Streamlit application allows users to interact with a MySQL database using natural language queries powered by LangChain. Users can explore and manipulate data without needing to write SQL commands directly.

## Deployed Link
- [SQL Chat Using LangChain](https://conversationalanalyticschatbot.streamlit.app/)
- [Algorithm Charts](https://docs.google.com/document/d/1FsQtduvAO54mPr5JvraIjTKfA9unPg1opfGcFczeJJ4/edit?addon_store)

## Getting Started

### Prerequisites
Ensure you have the following installed on your system:
- [Anaconda](https://www.anaconda.com/products/individual) (or Miniconda)
- Python 3.8 or higher

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/sql-chat-langchain.git
   cd sql-chat-langchain
2. **Create a Conda Environment**
   ```bash
   conda create -n sqlchat_env python=3

3. **Install Required Packages**
   Install all the required packages from the `requirements.txt` file.
   ```bash
   pip install -r requirements.txt
4. **Set Up Environment Variables**
  Create a .env file in the root directory to store your database credentials. Add the following lines:
   ```bash
   GROQ_API_KEY = 
Replace your_mysql_host, your_mysql_user, your_mysql_password, and your_database_name with your actual MySQL credentials.

5.**Use Streamlit to run the application.**
      ```bash
        streamlit run app.py


####  Algorithm

1. Import necessary libraries and load environment variables.
2. Set up Streamlit page configuration (title, icon).
3. Define a function to configure the SQLite database connection:
   a. Use sqlite3 to connect to a read-only database.
   b. Cache the connection for performance optimization.
4. Initialize the Groq language model using API key and model parameters.
5. Create a SQL database toolkit with the database connection and LLM.
6. Set up a SQL agent with:
   a. The LLM instance.
   b. The toolkit.
   c. Additional configurations (verbose mode, agent type).
7. Initialize session state for chat history.
8. Display all previous chat messages.
9. Provide an input box for user queries.
10. If a user submits a query:
    a. Add the query to chat history.
    b. Display the query in the chat interface.
    c. Process the query using the agent.
    d. Capture and display the agent's response.
    e. Append the response to chat history.
11. Wait for further user input to continue the interaction loop.

