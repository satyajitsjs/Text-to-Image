# Text to Image Project

This project converts text prompts into images using a Django backend and Celery for task management.

## Setup
### Prerequisites

- Python 3.10
- Virtualenv

### Installation

1. **Clone the repository:**

    ```sh
    git clone <repository-url>
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

5. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

### Celery Setup

1. **Start the Celery worker:**

    ```sh
    celery -A Text_to_Image worker --loglevel=info
    ```

Usage
Trigger a task:
Send a POST request to /trigger_task with a JSON body containing the prompts.

    ```json
    {
        "prompts": ["Your text prompt here"]
    }
    ```

Check task status:
Send a GET request to /check_task_status/<task_id> to check the status of a task.