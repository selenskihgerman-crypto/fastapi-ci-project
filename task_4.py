import subprocess

@app.route('/uptime', methods=['GET'])
def uptime():
    result = subprocess.run(['uptime', '-p'], capture_output=True, text=True)
    uptime_text = result.stdout.strip()
    return f"Current uptime is {uptime_text}"
