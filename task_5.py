import shlex

@app.route('/ps')
def ps():
    args = request.args.getlist('arg')
    quoted_args = [shlex.quote(arg) for arg in args]
    command = ['ps'] + args
    result = subprocess.run(command, capture_output=True, text=True)
    return f"<pre>{result.stdout}</pre>"
