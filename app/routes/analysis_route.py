from fastapi import APIRouter, status, Depends, UploadFile
from fastapi_cognito import CognitoAuth, CognitoSettings
from app.controllers.analysis_controller import AnalysisController
from app.config.aws_settings import AwsSetting

aws_settings = AwsSetting()
cognito_sa = CognitoAuth(settings=CognitoSettings.from_global_settings(aws_settings), userpool_name="sa")

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"]
)


# routes for analysis of radiography
@router.post("/", response_model=None, status_code=status.HTTP_200_OK)
def get_analysis(image_file: UploadFile, analysis_controller: AnalysisController = Depends()):
    image = image_file.file.read()
    return analysis_controller.get_analysis(image)

