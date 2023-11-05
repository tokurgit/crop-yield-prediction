import logging
import numpy as np
import pickle
from flask import Flask, Response
from flask import request
from flask import jsonify
from serializer import CropDataSchema
from marshmallow.exceptions import ValidationError


model_file_name = "model.bin"
app = Flask("crop_yield")
logger = logging.getLogger(__name__)

# Open model_file and instruct that we will "rb" = Read Bytes
with open(model_file_name, "rb") as f_in:
    # Need also DictVectorizer, otherwise won't be able to translate a customer to feature matrix
    dv, model = pickle.load(f_in)


@app.route("/", methods=["GET"])
def health_check() -> Response:
    return jsonify({"status": "LIVE"})


def predict_crop_yield(field_data: dict) -> int:
    logger.info("Predicting yield for field data")

    X = dv.transform([field_data])
    y_pred = model.predict(X)
    predicted_yield = np.expm1(y_pred)

    logger.info("Successfully predicted yield")
    return predicted_yield[0].round(2)


@app.route("/predict", methods=["POST"])
def predict() -> Response:
    try:
        field_data = request.get_json()
        # validate incoming data
        CropDataSchema().load(field_data)
    except ValidationError as exc:
        logger.error(f"Incorrect data provided {exc} in request", exc_info=1)
        return jsonify(exception=exc.messages)
    except Exception as exc:
        logger.error(f"Error {exc} occured while parsing data from request", exc_info=1)
        return jsonify(exception=exc)

    y_pred = predict_crop_yield(field_data)
    result = {
        "predicted_yield": {
            "hectograms_per_hectare": y_pred,
            "kilograms_per_hectare": (y_pred * 0.1).round(2),
            "tonnes_per_hectare": (y_pred * 0.0001).round(2),
        },
    }
    return jsonify(result)


if __name__ == "__main__":
    # Only for local development
    app.run(debug=True, host="0.0.0.0", port=9696)

if __name__ != '__main__':
    # Only for production

    # Enable logging on the  gunicorn server
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_logger.handlers)
    app.logger.setLevel(gunicorn_logger.level)
