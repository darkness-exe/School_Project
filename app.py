from flask import Flask, render_template, request, session, redirect,url_for #Импортирование инструментов flask 
"""
    Flask - это базовая функция, которая позволяет создавать веб-приложения.
    render_template - возвращает веб-страницу, которую пользователь увидит в браузере.
    request - хранит информацию о том, что пользователь запросил на сервере.
    session - позволяет сохранять информацию между посещениями веб-сайта.
    redirect - отправляет пользователя на другую страницу.
    url_for - помогает создавать ссылки на разные страницы в приложении."""
from email.mime.text import MIMEText #Импотируем модули для отправки сообщений на почту 
from email.mime.multipart import MIMEMultipart #Импотируем модули для отправки сообщений на почту 
import smtplib #Имортируем модуль для установки соединения с сервером SMTP и отправки сообщения.
import sqlite3 #Импортируем модуль для взаимодействовать с базами данных SQLite
import secrets #Импортриуем модуль для для генерации безопасного токена для URL
import logging #Импортриуем модуль для отслеживания действий программы


app = Flask(__name__, static_folder='static')#Создаем  веб-приложение с именем "app" и указываем где хранятся статические файлы
app.secret_key = 'secret_key' #Устанавливаем секртеный ключ для шифрования данных 
logging.basicConfig(level=logging.INFO) #Информация о том что происходит на сервере 
logger = logging.getLogger(__name__) #Информация о том что происходит на сервере 

DATABASE_NAME = 'DATABASE.db' #Создаем переменую с именем для базы данных 
conn = sqlite3.connect(DATABASE_NAME) #Создаем переменую которая будет соеденить нас с базой данных
cur = conn.cursor() #Создаем обьект для выполнения SQL запросов



def send_email(receiver_email , name, email, result_proc):
    """Функция для отправки сообщений на почту пользователя"""

    sender_email = "shcoolprojecttest@gmail.com" #логин почты для отправки сообщений пользователям
    password = "lhui zagv izzz yrni" #пароль почты для отправки сообщений пользователям
    subject = "Результаты теста" #заголовок сообщения
    body = f"Привет {name}. Тест успешно прошел {name_user} {surname} на {result_proc}"#Текст сообещения

    message = MIMEMultipart() #Обьект для отправки писем
    message["From"] = sender_email #адрес отправителя письма
    message["To"] = receiver_email #адрес получателя письма
    message["Subject"] = subject #заголовок письма

    # Добавляем текст письма
    message.attach(MIMEText(body, "plain"))

    # Устанавливаем соединение с SMTP-сервером Gmail (в данном случае)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        # Начинаем шифрованное соединение
        server.starttls()
        
        # Логинимся в аккаунт
        server.login(sender_email, password)
        
        # Отправляем письмо
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Письмо отправлено успешно!")



def creation_of_databases_6_questions(cur):
    """Функция создание таблицы в базе данных для хранения информации о тесте"""
    cur.execute('''
            CREATE TABLE IF NOT EXISTS test (
                    id INTEGER PRIMARY KEY,
                    token_url TEXT NOT NULL,
                    question_1 TEXT NOT NULL,
                    answer_options1_1 TEXT NOT NULL,
                    answer_options2_1 TEXT NOT NULL,
                    answer_options3_1 TEXT NOT NULL,
                    answer_1 TEXT NOT NULL,
                    question_2 TEXT NOT NULL,
                    answer_options1_2 TEXT NOT NULL,
                    answer_options2_2 TEXT NOT NULL,
                    answer_options3_2 TEXT NOT NULL,
                    answer_2 TEXT NOT NULL,
                    question_3 TEXT NOT NULL,
                    answer_options1_3 TEXT NOT NULL,
                    answer_options2_3 TEXT NOT NULL,
                    answer_options3_3 TEXT NOT NULL,
                    answer_3 TEXT NOT NULL,
                    question_4 TEXT NOT NULL,
                    answer_options1_4 TEXT NOT NULL,
                    answer_options2_4 TEXT NOT NULL,
                    answer_options3_4 TEXT NOT NULL,
                    answer_4 TEXT NOT NULL,
                    question_5 TEXT NOT NULL,
                    answer_options1_5 TEXT NOT NULL,
                    answer_options2_5 TEXT NOT NULL,
                    answer_options3_5 TEXT NOT NULL,
                    answer_5 TEXT NOT NULL,
                    question_6 TEXT NOT NULL,
                    answer_options1_6 TEXT NOT NULL,
                    answer_options2_6 TEXT NOT NULL,
                    answer_options3_6 TEXT NOT NULL,
                    answer_6 TEXT NOT NULL,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL
            )
    ''')
    conn.commit() 
    conn.close()

def creation_of_answer_user(cur):
    """Функция создание таблицы в базе данных для хранения информации о прохождения теста"""
    cur.execute('''
        CREATE TABLE IF NOT EXISTS answer (
            id INTEGER PRIMARY KEY,
            answer_user_1 TEXT NOT NULL,
            answer_user_2 TEXT NOT NULL,
            answer_user_3 TEXT NOT NULL,
            answer_user_4 TEXT NOT NULL,
            answer_user_5 TEXT NOT NULL,
            answer_user_6 TEXT NOT NULL,
            token TEXT NOT NULL,
            name_user TEXT NOT NULL
        )
    ''')



