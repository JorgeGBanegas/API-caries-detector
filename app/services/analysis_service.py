import base64
import io
import json
import os
import numpy as np
from PIL import Image
import boto3

from app.config.aws_settings import AwsSetting

aws_setting = AwsSetting()
aws_credentials = aws_setting.aws_credentials
aws_access_key_id = aws_credentials["aws_access_key_id"]
aws_secret_access_key = aws_credentials["aws_secret_access_key"]
aws_region = aws_setting.userpools["sa"]["region"]
endpoint_name = aws_setting.endpoint_sagemaker


def _load_image(image_file):
    image_stream = io.BytesIO(image_file)
    img = Image.open(image_stream)
    # img = img.resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img


def _predict(image):
    runtime_client = boto3.client('runtime.sagemaker', region_name=aws_region)
    payload = {
        'instances': image.tolist()
    }
    payload_json = json.dumps(payload)
    response = runtime_client.invoke_endpoint(EndpointName=endpoint_name,
                                              ContentType='application/json',
                                              Body=payload_json)

    result = json.loads(response['Body'].read().decode())
    return result


class AnalysisService:
    @staticmethod
    def analyze_image(image_file):
        image = _load_image(image_file)
        prediction = _predict(image)
        probability = prediction['predictions'][0][0]
        result = 1 - probability
        label = "Caries" if result > 0.5 else "Sin Caries"
        percentage_probability = result * 100
        # limit to 2 decimal places
        percentage_probability = round(percentage_probability, 2)
        return label, percentage_probability
