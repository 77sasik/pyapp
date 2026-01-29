from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime

app = Flask(__name__)

_project_id = 0

def _next_id():
    global _project_id
    _project_id += 1
    return _project_id

def _init_projects():
    global _project_id
    _project_id = 0
    return [
        {'id': _next_id(), 'name': '통합 플랫폼 고도화', 'pm': '김철수', 'type': '개발', 'start': '2026-01-02', 'end': '2026-06-30', 'amount': 12000},
        {'id': _next_id(), 'name': '결제 시스템 리뉴얼', 'pm': '이영희', 'type': '개발', 'start': '2026-01-02', 'end': '2026-08-15', 'amount': 8500},
        {'id': _next_id(), 'name': '고객 포털 유지보수', 'pm': '박지민', 'type': '유지보수', 'start': '2026-01-02', 'end': '2026-12-31', 'amount': 3200},
        {'id': _next_id(), 'name': '데이터 마이그레이션', 'pm': '최민수', 'type': '개발', 'start': '2026-01-02', 'end': '2026-09-20', 'amount': 6000},
        {'id': _next_id(), 'name': '인프라 모니터링', 'pm': '정수진', 'type': '유지보수', 'start': '2026-01-02', 'end': '2026-05-31', 'amount': 2100},
        {'id': _next_id(), 'name': '모바일 앱 v2', 'pm': '한동훈', 'type': '개발', 'start': '2026-01-02', 'end': '2026-11-30', 'amount': 15000},
    ]

PROJECTS = _init_projects()

SORT_KEYS = ('no', 'name', 'pm', 'type', 'start', 'end', 'amount')

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

def _project_by_id(id):
    try:
        k = int(id)
        return next((p for p in PROJECTS if p['id'] == k), None)
    except (TypeError, ValueError):
        return None

@app.route('/menu2')
def menu2():
    sort_key = request.args.get('sort', 'no')
    order = request.args.get('order', 'asc')
    if sort_key not in SORT_KEYS:
        sort_key = 'no'
    if order not in ('asc', 'desc'):
        order = 'asc'
    projects = []
    for i, p in enumerate(PROJECTS, 1):
        proj = dict(p)
        proj['no'] = i
        projects.append(proj)
    def key_fn(p):
        if sort_key == 'no':
            return (0, p.get('no', 0))
        if sort_key == 'amount':
            return (0, p.get('amount', 0))
        k = p.get(sort_key)
        if k is None:
            return (1, '')
        return (0, str(k))
    projects.sort(key=key_fn, reverse=(order == 'desc'))
    for i, p in enumerate(projects, 1):
        p['no'] = i
    total_amount = sum(p.get('amount', 0) for p in PROJECTS)
    return render_template(
        'menu2.html',
        menu_name='menu2',
        projects=projects,
        total_amount=total_amount,
        sort_key=sort_key,
        order=order,
    )

@app.route('/projects/add', methods=['POST'])
def projects_add():
    name = request.form.get('name', '').strip()
    pm = request.form.get('pm', '').strip()
    ptype = request.form.get('type', '개발')
    start = (request.form.get('start') or '')[:10]
    end = (request.form.get('end') or '')[:10]
    try:
        amount = int(request.form.get('amount') or 0)
    except (TypeError, ValueError):
        amount = 0
    if name and start and end:
        PROJECTS.append({
            'id': _next_id(), 'name': name, 'pm': pm, 'type': ptype,
            'start': start, 'end': end, 'amount': amount,
        })
    return redirect(url_for('menu2'))

@app.route('/project/<int:id>')
def project_detail(id):
    proj = _project_by_id(id)
    if not proj:
        return redirect(url_for('menu2'))
    return render_template('project_detail.html', menu_name='menu2', project=proj)

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
