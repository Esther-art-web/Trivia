import os
from flask import Flask, request, abort, jsonify, json
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    url = '/api/*'
    cors = CORS(app, resources = {url: {'origins' : '*'}})

    
    # @TODO: Use the after_request decorator to set Access-Control-Allow
    
    # @app.after_request
    # def after_request(response):
    #     response.headers.add("Access-Control-Allow-Origin", "*")
    #     response.headers.add("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
    #     response.headers.add("Access-Control-Allow-Headers", 'Content-Type')

    # """
    # @TODO:
    # Create an endpoint to handle GET requests
    # for all available categories.
    # """

    @app.route('/categories')
    def get_categories(): 
        try:
            all_categories = Category.query.all()
            categories = {}
            for index in range(len(all_categories)):
                category = all_categories[index]
                categories[category.id] = category.type
        except Exception:
            abort(405)        
        return jsonify({"categories" : categories})

    # """
    # @TODO:
    # Create an endpoint to handle GET requests for questions,
    # including pagination (every 10 questions).
    # This endpoint should return a list of questions,
    # number of total questions, current category, categories.

    @app.route('/questions')
    def get_questions_by_page():
        try:
            page = int(request.args.get('page', 1))
            QUESTIONS_PER_PAGE = 10
            all_questions = Question.query.all()
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
            page_questions = all_questions[start : end]
            questions = []
            categories = {}
            if page_questions:
                for page_question in page_questions:
                    question = {
                        'id' : page_question.id,
                        'question' : page_question.question,
                        'answer' : page_question.answer,
                        'difficulty' : page_question.difficulty,
                        'category' : page_question.category
                    }
                    category = Category.query.get(page_question.category)
                    categories[page_question.category] = category.type
                    questions.append(question)
            else:
                abort(404)
        except Exception:
            abort(404)
        return jsonify({
            'questions' : questions,
            'totalQuestions' : len(all_questions),
            'categories' : categories
            })

    # TEST: At this point, when you start the application
    # you should see questions and categories generated,
    # ten questions per page and pagination at the bottom of the screen for three pages.
    # Clicking on the page numbers should update the questions.
    # """


    # """
    # @TODO:
    # Create an endpoint to DELETE question using a question ID.

    @app.route('/questions/<int:question_id>', methods =['DELETE'])
    def delete_question(question_id):
        res_question_id = None
        try:
            question = Question.query.get(question_id)
            res_question_id = question.id
            question.delete()
        except Exception:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()    
        return jsonify({'question_id' : res_question_id})


    # TEST: When you click the trash icon next to a question, the question will be removed.
    # This removal will persist in the database and when you refresh the page.
    # """

    # """
    # @TODO:
    # Create an endpoint to POST a new question,
    # which will require the question and answer text,
    # category, and difficulty score.

    @app.route('/questions', methods = ['POST'])
    def create_new_question_and_search_question():
        res_question_id=None
        body=request.get_json()
        if body.get('searchTerm'):
            search_term = body.get('searchTerm')
            questions = Question.query.filter(Question.question.ilike('%'+search_term+'%')).all()
            res = []
            if questions:
                for question in questions:
                    _question = {
                        'id' : question.id,
                        'question' : question.question,
                        'answer' : question.answer,
                        'difficulty' : question.difficulty,
                        'category' : question.category
                    }
                    res.append(_question)

            else:
                abort(404)        
                
            return jsonify({
                'questions' : res, 
                'totalQuestions' : len(questions),
                'currentCategory' : 'Entertainment'
                })
        else:     
            try:
                question = Question(
                    question=body.get('question'),
                    answer=body.get('answer'),
                    category= body.get('category'),
                    difficulty=body.get('difficulty')
                    )
                question.insert()
                res_question_id = question.id
                
            except Exception:
                db.session.rollback()
                abort(400)
            finally:
                db.session.close()    
            return jsonify({
                'question_id' : res_question_id
            })
    
    # TEST: When you submit a question on the "Add" tab,
    # the form will clear and the question will appear at the end of the last page
    # of the questions list in the "List" tab.
    # """

    # """
    # @TODO:
    # Create a POST endpoint to get questions based on a search term.
    # It should return any questions for whom the search term
    # is a substring of the question.

    # 
    # TEST: Search by any phrase. The questions list will update to include
    # only question that include that string within their question.
    # Try using the word "title" to start.
    # """

    # """
    # @TODO:
    # Create a GET endpoint to get questions based on category.
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        category = Category.query.get(category_id)
        if category:
            questions = Question.query.filter_by(category = category_id).all()
            res = []
            for question in questions:
                    _question = {
                        'id' : question.id,
                        'question' : question.question,
                        'answer' : question.answer,
                        'difficulty' : question.difficulty,
                        'category' : question.category
                    }
                    res.append(_question)
        else:
            abort(404)
        return jsonify({
            'questions' : res,
            'totalQuestions' : len(questions),
            'currentCategory' : 'History'
            })
    # TEST: In the "List" tab / main screen, clicking on one of the
    # categories in the left column will cause only questions of that
    # category to be shown.
    # """

    # """
    # @TODO:
    # Create a POST endpoint to get questions to play the quiz.
    # This endpoint should take category and previous question parameters
    # and return a random question within the given category,
    # if provided, and that is not one of the previous questions.
    @app.route('/quizzes', methods = ['POST'])
    def get_quizzes():
        try:
            body = request.get_json()
            prev_questions = body.get('previous_questions')
            quiz_category = body.get('quiz_category')
            category = Category.query.filter_by(type=quiz_category).one_or_none()
            if category:
                questions_in_category = Question.query.filter_by(category = category.id).all()
                selected_question = random.choice(questions_in_category)
                while selected_question.id in prev_questions:
                    selected_question = random.choice(questions_in_category)
                else: 
                    res = {
                        'id' : selected_question.id,
                        'question' : selected_question.question,
                        'answer' : selected_question.answer,
                        'difficulty' : selected_question.difficulty,
                        'category' : selected_question.category
                    }
            else:
                abort(404)
        except Exception:
            abort(404)
        return jsonify({'question' : res})    

    # TEST: In the "Play" tab, after a user selects "All" or a category,
    # one question at a time is displayed, the user is allowed to answer
    # and shown whether they were correct or not.
    # """

    @app.route('/')
    def index():
        return jsonify({
            'Success' : True
        })
    # """
    # @TODO:
    # Create error handlers for all expected errors
    # including 404 and 422.
    # """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success' : False,
            'error' : 400,
            'message' : 'Bad Request'
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success' : False,
            'error' : 404,
            'message' : 'Not Found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success' : False,
            'error' : 405,
            'message' : 'Method Not Allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success' : False,
            'error' : 422,
            'message' : 'Unprocessable Entity'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success' : False,
            'error' : 500,
            'message' : 'Internal Server Error'
        }), 500 

    return app
if __name__ == '__main__':
    app = create_app()
    app.run()

