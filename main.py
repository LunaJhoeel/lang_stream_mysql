import credentials
import pandas as pd
from sqlalchemy import create_engine
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
import streamlit as st

# Page title
st.set_page_config(page_title='MyFuture-AI Tech Stack App')
st.title('MyFuture-AI Tech Stack App')

# Connection parameters to MySQL service inside Docker Compose
db_host = "mydb"
db_user = "root"
db_password = "root_password"
db_name = "tech_stack_db"
db_port = "3306"

# Function to fetch data from MySQL into a pandas DataFrame
def fetch_data_from_mysql(query):
    connection_str = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(connection_str)
    return pd.read_sql(query, engine)

# Generate LLM response
def generate_response(mysql_query, input_query):
    df = fetch_data_from_mysql(mysql_query)
    llm = ChatOpenAI(model_name='gpt-3.5-turbo-0613', temperature=0.2, openai_api_key=credentials.openai_api_key)
    
    # Create Pandas DataFrame Agent
    agent = create_pandas_dataframe_agent(llm, df, verbose=True, agent_type=AgentType.OPENAI_FUNCTIONS)
    
    # Perform Query using the Agent
    response = agent.run(input_query)
    return st.success(response)

# Input widgets
question_list = [
  '¿Cuántas filas hay en la bd de teck stack?',
  '¿Es "Test" un componente?',
  'Otra']
query_text = st.selectbox('Seleccione una consulta de ejemplo:', question_list)

# App logic
if query_text == 'Otra':
  query_text = st.text_input('Ingrese su consulta:', placeholder='Ingrese consulta aquí...')
else:
  # Corresponding MySQL query based on the selected question
  if query_text == '¿Cuántas filas hay en la bd de teck stack?':
      mysql_query = "SELECT COUNT(*) FROM tech_stack_table"  # Example query, adjust as needed
  elif query_text == '¿Es "Test" un componente?':
      mysql_query = "SELECT * FROM tech_stack_table WHERE component = 'Test'"  # Example query, adjust as needed
  else:
      mysql_query = ""  # Default or handle other cases

  response = generate_response(mysql_query, query_text)
  st.write(response)