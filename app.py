from flask import Flask, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

PROJECTS = [
    {'name': '통합 플랫폼 고도화', 'pm': '김철수', 'type': '개발', 'start': '2026-01-02', 'end': '2026-06-30'},
    {'name': '결제 시스템 리뉴얼', 'pm': '이영희', 'type': '개발', 'start': '2026-01-02', 'end': '2026-08-15'},
    {'name': '고객 포털 유지보수', 'pm': '박지민', 'type': '유지보수', 'start': '2026-01-02', 'end': '2026-12-31'},
    {'name': '데이터 마이그레이션', 'pm': '최민수', 'type': '개발', 'start': '2026-01-02', 'end': '2026-09-20'},
    {'name': '인프라 모니터링', 'pm': '정수진', 'type': '유지보수', 'start': '2026-01-02', 'end': '2026-05-31'},
    {'name': '모바일 앱 v2', 'pm': '한동훈', 'type': '개발', 'start': '2026-01-02', 'end': '2026-11-30'},
]

def progress_rate(start_str, end_str):
    try:
        start = datetime.strptime(start_str, '%Y-%m-%d')
        end = datetime.strptime(end_str, '%Y-%m-%d')
        today = datetime.now().date()
        start, end = start.date(), end.date()
        if today <= start:
            return 0
        if today >= end:
            return 100
        total = (end - start).days
        elapsed = (today - start).days
        return round(100 * elapsed / total)
    except Exception:
        return 0

@app.route('/')
def index():
    return redirect(url_for('dashboard'))




@app.route('/dashboard')
def dashboard():
    projects = []
    for i, p in enumerate(PROJECTS, 1):
        proj = dict(p)
        proj['no'] = i
        proj['progress'] = progress_rate(proj['start'], proj['end'])
        projects.append(proj)
    return render_template('dashboard.html', menu_name='dashboard', projects=projects)

@app.route('/menu2')
def menu2():
    return render_template('menu2.html', menu_name='menu2')

@app.route('/menu3')
def menu3():
    return render_template('menu3.html', menu_name='menu3')

@app.route('/menu4')
def menu4():
    return render_template('menu4.html', menu_name='menu4')

@app.route('/menu5')
def menu5():
    return render_template('menu5.html', menu_name='menu5')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
