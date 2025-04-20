from flask import Flask, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

class CodeExecForm(FlaskForm):
    code = StringField('Python code', validators=[DataRequired()])
    timeout = IntegerField('Timeout', validators=[DataRequired(), NumberRange(min=1, max=30)])

@app.route('/execute', methods=['POST'])
def execute_code():
    form = CodeExecForm()
    if not form.validate_on_submit():
        return jsonify({'error': 'Invalid input', 'messages': form.errors}), 400

    code = form.code.data
    timeout = form.timeout.data

    # Безопасный запуск с ограничением ресурсов
    cmd = [
        'prlimit',
        '--nproc=1:1',
        'python3', '-c', code
    ]

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        try:
            out, err = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            out, err = proc.communicate()
            return jsonify({'error': 'Timeout', 'output': out, 'stderr': err}), 408
        return jsonify({'output': out, 'stderr': err, 'returncode': proc.returncode})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500
