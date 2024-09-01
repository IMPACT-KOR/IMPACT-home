from flask import Flask, request, redirect, url_for, render_template_string, session
import json
import os
from invest_analysis import parse_investment_file, assign_teams, balance_teams

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 세션을 위해 필요한 비밀 키 설정

# JSON 파일에서 사용자 데이터 불러오기
def load_user_data():
    with open('user_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

USER_DATA = load_user_data()

# HTML 템플릿을 문자열로 정의
login_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>
    <form method="POST">
        <div>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
        </div>
        <button type="submit">Login</button>
    </form>
    {% if error %}
    <p style="color: red;">{{ error }}</p>
    {% endif %}
</body>
</html>
'''

dashboard_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
</head>
<body>
    <h2>Dashboard</h2>
    <p>현재 잔액: {{ balance }}</p>
    <form method="POST" action="/invest">
        <div>
            <label for="investee">투자할 사람 이름:</label>
            <input type="text" id="investee" name="investee" required>
        </div>
        <div>
            <label for="amount">투자 금액:</label>
            <input type="number" id="amount" name="amount" min="0" max="1000" required>
        </div>
        <button type="submit">투자</button>
    </form>
    {% if error %}
    <p style="color: red;">{{ error }}</p>
    {% endif %}
    <form method="POST" action="/logout">
        <button type="submit">투자 종료</button>
    </form>
    {% if is_admin %}
    <form method="GET" action="/log">
        <button type="submit">투자 로그 보기</button>
    </form>
    <form method="POST" action="/clear_log">
        <button type="submit">로그 초기화</button>
    </form>
    {% endif %}
    <h3>팀 배정</h3>
    <form method="POST" action="/assign_teams">
        <div>
            <label for="team_count">팀 수 입력:</label>
            <input type="number" id="team_count" name="team_count" required>
        </div>
        <button type="submit">팀 배정</button>
    </form>
</body>
</html>
'''

log_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Investment Log</title>
</head>
<body>
    <h2>Investment Log</h2>
    <pre>{{ log_content }}</pre>
    <a href="{{ url_for('dashboard') }}">돌아가기</a>
</body>
</html>
'''

team_assignment_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Team Assignment</title>
</head>
<body>
    <h2>팀 배정 결과</h2>
    {% for team, members in teams.items() %}
        <h3>{{ team }} 팀</h3>
        <p>{{ ', '.join(members) }}</p>
    {% endfor %}
    <a href="{{ url_for('dashboard') }}">돌아가기</a>
</body>
</html>
'''

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USER_DATA and USER_DATA[username] == password:
            session['username'] = username
            session['balance'] = 1000  # 초기 잔액 설정
            session['is_admin'] = (username == 'admin')  # 관리자인지 여부를 세션에 저장
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid Credentials. Please try again."
    return render_template_string(login_template, error=error)

@app.route('/invest', methods=['POST'])
def invest():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    investee = request.form['investee']
    amount = int(request.form['amount'])
    
    # Ensure the investee exists in the user data
    if investee not in USER_DATA:
        session['error'] = "투자할 사용자가 존재하지 않습니다."
        return redirect(url_for('dashboard'))

    # Ensure the user has enough balance to invest
    if session['balance'] < amount:
        session['error'] = "잔액이 부족합니다."
        return redirect(url_for('dashboard'))
    
    # Deduct the amount from the user's balance
    session['balance'] -= amount
    
    # Log the investment in the specified format
    log_entry = f"ID: {username}, 투자 대상: {investee}, 투자 금액: {amount}\n"
    with open('investment_log.txt', 'a', encoding='utf-8') as f:
        f.write(log_entry)
    
    session['error'] = f"{investee}에게 {amount} 포인트를 성공적으로 투자했습니다."
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    error = session.pop('error', None)
    is_admin = session.get('is_admin', False)
    return render_template_string(dashboard_template, balance=session['balance'], error=error, is_admin=is_admin)

@app.route('/log')
def view_log():
    if 'username' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    if not os.path.exists('investment_log.txt'):
        log_content = "No investment log available."
    else:
        with open('investment_log.txt', 'r', encoding='utf-8') as f:
            log_content = f.read()
    
    return render_template_string(log_template, log_content=log_content)

@app.route('/clear_log', methods=['POST'])
def clear_log():
    if 'username' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    open('investment_log.txt', 'w').close()  # 파일 내용을 비움
    session['error'] = "로그가 초기화되었습니다."
    return redirect(url_for('dashboard'))

@app.route('/assign_teams', methods=['POST'])
def assign_teams_route():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        team_count = int(request.form['team_count'])
        investment_data = parse_investment_file('investment_log.txt')
        teams = assign_teams(investment_data, team_count)
        balanced_teams = balance_teams(teams)
        return render_template_string(team_assignment_template, teams=balanced_teams)
    except Exception as e:
        session['error'] = str(e)
        return redirect(url_for('dashboard'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('balance', None)
    session.pop('is_admin', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4027)