@app.route("/")
def home():
    """Создание домашний страницы"""

    #Создаем token для теста
    token = secrets.token_urlsafe(6) 
    return render_template("index.html" , token=token) 


@app.route('/loging', methods=['GET', 'POST']) # Указываем маршрут '/loging' и методы GET и POST
def loging():
    """Созданию страницу для регистрация пользователя"""

    # Проверяем, если запрос был методом POST
    if request.method == 'POST':
        # Получаем данные из формы запроса
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        
        # Сохраняем данные в сессии
        session['email'] = email 
        session['name'] = name
        session['password'] = password 

     # Проверяем, есть ли данные о пользователе в сессии
    if 'name' in session and 'email' in session and 'password' in session:
        # Если данные есть, получаем имя пользователя из сессии и отображаем профиль
        name = session['name']
        return render_template('profile.html', name=name)
    else:
        # Если данных о пользователе нет, отображаем страницу входа
        return render_template('loging.html')


@app.route('/profile')
def profile():
    """Созданием страницу для отрисовки профиля пользователя"""

    # Получаем данные из сессии
    email = session.get('email')
    name = session.get('name')
    password = session.get('password')
    
    # Проверяем, есть ли данные в сессии
    if email and name and password:
        # Если данные есть, отображаем профиль пользователя
        return render_template('log_profile.html', email= email, name=name)
    else:
        # Если данных нет, перенаправляем на страницу входа
        return redirect(url_for("loging"))



@app.route('/test/<token>', methods=['GET', 'POST'])
def testtt(token):
    if session.get('name') is None:
        return redirect(url_for("loging"))
    else:
        try:
            name = session.get('name')
            email = session.get('email')

            if request.method == 'POST':
                test_data_q = [token]
                for i in range(1, 7):
                    question = request.form.get(f'question__{i}')
                    options = [request.form.get(f'q{i}_{j}_text') for j in range(1, 4)]
                    test_data_q.extend([question] + options)
                states = [request.form[f'q{i}'] for i in range(1, 7)]
                input_texts = [request.form.get(f'{state}_text', '') for state in states]
                test_data_input = input_texts
                test_data_q += test_data_input + [name, email ]         

                conn = get_db_connection()
                try:
                    conn.execute('''
                        INSERT INTO test (
                            token_url,
                            question_1, answer_options1_1, answer_options2_1, answer_options3_1, 
                            question_2, answer_options1_2, answer_options2_2, answer_options3_2, 
                            question_3, answer_options1_3, answer_options2_3, answer_options3_3, 
                            question_4, answer_options1_4, answer_options2_4, answer_options3_4, 
                            question_5, answer_options1_5, answer_options2_5, answer_options3_5, 
                            question_6, answer_options1_6, answer_options2_6, answer_options3_6,
                            answer_1 ,answer_2 ,answer_3 ,answer_4 ,answer_5 ,answer_6 ,
                            name, email
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', test_data_q)
                    conn.commit()
                    logger.info("Test data inserted successfully.")
                except Exception as e:
                    conn.rollback()
                    logger.error(f"Error inserting test data: {e}")
                finally:
                    conn.close()

                return render_template('test_created.html', token=token, name=name, email=email)
            
            return render_template('create_test.html', token=token)

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return "An error occurred", 500





@app.route('/views/<token>', methods=['GET', 'POST'])
def view_test(token):
    global name_user, surname, result_proc
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM test WHERE token_url=?", (token,))
    data = cur.fetchone()
    
    if not data:
        return "Тест с указанным токеном не найден"

    answers = [data[i] for i in range(6, 32, 5)]
    conn.close()

    if request.method == "POST":
        name_user = request.form.get("name_user")
        surname = request.form.get('surname')
        user_answers = [request.form.get(f'answer_{i}') for i in range(1, 7)]
        correct_answers = answers
        results = [1 if user_answer == correct_answer else 0 for user_answer, correct_answer in zip(user_answers, correct_answers)]
        full_name = f"{name_user} {surname}"

        print(*results, token, full_name)
        try:
            conn = get_db_connection()
            conn.execute("""INSERT INTO answer (
                        answer_user_1, answer_user_2, answer_user_3, answer_user_4, answer_user_5, answer_user_6, token, name_user)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (*results, token, full_name))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print("Ошибка при записи ответов в базу данных:", e)

        result = sum(results)
        result_proc = (result/6)*100
        result_proc = ("Процент правильных ответов: {:.2f}%".format(result_proc))
        email = session.get('email')
        name = session.get('name')
        receiver_email = email
        send_email(receiver_email , name,email,result_proc)
        return render_template("passed_test.html", name_user=name_user, result=result)
        return f'Поздравляем, {name_user}! Вы прошли тест. Вы ответили правильно на {result} вопросов из 6.'
    return render_template('view_test.html', data=data)

@app.route("/views_test", methods=['GET', 'POST'])
def views_test():
    if request.method == 'POST':
        token = request.form['token']  # Получаем токен из формы
        return redirect(url_for("view_test", token=token))

    return render_template("views_test.html")

def get_db_connection():
    return sqlite3.connect(DATABASE_NAME)

def main():
    """Функция для запуска всех функций"""
    with get_db_connection() as conn:
        conn = sqlite3.connect(DATABASE_NAME)
        cur = conn.cursor()
        creation_of_databases_6_questions(cur=cur)
        creation_of_answer_user(cur=cur)

if __name__ == '__main__':
    main()
    app.run(debug=True)
