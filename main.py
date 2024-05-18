import openai
import json
import matplotlib.pyplot as plt
import sys

if len(sys.argv) < 2:
    print("Please provide OpenAI API key as an argument. Python main.py <API_KEY>")
    sys.exit(1)
openai.api_key = sys.argv[1]

TRUNCANATE_LIMIT_TOTAL=1000
TRUNCANATE_LIMIT_FUNCTION=300
import psycopg2

host = "localhost"
port = "6544"
user = "postgres"
password = "postgres"
database = "test"


def trigger_sql_query(query):
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
        )
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        if cur.description:
            result = cur.fetchall()
        else:
            result = "Query executed successfully."
        cur.close()
        conn.close()
        return result
    except Exception as e:
        return str(e)

def show_matplotlib_plot(plot_type: str, x: list, y: list, title: str, xlabel: str, ylabel: str):
    if plot_type == "line":
        plt.plot(x, y)
    elif plot_type == "scatter":
        plt.scatter(x, y)
    elif plot_type == "bar":
        plt.bar(x, y)
    else:
        "Invalid plot type. Supported types: 'line', 'scatter', 'bar'"
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    return "Plot displayed successfully."

def system_thought_proccess(task):
    how_to = "I don't have a thought process for this task."
    if task == "segmentation":
        how_to = """
        Data Segmentation Steps:
        1. Identify the Variable:
           - Ask the user for the variable or determine which variable you want to use for segmentation (e.g., transaction value, age).
        2. Determine Range:
           - Identify the minimum and maximum values of the variable in the dataset.
           - Calculate the range by subtracting the minimum value from the maximum value.
        3. Segment Creation:
           - Decide how many segments you want to create.
           - Divide the range of the variable by the number of segments to determine the width of each segment.
        4. Define Thresholds:
           - Define segment thresholds based on the width calculated in the previous step.
           - Use a CASE statement in an SQL query to assign each data point to the appropriate segment.
        5. Execute and Retrieve:
           - Execute the SQL statement.
           - Retrieve and review the segmented data to ensure it's correctly categorized.
        
        Example SQL snippet:
        ```sql
        SELECT 
            CASE 
                WHEN age <= 20 THEN 'Very Young'
                WHEN age BETWEEN 21 AND 30 THEN 'Young'
                WHEN age BETWEEN 31 AND 50 THEN 'Middle'
                WHEN age BETWEEN 51 AND 70 THEN 'Old'
                ELSE 'Very Old'
            END AS age_group
        FROM users;
        ```
        Note: Adjust age thresholds based on your specific requirements.
        """
    elif task == "exploratory_data_analysis":
        how_to = """
        Exploratory Data Analysis (EDA) process using SQL:
        1. Schema Exploration:
           - Identify tables and their relationships (DESCRIBE, SHOW COLUMNS FROM).
           - Understand column names, data types, and purpose.
        2. Data Quality Checks:
           - Check for missing values (COUNT(column_name) WHERE column_name IS NULL).
           - Identify duplicates (COUNT(*) GROUP BY all columns).
           - Look for outliers using descriptive statistics (next step).
        3. Descriptive Statistics:
           - Calculate summary statistics for numerical data (COUNT, SUM, AVG, MIN, MAX, STDDEV).
           - Use COUNT or COUNT(*) GROUP BY for category frequencies.
        4. Data Visualization:
           - Perform data visualization using function show_matplotlib_plot (e.g., histograms, box plots, scatter plots).
        5. Join and Filter Data:
           - Use JOIN clauses to combine data from multiple tables.
           - Filter data using WHERE clauses for specific analysis.
        6. Derive New Variables:
           - Create new calculated columns using SQL expressions.
           - This can involve math operations, date/time manipulations, or text transformations.
        7. Iterate and Refine:
           - As you explore, new questions may arise.
           - Refine your queries based on these questions and continue the exploration process.
        """
    elif task == "measures_computation":
        how_to = """
        Measures Computation Steps:
        1. Identify the Measures:
            - Determine the measures you want to compute (e.g., sum, average, count).
        2. Grouping Criteria:
            - Identify the grouping criteria for the computation (e.g., by region, by product).
        3. SQL Aggregation Functions:
            - Use SQL aggregation functions such as SUM, AVG, COUNT to compute the measures.
        4. Group By Clause:
            - Include the GROUP BY clause in your SQL query to group the data based on the criteria.
        5. Execute and Retrieve:
            - Execute the SQL query.
            - Retrieve and review the computed measures.
        """
    return how_to


