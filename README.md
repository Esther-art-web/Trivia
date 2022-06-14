# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`
0
By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.


<!-- API Documentation -->

## API Reference

### Introduction
The Trivia API uses resource-oriented URLs, accepts JSON formatted, form encoded request bodies and returns **JSON-encoded** responses, using correct HTTP response status codes.

Trivia API was created using ***Test Driven Development*** (TDD), hence you can also use this API in test mode without interacting with your main development database


### Getting Started
#### Base URL
` http://127.0.0.1:5000 `

#### API keys / Authentication
None

### Errors
Trivia uses some of the standard HTTP status codes to indicate the success or failure of an API request.
Codes in the category of `2xx` represent `Success`. Codes in the category of `3xx` represent `Redirection`. Codes in the category of `4xx` represent ` Client Error `(i.e error causes by input data). Codes in the category of `5xx` represent `Server Error` (i.e error with Trivia servers)

#### Status codes and messages 
`200` - **OK**   --> Everything went as expected\
`400` - **Bad Request**    --> The request was unacceptable\
`404`  -  **Not Found**    --> Request resouce not found\
`405`  -  **Method Not Allowed**    --> Incorrect HTTP method used for endpoint\
`422`  -  **Unprocessable Entity**   --> Request argument/body syntax is correct, but unable to process it\
`500`  -  **Internal Server Error**   --> Something went wrong with Trivia server

### Resource Endpoint Library
`GET '/api/v1.0/' `
- Welcome Page
- Request Arguments: None
- Returns: An object with a welcome message
#### Sample

URL\
`curl http://127.0.0.1:5000/api/v1.0/`

Response 
```
    {
        "message": "Welcome to Trivia API Home Page"
    }
```
---

`GET '/api/v1.0/categories' `
- This fetches a dictionary of all the categories from the database in which the keys are the ids and the values are the types.
- Request Arguments: None
- Returns: An object with a single key, `categories` that maps to an object of `id: category_type` pairs.

#### Sample
URL\
`curl http://127.0.0.1:5000/api/v1.0/categories`

Response
```
    {
        "categories": {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
        }
    }
```
---
`POST '/api/v1.0/categories' `
- This creates a new category provided it does not alraedy exist
- Request Arguments: An object with a single key `"type" : "type_value"` 
- Returns: An object with a single key of the new category id.

#### Sample
URL\
`curl http://127.0.0.1:5000/api/v1.0/categories -X POST -H "Content-Type:application/json" -d "{\"new_category\" : \"Fashion\"}"`

Response\
`{"category_id": 8}`

---
`GET '/api/v1.0/categories/${category_id}/questions'`
- This fetches all the questions of a particular category. The route variable `category_id` represents the id of the category.
- Request Argument(s): `category_id` - integer
- Returns: An object of three keys. `questions` which maps to the array of all the questions that have a `category` which is equal of `category_id`. `totalQuestions` which maps to the number of items in the `questions` array. `currentCategory` maps to .

#### Sample
URL\
`curl http://127.0.0.1:5000/api/v1.0/categories/2/questions`

Response
```
    {
        "currentCategory": "Art",
        "questions": [
            {
                "answer": "Escher",
                "category": 2,
                "difficulty": 1,
                "id": 16,
                "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?",
                "rating": 1
            },
            {
                "answer": "Mona Lisa",
                "category": 2,
                "difficulty": 3,
                "id": 17,
                "question": "La Giaconda is better known as what?",
                "rating": 1
            },
            {
                "answer": "One",
                "category": 2,
                "difficulty": 4,
                "id": 18,
                "question": "How many paintings did Van Gogh sell in his lifetime?",
                "rating": 1
            },
            {
                "answer": "Jackson Pollock",
                "category": 2,
                "difficulty": 2,
                "id": 19,
                "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?",
                "rating": 1
            }
        ],
        "totalQuestions": 4
    }
```
---
`GET '/api/v1.0/questions?page=${page_no}' `
- This fetches a dictionary of `questions` maps to an array of objects of 10 paginated questions. `categories` maps to an object of all the categories present in the `questions` array. `totalQuestions` maps to the count of all the questions.
- Request Argument(s): `page_no` - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string 

