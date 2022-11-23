from flask import Flask
from main.view import main_blueprint

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

app.register_blueprint(main_blueprint)

@app.errorhandler(404)
def error_page_404(err):
    return f"Страница не найдена. Проверьте данные в запросе: '{err}'"

@app.errorhandler(500)
def error_page_500(err):
    return f"Ошибка обработки сервером, данные по запросу не найдены: '{err}'"


if __name__ == '__main__':
    app.run()


