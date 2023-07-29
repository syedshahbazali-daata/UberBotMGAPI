from flask import Flask, jsonify
import json
from datetime import datetime

app = Flask(__name__)


def get_data_from_json():
    with open(f"users-data.json", "r", encoding='utf-8') as f:
        config = json.load(f)
    return config


# REST API
@app.route("/")
def index():
    return "Hello World"


@app.route("/api/users")
def get_users():
    try:
        return jsonify(get_data_from_json())
    except Exception as e:
        return {"status": "error",
                "message": str(e)}


@app.route("/api/create_user/<email>/<company>")
def create_user(email, company):
    if "@" not in email:
        return {"status": "error"}

    already_emails_list = get_data_from_json()
    already_emails_list = [i['email'] for i in already_emails_list]
    if email in already_emails_list:
        return {"message": "email already registered"}

    user_email = email
    company_name = company
    current_date = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
    joining_date = ""

    record = {
        "email": user_email,
        "company": company_name,
        "current_date": current_date,
        "joining_date": joining_date,
    }

    # add into users data
    with open(f"users-data.json", "r", encoding='utf-8') as f:
        config = json.load(f)

    config.append(record)

    with open(f"users-data.json", "w", encoding='utf-8') as f:
        json.dump(config, f, indent=4)

    return {"status": "success"}


@app.route("/api/update_user/<email>")
def update_user(email):
    if "@" not in email:
        return {"message": "wrong email"}

    users_data = get_data_from_json()
    current_date = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
    for single_user_data in users_data:
        if single_user_data['email'] == email:

            if single_user_data['joining_date'] != "":
                return {"message": "already join"}

            single_user_data['joining_date'] = current_date
            with open(f"users-data.json", "w", encoding='utf-8') as f:
                json.dump(users_data, f, indent=4)

            return {"message": "success"}

    return {"message": "email not found"}


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