#### Sample
URL\
`curl http://127.0.0.1:5000/api/v1.0/questions?page=1`

Response
```
    {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
        "currentCategory": "",
        "questions": [
            {
                "answer": "Maya Angelou",
                "category": 4,
                "difficulty": 2,
                "id": 5,
                "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
                "rating": 1
            },
            {
                "answer": "Muhammad Ali",
                "category": 4,
                "difficulty": 1,
                "id": 9,
                "question": "What boxer's original name is Cassius Clay?",
                "rating": 1
            },
            {
                "answer": "Apollo 13",
                "category": 5,
                "difficulty": 4,
                "id": 2,
                "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
                "rating": 1
            },
            {
                "answer": "Tom Cruise",
                "category": 5,
                "difficulty": 4,
                "id": 4,
                "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
                "rating": 1
            },
            {
                "answer": "Edward Scissorhands",
                "category": 5,
                "difficulty": 3,
                "id": 6,
                "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
                "rating": 1
            },
            {
                "answer": "Brazil",
                "category": 6,
                "difficulty": 3,
                "id": 10,
                "question": "Which is the only team to play in every soccer World Cup tournament?",
                "rating": 1
            },
            {
                "answer": "Uruguay",
                "category": 6,
                "difficulty": 4,
                "id": 11,
                "question": "Which country won the first ever soccer World Cup in 1930?",
                "rating": 1
            },
            {
                "answer": "George Washington Carver",
                "category": 4,
                "difficulty": 2,
                "id": 12,
                "question": "Who invented Peanut Butter?",
                "rating": 1
            },
            {
                "answer": "Lake Victoria",
                "category": 3,
                "difficulty": 2,
                "id": 13,
                "question": "What is the largest lake in Africa?",
                "rating": 1
            },
            {
                "answer": "The Palace of Versailles",
                "category": 3,
                "difficulty": 3,
                "id": 14,
                "question": "In which royal palace would you find the Hall of Mirrors?",
                "rating": 1
            }
        ],
        "totalQuestions": 19
    }
```
---
`POST '/api/v1.0/questions'`
- Sends a request to create a new question.
- Request Body: An object of question with `"question": "question_value"` key:value pairs
- Returns: An object with a single value of the question id

#### Sample
URL\
`curl http://127.0.0.1:5000/api/v1.0/questions -X POST -H "Content-Type:application/json" -d "{\"question\": \"What is the capital of Finland\",\"answer\": \"Helsinki\",\"category\": 3,\"difficulty\": 2,\"rating\":4}"`

Response\
`{"question_id": 24}`

---
`POST '/api/v1.0/questions'`
- Sends a request to search for a question.
- Request Body: An object with `"searchTerm": "searchTerm_value"`  key:value pair
- Returns: An object with a current category, an array of questions that matched the search term (case insensitive), current category string and total number of questions returned

#### Sample
URL\
`curl http://127.0.0.1:5000/api/v1.0/questions -X POST -H "Content-Type:application/json" -d "{\"searchTerm\": \"title of the 1990 fantasy\"}"`

Response
```
    {
        "currentCategory": "",
        "questions": [
            {
                "answer": "Edward Scissorhands",
                "category": 5,
                "difficulty": 3,
                "id": 6,
                "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
                "rating": 1
            }
        ],
        "totalQuestions": 1
    }
```
---
`POST '/api/v1.0/quizzes'`
- Fetches a random question from a given category provided it is not part of the previous three questions
- Request Body:  An object of the quiz category and an array of the previous three questions
- Returns: An single object of a random question in the given category

#### Sample
URL\
`curl http://127.0.0.1:5000/api/v1.0/quizzes -X POST -H "Content-Type: application/json" -d "{\"previous_questions\" : [4, 6, 12],\"quiz_category\" : \"Science\"}"`

Response 
```
   {
        "question": {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?",
            "rating": 1
        }
    }
```

### Deployment
None

### Authors
Udacity\
Ibeh Esther





