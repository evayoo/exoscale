# Exoscale API Project

This project demonstrates how to interact with the Exoscale API (https://www.exoscale.com) using Python. It includes examples of creating instances, managing SSH keys, and configuring security groups.

## Prerequisites

- Python 3.6 or later
- `pip` (Python package installer)
- Exoscale (https://www.exoscale.com/) account with API key and secret

## Setup

### 1. Clone the Repository

```sh
git clone git@github.com:evayoo/exoscale.git
cd exoscale
```

### 2. Create a Virtual Environment

```sh
python3 -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory and add your Exoscale API key and secret:

```plaintext
API_KEY=your_api_key_here
API_SECRET=your_api_secret_here
```

### 5. Running the Script

Execute the Python script to interact with the Exoscale API:

```sh
python script.py
```

## Project Structure

```
exoscale/
├── .env.example
├── .gitignore
├── create-instance.py
├── delete-instance.py
├── requirements.txt
└── README.md
```

- `.env.example`: Example of the `.env` file format.
- `.gitignore`: Specifies files and directories to be ignored by Git.
- `create-instance.py`: Main script demonstrating how to create instances.
- `delete-instance.py`: Main script demonstrating how to delete instances.
- `requirements.txt`: Lists the required Python packages.
- `README.md`: Project documentation.

## Usage

### Creating an Instance

You can create a new instance with the specified configuration. Sign in to Exoscale, and create an API key and store the access & secret access keys for your work. Update the `create-instance.py`,  `delete-instance.py` file with api_key and api_secret. Then run the Python code to create an instance. 

### Managing SSH Keys

The `create-instance.py` lists existing SSH key and uses a specified key for instance creation.

### Configuring Security Groups

The script checks for an existing security group named "allow-ping" and creates it if it doesn't exist. It also adds a rule to allow ICMP (ping) traffic.
