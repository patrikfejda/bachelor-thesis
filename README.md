# Bachelor Thesis: DataGPT

DataGPT is a conversational AI tool for business intelligence, built to streamline data analysis and reporting tasks.  It leverages the power of OpenAI's GPT-3.5-turbo-0613 language model to understand natural language queries and translate them into actionable insights. DataGPT also has the ability to interface with a PostgreSQL database, enabling direct data retrieval and manipulation using SQL.

## Features

* **Natural Language Processing:** Understands conversational language queries related to your datasets.
* **SQL Integration:**  Directly interacts with a PostgreSQL database to fetch, manipulate, and analyze data.
* **Data Visualization:**  Can potentially generate visualizations to aid in understanding your data (requires additional setup in `main.py`).
* **Business Intelligence Focus:**  Designed to assist with brainstorming, stakeholder communication, domain knowledge integration, metric identification, and analysis.

## Project Structure

* **`README.md`:** This file. Provides an overview of the project and instructions.
* **`docker-compose.yml`:** Configuration for setting up the PostgreSQL database environment using Docker.
* **`main.py`:** The core Python script that handles user interaction, OpenAI communication, SQL execution, and data visualization.
* **`messages/messages.json`:** Stores conversation history between the user and DataGPT.
* **`requirements.txt`:** Lists the required Python libraries for this project.
* **`sql_dumps/`:**  Contains sample SQL scripts (`carpassings.sql`, `users.sql`) for setting up the database schema and inserting example data.

## Getting Started

### Prerequisites

* **Python 3.x:** Make sure you have Python installed on your system.
* **Docker and Docker Compose:**  Install these tools to manage the database environment.
* **OpenAI API Key:**  Obtain an API key from OpenAI's platform.

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/patrikfejda/bachelor-thesis
   ```

2. **Start the Database:**
   ```bash
   docker-compose up -d 
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Optional: Load Sample Data:**
   * Use a PostgreSQL client (e.g., pgAdmin) to connect to the database (the default settings in `docker-compose.yml` use `postgres` as the user and password, and the database name is `test`).
   * Run the SQL scripts in the `sql_dumps` directory to create the tables and populate them with sample data.

### Usage

1. **Run the Script:**
   ```bash
   python main.py <YOUR_OPENAI_API_KEY>
   ```
   Replace `<YOUR_OPENAI_API_KEY>` with your actual OpenAI API key.

2. **Interact with DataGPT:**
   * Type your questions or requests in natural language.
   * DataGPT will respond with answers, insights, or SQL queries.
   * If DataGPT requests additional information, provide it.
   * To exit, press Ctrl+C or type "".