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
From within the `backend` directory first ensure that:
1. You are working using your created virtual environment
2. You have a database called `trivia` created (See config.py for details about the connection string.)

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

## Testing
From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
python manage.py test
```

Note: All tests are running against an SQLite database, therefore the test database is no longer necessary.

## API description

#### Endpoints

1. GET '/categories'
2. POST '/categories'
3. GET '/questions'
4. DELETE '/questions/<question_id>'
5. POST '/questions'
6. POST '/questions/search'
7. POST '/'
8. GET '/users'
9. POST '/users'
10. POST '/results'

Note: The original requirements asked for an additional endpoint to query questions based on category. It seemed like a duplication of the GET '/questions' endpoint, therefore I didn't implement it.

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

#### POST '/categories'

Description: Create a new category.

Parameters: 
1. name: 
    - String
    - Name of the new category
    - Required

Expected result:
```json
{
    "success": true,
    "error": 0,
    "message": 
    {
        "category": "Category Name"
    }
}
```

Errors:
1. Missing required parameter: ERROR 422
2. Category name already exists in database: ERROR 422

#### GET '/questions'

Description: Get a list of questions, including pagination (10 per page) and category selection.

Parameters: 
1. page: 
    - Int
    - Select which page to retrieve. (1 based)
    - Default: 1
2. category: 
    - String
    - String based name of category to retrieve OR "all" to retrieve all categories
    - Default: "all"

Expected result:
```json
{
    "success": true,
    "error": 0,
    "message": 
    {
        "current_category": "category name / all",
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
                "category": "Category name 1",
                "answer_count": 1,
                "correct_answers": 1
            },
            {
                "id": 2,
                "question": "Who is a good boy?",
                "answer": "I am!",
                "difficulty": 1,
                "category": "Category name 1",
                "answer_count": 1,
                "correct_answers": 1
            }
        ]
    }
}
```

Errors:
1. Category does not exist: ERROR 404
2. No questions on selected page: ERROR 404

#### DELETE '/questions/<question_id>'

Description: Delete a question byu question ID.

Parameters: None

Expected result:
```json
{
    "success": true,
    "error": 0,
    "message": 
    {
        "question": 12
    }
}
```

Errors:
1. QuestionID does not exist: ERROR 404

#### POST '/questions'

Description: Create a new question.

Parameters: 
1. question: 
    - String
    - The question
    - Required
2. answer: 
    - String
    - the answer to the question
    - Required
3. category:
    - String 
    - Name of category to which the question belongs to
    - Required
4. difficulty: 
    - Int, 1-5
    - Difficulty level
    - Required

Expected result:
```json
{
    "success": true,
    "error": 0,
    "message": 
    {
        "question": 
        {
            "id": 1,
            "question": "What's up?",
            "answer": "Not much",
            "difficulty": 1,
            "category": "Category name 1",
            "answer_count": 1,
            "correct_answers": 1
        }
    }
}
```

Errors:
1. Any of the parameters missing: ERROR 422
2. Category name not found in database: ERROR 404

#### POST '/questions/search'

Description: Search existing questions.

Parameters: 
1. search_term:
    - String
    - Search term to be used on the questions
    - Required
2. page: 
    - Int
    - Select which page to retrieve. (1 based)
    - Default: 1

Expected result:
```json
{
    "success": true,
    "error": 0,
    "message": 
    {
        "question_count": 123,
        "questions":
        [
            {
                "id": 1,
                "question": "What's up?",
                "answer": "Not much",
                "difficulty": 1,
                "category": "Category name 1",
                "answer_count": 1,
                "correct_answers": 1
            },
            {
                "id": 2,
                "question": "Who is a good boy?",
                "answer": "I am!",
                "difficulty": 1,
                "category": "Category name 1",
                "answer_count": 1,
                "correct_answers": 1
            }
        ]
    }
}
```

Errors:
1. Required parameter missing: ERROR 422
2. No questions on selected page: ERROR 404

#### POST '/'

Description: Play Trivia.

Parameters: 
1. previous_questions:
    - [] of Int
    - Question IDs already used
    - Default: empty
2. category: 
    - String
    - Name of category for the game or "all" for using questions of all categories
    - Default: "all"

Expected result:
```json
{
    "success": true,
    "error": 0,
    "message": 
    {
        "id": 2,
        "question": "Who is a good boy?",
        "answer": "I am!",
        "difficulty": 1,
        "category": "Category name 1",
        "answer_count": 1,
        "correct_answers": 1
    }
}
```

#### GET '/users'

Description: Get a list of registered users.

Parameters: None

Expected result:
```json
{
    "success": true,
    "error": 0,
    "message": 
    [
        {
            "id": 1,
            "name": "Name1",
            "questions_answered": 1,
            "correct_answers": 1
        },
        {
            "id": 2,
            "name": "Name2",
            "questions_answered": 1,
            "correct_answers": 1
        }
    ]
}
```

Errors: None

#### POST '/users'

Description: Create a new user.

Parameters: 
1. name: 
    - String
    - Name of the new user
    - Required

Expected result:
```json
{
    "success": true,
    "error": 0,
    "message": 
    {
        "name": "New User Name"
    }
}
```

Errors:
1. Missing required parameter: ERROR 422
2. User name already exists in database: ERROR 422

#### POST '/results'

Description: Let the API know whether a question was answered sucessfully by a particular user.

Parameters: 
1. question_id: 
    - Integer
    - ID of question that was answered
    - Required
2. user_id: 
    - Integer
    - ID of user who answered the question
    - Required
    - Set to -1 if player doesn't want to collect info about him/her
3. success: 
    - Boolean
    - Whether the answer was correct
    - Required

Expected result if user ID is provided:
```json
{
    "success": true,
    "error": 0,
    "message": 
    {
        "user": 
        {
            "id": 2,
            "name": "Name2",
            "questions_answered": 1,
            "correct_answers": 1
        },
        "question": 
        {
            "id": 2,
            "question": "Who is a good boy?",
            "answer": "I am!",
            "difficulty": 1,
            "category": "Category name 1",
            "answer_count": 1,
            "correct_answers": 1
        }
    }
}
```

Expected result in Anonymous mode:
```json
{
    "success": true,
    "error": 0,
    "message": 
    {
        "user": "None",
        "question": 
        {
            "id": 2,
            "question": "Who is a good boy?",
            "answer": "I am!",
            "difficulty": 1,
            "category": "Category name 1",
            "answer_count": 1,
            "correct_answers": 1
        }
    }
}
```

Errors:
1. Missing required parameter: ERROR 422
2. Supplied question / user ID does not exist in database: ERROR 422

## Credits

Though I did not end up using Flask-RESTPlus for the project, I borrowed some of the implementation details from this tutorial:
https://www.freecodecamp.org/news/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563/