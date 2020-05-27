# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Database Setup
From within the `backend` directory first ensure you are working using your created virtual environment.

With Postgres running, initialize the database using migrations. In terminal run:
```bash
python manage.py db upgrade
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
python manage.py run
```

Setting the `TRIVIA_ENV` variable to `dev` will detect file changes and restart the server automatically.

## API description

#### Endpoints

1. GET '/categories'
2. GET '/questions'
3. DELETE '/questions/<question_id>'
4. POST '/questions'
5. POST '/questions/search'
6. POST '/'

#### Responses

All endpoints return JSON messages with the following structure:
```json
{
    "success": true,
    "error": 0,
    "message": "<see description of the actual endpoint>"
}
```

For all HTTP error the following response is expected (using 404 as illustration):
```json
{
    "success": false,
    "error": 404,
    "message": "Message describing the error"
}
```

#### GET '/categories'

Description: Get the names of all available categories.

Parameters: None

Expected result:
```json
{
    "success": true,
    "error": 0,
    "message": 
    [
        "Category name 1",
        "Category name 2"
    ]
}
```

Errors: None

#### GET '/questions'

Description: Get a list of questions, including pagination (10 per page) and category selection.

Parameters: 
1. page: select which page to retrieve. (1 based)
    - Default: 1
2. category: string based name of category to retrieve OR "all" to retrieve all categories
    - Default: "all"

Expected result:
```json
{
    "success": true,
    "error": 0,
    "message": 
    {
        "current category": "category name / all",
        "categories":
            [
                "Category name 1",
                "Category name 2"
            ],
        "question_count": 123,
        "questions":
        [
            {
                "id": 1,
                "question": "What's up?",
                "answer": "Not much",
                "difficulty": 1,
                "category": "Category name 1"
            },
            {
                "id": 2,
                "question": "Who is a good boy?",
                "answer": "I am!",
                "difficulty": 1,
                "category": "Category name 1"
            }
        ]
    }
}
```

#### DELETE '/questions/<question_id>'

#### POST '/questions'

#### POST '/questions/search'

#### POST '/'

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```


## Testing
To run the tests, run

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
python manage.py test
```