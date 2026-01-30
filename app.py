from flask import Flask, render_template, redirect, url_for, request, jsonify
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

# Project-level deliverables (각 프로젝트별 산출물 커스터마이징)
PROJECT_DELIVERABLES = {}

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

@app.route('/projects')
def projects():
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
        'projects.html',
        menu_name='projects',
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
    return redirect(url_for('projects'))

@app.route('/project/<int:id>')
def project_detail(id):
    proj = _project_by_id(id)
    if not proj:
        return redirect(url_for('projects'))
    return render_template('project_detail.html', menu_name='projects', project=proj)

@app.route('/deliverables')
def deliverables():
    return render_template('deliverables.html', menu_name='deliverables')


# --- Deliverables baseline (산출물 관리) sample data ---
DELIVERABLES = [
    {
        'id': 'A00', 'code': 'A00', 'title': '프로젝트 착수', 'children': [
            {'id': 'A10', 'code': 'A10', 'title': '요건 수집', 'children': [
                {'id': 'A11', 'code': 'A11', 'title': '요구사항 문서', 'children': []},
                {'id': 'A12', 'code': 'A12', 'title': '이해관계자 목록', 'children': []},
            ]},
            {'id': 'A20', 'code': 'A20', 'title': '초기 검토', 'children': []},
        ]
    },
    {
        'id': 'B00', 'code': 'B00', 'title': '계획 수립', 'children': [
            {'id': 'B10', 'code': 'B10', 'title': '프로젝트 계획서', 'children': []},
            {'id': 'B20', 'code': 'B20', 'title': '리스크 등록부', 'children': []},
        ]
    },
    {
        'id': 'C00', 'code': 'C00', 'title': '실행 및 통제', 'children': [
            {'id': 'C10', 'code': 'C10', 'title': '개발 산출물', 'children': [
                {'id': 'C11', 'code': 'C11', 'title': '설계서', 'children': []},
                {'id': 'C12', 'code': 'C12', 'title': '소스코드', 'children': []},
            ]},
        ]
    },
    {'id': 'D00', 'code': 'D00', 'title': '종료', 'children': []},
    {'id': 'E00', 'code': 'E00', 'title': '개발 산출물', 'children': [
        {'id': 'E10', 'code': 'E10', 'title': '배포 패키지', 'children': []},
    ]},
]


@app.route('/api/deliverables')
def api_deliverables():
    return jsonify(DELIVERABLES)


@app.route('/api/deliverables/update', methods=['POST'])
def api_deliverables_update():
    try:
        data = request.get_json()
    except Exception:
        data = None
    if not isinstance(data, list):
        return jsonify({'ok': False, 'error': 'invalid payload'}), 400
    global DELIVERABLES
    DELIVERABLES = data
    return jsonify({'ok': True})


# Project-level deliverables API
@app.route('/api/project/<int:proj_id>/deliverables')
def api_project_deliverables(proj_id):
    """프로젝트별 산출물 조회. 저장된 내용 또는 베이스라인 반환"""
    if proj_id not in PROJECT_DELIVERABLES:
        # 첫 조회 시 베이스라인 복사
        import copy
        PROJECT_DELIVERABLES[proj_id] = copy.deepcopy(DELIVERABLES)
    return jsonify(PROJECT_DELIVERABLES[proj_id])


@app.route('/api/project/<int:proj_id>/deliverables/update', methods=['POST'])
def api_project_deliverables_update(proj_id):
    """프로젝트별 산출물 업데이트"""
    try:
        data = request.get_json()
    except Exception:
        data = None
    if not isinstance(data, list):
        return jsonify({'ok': False, 'error': 'invalid payload'}), 400
    PROJECT_DELIVERABLES[proj_id] = data
    return jsonify({'ok': True})

@app.route('/menu4')
def menu4():
    return render_template('menu4.html', menu_name='menu4')

@app.route('/menu5')
def menu5():
    return render_template('menu5.html', menu_name='menu5')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
