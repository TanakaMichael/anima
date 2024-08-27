from flask import Blueprint, request
import subprocess
import os

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data is None:
        return "Invalid data", 400
    
    print(data)
    
    if data.get('ref') == 'refs/heads/master':
        try:
            result = subprocess.run(['/usr/bin/git', 'pull'], cwd='/home/ubuntu/myflaskapp', check=True, capture_output=True, text=True)
            print(f"Git pull output: {result.stdout}")
            print(f"Git pull error: {result.stderr}")
            env = os.environ.copy()
            env['PATH'] = '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
            try:
                result = subprocess.run(
                    ['/bin/systemctl', 'restart', 'myflaskapp'],
                    cwd='/home/ubuntu/myflaskapp',
                    check=True,
                    capture_output=True,
                    text=True,
                    env=env
                )
                print(f"Service restart succeeded: {result.stdout}")
            except subprocess.CalledProcessError as e:
                print(f"Service restart failed: {e.stderr}")
            return "Success", 200
        except subprocess.CalledProcessError as e:
            print(f"Error during webhook processing: {e}")
            print(f"Git pull output: {e.output}")
            print(f"Git pull stderr: {e.stderr}")
            return f"Error during webhook processing: {str(e)}", 500
    else:
        return "No action needed", 200
