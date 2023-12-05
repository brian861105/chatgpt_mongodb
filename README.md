# chatroom-backend

> Backend service for creating custom chatrooms, communicating with OpenAI API, and storing conversations in MongoDB.

background details relevant to understanding what this module does

## Prerequisites

Before you begin, ensure you have met the following requirements:

1. **Python 3.10 or higher**
2. **Create a tmp folder and configure key.json:** Follow these steps to set up your temporary folder and configure the `key.json` file:

   ```bash
   mkdir tmp
   cd tmp
   ```
Create a key.json file and add your MongoDB and OpenAI API keys:

    ```bash
    {
    "mongodb_password": "your_mongodb_password",
    "openai_api_key": "your_openai_api_key"
    }
    ```

## Getting Started
1. Clone the repository:
```bash
    git clone https://github.com/brian861105/chatroom-backend.git
```
2. Navigate to the project directory:
```bash
    cd chatroom-backend
```
3. Install the dependencies:
```bash
    pip install -r requirements.txt
```
4. Run the application:
``` bash
    python app/api.py
```
## Acknowledgments

## License