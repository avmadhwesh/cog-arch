from flask import Flask, request, jsonify
import logging
import datetime
from pathlib import Path
import json
import os
from werkzeug.middleware.proxy_fix import ProxyFix

def mkdirp(p):
    return Path(p).mkdir(exist_ok=True, parents=True)

app = Flask("experiments")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1) # for accurate ip address logging
app.logger.setLevel(logging.INFO)
logger = logging.getLogger("experiments")

# make data directory
data_dir_path = Path(os.environ.get("DATA_DIRECTORY", "data"))
logger.info(f"Using {data_dir_path} to save data.")

def save_dict(directory_path, file_ident: str, content: dict):
    basename = str(datetime.datetime.now().isoformat()) + " " + str(file_ident) + ".json"
    savefilepath = directory_path / basename
    savefilepath.write_text(json.dumps(content))
    return jsonify({"status": "success"})

def register_experiment(experiment_name):

    exp_dir_path = data_dir_path / experiment_name
    mkdirp(exp_dir_path)

    @app.route(f"/api/{experiment_name}/save", methods=["POST"])
    def save_function():
        req_data = request.json
        participant_number = req_data["participantNumber"]
        experiment_data = req_data["data"]
        logger.info(f"{participant_number} has started the experiment.")
        experiment_data_dir_path = exp_dir_path / "experiment"
        mkdirp(experiment_data_dir_path)
        return save_dict(experiment_data_dir_path, str(participant_number), experiment_data)

    @app.route(
        f"/api/{experiment_name}/consent", methods=["POST"]
    )
    def consent_function():
        req_data = request.json
        participant_number = req_data["participantNumber"]
        consent_data = req_data["data"]
        logger.info("%s has started the experiment.", participant_number)
        consent_data_dir_path = exp_dir_path / "consent"
        mkdirp(consent_data_dir_path)
        return save_dict(consent_data_dir_path, str(participant_number), consent_data)

    @app.route(f"/api/{experiment_name}/log", methods=["POST"])
    def log_function():
        req_data = request.json
        participant_number = req_data["participantNumber"]
        message = req_data["message"]
        logger.info("%s|%s: %s", request.remote_addr, participant_number, message)
        return jsonify({"status": "success"})

register_experiment("clustering")
