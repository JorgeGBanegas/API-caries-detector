import io
import os
import keras as keras
import numpy as np
from PIL import Image
import boto3


from app.config.aws_settings import AwsSetting

aws_setting = AwsSetting()
aws_credentials = aws_setting.aws_credentials
aws_access_key_id = aws_credentials["aws_access_key_id"]
aws_secret_access_key = aws_credentials["aws_secret_access_key"]
aws_region = aws_setting.userpools["sa"]["region"]


def _load_image(image_file):
    image_stream = io.BytesIO(image_file)
    image = Image.open(image_stream)
    image_array = np.array(image)
    return image_array


def _load_model():
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    model_path = os.path.join(parent_dir, 'model_ai', 'best_model.h5')
    model_directory = os.path.dirname(model_path)
    if os.path.exists(model_path):
        model = keras.models.load_model(model_path)
        return model

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )
    bucket_name = 'intellident-model'
    object_name = 'best_model.h5'
    file_name = os.path.join(model_directory, 'best_model.h5')
    s3.download_file(bucket_name, object_name, file_name)

    os.rename(file_name, model_path)

    model = keras.models.load_model(model_path)

    return model


class AnalysisService:
    @staticmethod
    def analyze_image(image_file):
        model = _load_model()
        image = _load_image(image_file)
        prediction = model.predict(np.expand_dims(image, axis=0), verbose=0)[0]
        probability = prediction[0]
        label = "Caries" if probability > 0.5 else "No Caries"
        percentage_probability = probability * 100
        return label, percentage_probability
