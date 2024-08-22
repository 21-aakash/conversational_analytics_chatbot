import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
import pandas as pd
import os
from dotenv import load_dotenv
from io import StringIO

# Load environment variables from the .env file
load_dotenv()

# Retrieve the Groq API key from the environment variables
api_key = os.getenv("GROQ_API_KEY")

# Check if the API key is present
if not api_key:
    raise ValueError("Groq API key is missing. Please ensure it's set in the .env file.")

# Now you can use the api_key variable in your application


# Setting up the page configuration with title and icon
st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="👽")


# CSS for background image
page_bg_img = '''
<style>
#root {
    background-image: url("back.jpg"); /* Update with your image path */
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
</style>
'''

# df = pd.read_csv('reports.csv', encoding='ISO-8859-1')
# st.write(df.head())


# Apply the background image CSS
st.markdown(page_bg_img, unsafe_allow_html=True)

with st.popover("Open popover"):
    
    name = st.text_input("What's your name?")

st.write("Your name:", name)
# Create two columns
col1, col2 = st.columns([1, 4])  # Adjust the ratio as needed

# Display the image in the first column
with col1:
    st.image("pic.png", width=120)

# Display the title in the second column
with col2:
    st.title("Hey! My name is SkyChat 7.0.0 ")


# Database connection options
LOCALDB = "USE_LOCALDB"

radio_opt = ["Use SQLite 3 Database - analytics_db"]



# Initialize the Groq LLM
llm = ChatGroq(groq_api_key=api_key, model_name="gemma2-9b-it", streaming=True)

# Function to configure SQLite database
@st.cache_resource(ttl="2h")
def configure_db():
    dbfilepath = (Path(__file__).parent / "analytics_db").absolute()
    creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
    return SQLDatabase(create_engine("sqlite:///", creator=creator))

# Configure DB
db = configure_db()

# SQL toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)  # Directly pass llm object

# Creating an agent with SQL DB and Groq LLM
agent = create_sql_agent(
    llm=llm,  # Pass llm directly
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# Session state for messages (clear button available)
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display chat history messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input for user query
user_query = st.chat_input(placeholder="Ask anything from the database")

# # If user query is submitted
# if user_query:
#     st.session_state.messages.append({"role": "user", "content": user_query})
#     st.chat_message("user").write(user_query)

#     # Generate response from agent
#     with st.chat_message("assistant"):
#         streamlit_callback = StreamlitCallbackHandler(st.container())
#         try:
#             response = agent.run(user_query, callbacks=[streamlit_callback])
#             st.session_state.messages.append({"role": "assistant", "content": response})
#             print("response", response)
#             st.write(response)

#             # Ensure the response is in tabular format
#             if isinstance(response, list):
#                 if all(isinstance(i, tuple) for i in response) and len(response) > 0:
#                     # Assuming the first tuple contains the headers
#                     headers = [f"Column {i+1}" for i in range(len(response[0]))]
#                     df = pd.DataFrame(response, columns=headers)
#                     st.dataframe(df.style.set_properties(**{'color': 'white', 'background-color': 'black'}))
#                 else:
#                     st.write("The response is not in tabular format.")
#             else:
#                 st.write("The response is not in tabular format.")
                
#         except Exception as e:
#             st.error(f"An error occurred: {str(e)}")
# If the user submits a query, process it
if user_query:
    # Add the user's message to the chat history and display it
    st.session_state["messages"].append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query, unsafe_allow_html=True)

    # Get the agent's response to the user's query
    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        # Run the agent with the user's query, capturing the output and displaying it
        response = agent.run(user_query,callbacks=[streamlit_callback] )
        # Add the assistant's response to the message history
        st.session_state["messages"].append({"role": "assistant", "content": response})
        # Display the assistant's response
        st.write(response, unsafe_allow_html=True)
#         print("type is :", type(response))
#         #Convert the string to a DataFrame
#         data = StringIO(response)  # Convert the string to a file-like object
#         df = pd.read_csv(data)     # Read the file-like object into a DataFrame

# # Display the DataFrame in a table format using Streamlit
#         st.dataframe(df)
#         # ans = pd.DataFrame(response, columns=[f"Column {i}" for i in range(len(response[0]))])
#         # st.dataframe(ans)
       
        
