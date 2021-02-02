from flask import Flask, request
from flask import jsonify
from worker import celery

dev_mode = True
app = Flask(__name__)


@app.route('/api/lisa-analysis/success/<string:task_id>', methods=['POST'])
def analysis_complete(task_id: str) -> str:
    """ 
    On POST, a lisa task_id is parsed form the route URL and response.data is checked for analysis results.
    If analysis data is present, a celery task is created to handle the processing of the LiSa analysis 
    result data for the corresponding MalwarePayload.

    Args:
        task_id (str): The LiSa task_id referencing to a specific MalwarePayload

    Returns:
        str: Success/failure response message
    """
    analysis_data = request.json

    if analysis_data:
        celery.send_task('tasks.lisa_analysis_success', args=[task_id, analysis_data], kwargs={})
        return jsonify("Status update received"), 200
    else:
        return jsonify("No analysis data provided"), 400


@app.route('/api/lisa-analysis/failure/<string:task_id>', methods=['POST'])
def analysis_failed(task_id: str) -> BaseResponse:
    """ 
    On POST, a lisa task_id is parsed form the route URL and response.data is checked for failure data.
    If failure data is present, a celery task is created to handle the failed LiSa analysis attempt 
    for the corresponding MalwarePayload.

    Args:
        task_id (str): The LiSa task_id referencing a specific MalwarePayload

    Returns:
        str: Success/failure response message
    """
    failure_data = request.json

    if failure_data:
        celery.send_task('tasks.lisa_analysis_failed', args=[task_id, failure_data], kwargs={})
        return jsonify("Status update received"), 200
    else:
        return jsonify("No failure data provided")


@app.route('/api/ping')
def health_check() -> str:
    """
    Used as a health-check end-point to verify if the Flask application is running.

    Returns:
        str: Responds with HTTP Status Code 200 if Flask server is online.
    """
    return jsonify("OK"), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001')
