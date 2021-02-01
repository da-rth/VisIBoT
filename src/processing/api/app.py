import celery.states as states
from flask import Flask, request
from flask import url_for, jsonify
from worker import celery

dev_mode = True
app = Flask(__name__)

@app.route('/api/lisa-analysis/success/<string:task_id>', methods = ['POST'])
def analysis_complete(task_id: str) -> str:
    analysis_data = request.json

    if analysis_data:
        celery.send_task('tasks.lisa_analysis_success', args=[task_id, analysis_data], kwargs={})
        return jsonify("Status update received"), 200
    else:
        return jsonify("No analysis data provided"), 400


@app.route('/api/lisa-analysis/failure/<string:task_id>', methods = ['POST'])
def analysis_failed(task_id: str) -> str:
    failure_data = request.json

    if failure_data:
        celery.send_task('tasks.lisa_analysis_failed', args=[task_id, failure_data], kwargs={})
        return jsonify("Status update received"), 200
    else:
        return jsonify("No failure data provided")


@app.route('/api/ping')
def health_check() -> str:
    return jsonify("OK"), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001')
