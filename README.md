# Text to Image Project

This project converts text prompts into images using a Django backend and Celery for task management.

## Setup
### Prerequisites

- Python 3.10
- Virtualenv

### Installation

1. **Clone the repository:**

    ```sh
    git clone [<repository-url>](https://github.com/satyajitsjs/Text-to-Image.git)
    cd Text-to-Image
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python3 -m venv evnsmart
    source evnsmart/bin/activate
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations:**

    ```sh
    python manage.py migrate
    ```
5. **Put The Stability Api Key:**
    - In settings.py
        - STABILITY_API_KEY = "Your API KEY"

6. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

### Celery Setup

1. **Start the Celery worker:**

    ```sh
    celery -A Text_to_Image worker --loglevel=info
    ```

# Usage
## Trigger a task:
- Send a POST request to /trigger_task with a JSON body containing the prompts.

    ```json
    {
        "prompts": ["Your text prompt here"]
    }
    ```

## Check task status:
- Send a GET request to /check_task_status/<task_id> to check the status of a task.
- And it will gave the image as response