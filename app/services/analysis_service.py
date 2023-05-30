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
    image = Image.open(image_stream)
    image_array = np.array(image)
    image_array = np.expand_dims(image_array, axis=0)
    return image_array


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
        print(prediction)
        probability = prediction['predictions'][0][0]
        label = "Caries" if probability > 0.5 else "No Caries"
        percentage_probability = probability * 100
        # limit to 2 decimal places
        percentage_probability = round(percentage_probability, 2)
        return label, percentage_probability
