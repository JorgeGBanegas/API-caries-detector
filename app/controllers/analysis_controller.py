from fastapi import HTTPException, Depends
from starlette import status

from app.dependencies.dependencies import get_analysis_service
from app.services.analysis_service import AnalysisService


class AnalysisController:
    def __init__(self, analysis_service: AnalysisService = Depends(get_analysis_service)):
        self.analysis_service = analysis_service

    def get_analysis(self, image):
        try:
            diagnosis, probability = self.analysis_service.analyze_image(image)
            result = {
                "diagnosis": diagnosis,
                "probability": probability
            }
            return result
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                "message": "Error al realizar el analisis, por favor cargue una radiografia en buena calidad e "
                           "intentelo de nuevo",
                "error": str(e)
            })