AVAILABLE_FUNCTIONS = {
    "trigger_sql_query": trigger_sql_query,
    "system_thought_proccess": system_thought_proccess,
    "show_matplotlib_plot": show_matplotlib_plot,
}

FUNCTIONS = [
    {
        "name": "trigger_sql_query",
        "description": "Trigger a SQL query on the database. Dont read all data from the database, just a few rows.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "SQL query to be executed.",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "system_thought_proccess",
        "description": "Get instructions on how to accomplish a given task. Supported tasks=['segmentation', 'exploratory_data_analysis', 'measures_computation']",
        "parameters": {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "Type of task you want a thought proccess for.",
                },
            },
            "required": ["task"],
        },
    },
    {
        "name": "show_matplotlib_plot",
        "description": "Show a matplotlib plot based on the given data.",
        "parameters": {
            "type": "object",
            "properties": {
                "plot_type": {
                    "type": "string",
                    "description": "Type of plot to show. Supported types=['line', 'scatter', 'bar']",
                },
                "x": {
                    # "type": "array",
                    "description": "X-axis data points.",
                },
                "y": {
                    # "type": "array",
                    "description": "Y-axis data points.",
                },
                "title": {
                    "type": "string",
                    "description": "Title of the plot.",
                },
                "xlabel": {
                    "type": "string",
                    "description": "Label for X-axis.",
                },
                "ylabel": {
                    "type": "string",
                    "description": "Label for Y-axis.",
                },
            },
            "required": ["plot_type", "x", "y", "title", "xlabel", "ylabel"],
        },
    },
]


def read_messages():
    with open("messages/messages.json", "r") as f:
        return json.load(f)


def write_messages(messages):
    with open("messages/messages.json", "w") as f:
        json.dump(messages, f, indent=4)


messages = read_messages()

def handle_response_message(messages, response_message):
    messages.append(response_message)
    if response_message.get("function_call"):
        return handle_function_call(messages, response_message)
    elif response_message.get("content"):
        return handle_user_response(messages, response_message)
    else:
        raise Exception("Invalid response message.")

def truncanate_messages(messages, n=10):
    messages_content = [message["content"] or str(message["function_call"])  for message in messages]
    messages_content = "\n".join(messages_content)
    if len(messages_content.split()) < TRUNCANATE_LIMIT_TOTAL:
        return messages
    else:
        print(f"        > [SYS]: Truncating messages to last {n} messages.")
        return truncanate_messages(messages[-n:], n-1)


def send_messages_to_model(messages):

    messages = truncanate_messages(messages)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=FUNCTIONS,
        function_call="auto",
    )
    response_message = response["choices"][0]["message"]
    return handle_response_message(messages, response_message)


def handle_function_call(messages, response_message):
    function_name = response_message["function_call"]["name"]
    function_to_call = AVAILABLE_FUNCTIONS[function_name]
    function_args = json.loads(response_message["function_call"]["arguments"])

    print(f"        > [GPT]: Call function {function_name} with args {function_args}")
    print(f"        > [SYS]: Calling function {function_name}")
    try:
        function_response = function_to_call(**function_args)
    except Exception as e:
        function_response = "Function call failed."
        print(f"        > [SYS]: Function call failed.")
    try:
        function_response = json.dumps(function_response)
    except:
        function_response = json.dumps(str(function_response))



    # truncate the response if it's too long
    if len(function_response) > TRUNCANATE_LIMIT_FUNCTION:
        function_response = function_response[:TRUNCANATE_LIMIT_FUNCTION] + "... (message was too long)"
    print(f"        > [SYS]: Function responded: {function_response[:100]}")

    messages.append(
        {
            "role": "function",
            "name": function_name,
            "content": function_response,
        }
    )
    return send_messages_to_model(messages)


def handle_user_response(messages, response_message):
    if response_message:
        print(f"[GPT]: {response_message['content']}")
    user_response = input("\n[YOU]: ")
    if user_response == " " or user_response == "":
        return messages
    messages.append({"role": "user", "content": user_response})
    return send_messages_to_model(messages)


messages = handle_user_response(messages, None)


print()
if input("[SYS]: Do you want to save the conversation? [y/N]: ") == "y":
    print("[SYS]: Saving messages...")
    write_messages(messages)
    print("[SYS]: Messages saved...")
