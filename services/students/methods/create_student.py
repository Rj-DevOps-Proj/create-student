from flask import Blueprint, current_app, jsonify, request

from ..db import INTEGRITY_ERRORS, connect, execute, validate_student_payload


def create_student_blueprint():
    blueprint = Blueprint("create_student", __name__)

    @blueprint.route("/students", methods=["POST"])
    def create_student():
        payload = request.get_json(silent=True)
        data, error = validate_student_payload(payload)
        if error:
            return jsonify(error[0]), error[1]

        database_url = current_app.config["DATABASE_URL"]
        connection = connect(database_url)
        try:
            cursor = execute(
                connection,
                "INSERT INTO students (name, email, grade) VALUES (%s, %s, %s) RETURNING id",
                (data["name"], data["email"], data["grade"]),
            )
            student_id = cursor.fetchone()["id"]
            connection.commit()
        except INTEGRITY_ERRORS:
            return jsonify({"error": "A student with that email already exists."}), 400
        finally:
            connection.close()

        return jsonify({"id": student_id, **data}), 201

    return blueprint
