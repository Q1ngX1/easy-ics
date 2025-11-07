"""
API router definition

- upload
    - /api/upload/img: OCR image upload
    - /api/upload/text: Text parsing
    - /api/upload/patch: Future
- /api/download_ics: Download ICS file
- /api/check_health: Health check
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import Optional
import logging
from datetime import datetime

from app.services.ocr_service import get_ocr_service
from app.models.event import EventData, ICSDownloadRequest

logger = logging.getLogger(__name__)

router = APIRouter()


# ===== API =====

@router.post("api/upload/basetime")
async def set_timezone(timezone: dict):
    pass

@router.post("/api/upload/img")
async def upload_img(
    file: UploadFile = File(...),
    lang: Optional[str] = Query("chi_sim+eng", description="OCR Language")
):
    """
    Args:
        file: PNG, JPG, JPEG, BMP, TIFF
        lang: deafult: chi_sim+eng
        
    Returns:
        {
            "success": bool,
            "text": str,
            "filename": str,
            "length": int,
            "message": str
        }
        
    Example:
        ```bash
        curl -X POST "http://localhost:8000/api/upload_img" \\
             -F "file=@/path/to/image.png" \\
             -H "accept: application/json"
        ```
    """
    try:
        # file type check
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file.content_type}"
            )
        
        image_bytes = await file.read()
        
        if len(image_bytes) == 0:
            raise HTTPException(status_code=400, detail="empty file")
        
        from app.services.ocr_service import OCRService
        ocr_service = OCRService(lang=lang)
        
        if not ocr_service.is_tesseract_available():
            raise HTTPException(
                status_code=503,
                detail="Tesseract OCR is not installed or unavaliable"
            )

        text = ocr_service.extract_text_from_bytes(image_bytes)
        
        if not text or text.strip() == "":
            logger.warning(f"Unable to detect text: {file.filename}")
            return {
                "success": True,
                "text": "",
                "filename": file.filename,
                "length": 0,
                "message": "Unable to detect text"
            }
        
        logger.info(f"OCR success: {file.filename}, length: {len(text)}")
        
        return {
            "success": True,
            "text": text,
            "filename": file.filename,
            "length": len(text),
            "message": "OCR success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OCR failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"OCR failed: {str(e)}"
        )

@router.post("/api/upload/text")
async def upload_text(
    text: str = Query(..., description="text content"),
    timezone: Optional[str] = Query(None, description="User timezone (IANA format)"),
    lang: Optional[str] = Query("chi_sim+eng", description="OCR Language")
):
    """
    Args:
        text: plain text
        timezone: Optional user timezone (e.g., 'Asia/Shanghai')
        lang: default: chi_sim+eng
        
    Returns:
        {
            "success": bool,
            "events": List[dict],  
            "count": int,
            "timezone": str,
            "message": str
        }
    
    """
    try:
        if not text or text.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="Content cannot be empty"
            )
        
        from app.services.parser_service import ParserService
        
        parser = ParserService()
        event = parser.parse(text, timezone=timezone)
        
        logger.info(f"Parsing success, timezone: {timezone or 'default'}")
        
        return {
            "success": True,
            "events": [event.to_dict()],
            "count": 1,
            "timezone": timezone,
            "message": "Text parsing success"
        }
        
    except HTTPException:
        raise
    except NotImplementedError as e:
        logger.warning(f"Text parsing service undeveloped: {str(e)}")
        raise HTTPException(
            status_code=501,
            detail="Text parsing "
        )
    except Exception as e:
        logger.error(f"Text parsing failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Text parsing failed: {str(e)}"
        )
    

@router.post("/api/download_ics")
async def download_ics(request: ICSDownloadRequest):
    """
    Args:
        request
        
    Returns:
        ICS file stream
    
    """
    try:
        if not request.events or len(request.events) == 0:
            raise HTTPException(status_code=400, detail="Events list cannot be empty")
        from app.services.ics_service import ICSService
        from app.models.event import Event
        
        ics_service = ICSService()
        
        events = []
        for event_data in request.events:
            try:
                start_time = datetime.fromisoformat(event_data.start_time)
                end_time = datetime.fromisoformat(event_data.end_time)
                
                event = Event(
                    title=event_data.title,
                    start_time=start_time,
                    end_time=end_time,
                    location=event_data.location,
                    description=event_data.description
                )
                events.append(event)
            except ValueError as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Time format incorrect: {str(e)}"
                )
        
        ics_content = ics_service.generate_ics(events)
        
        logger.info(f"ICS file generated successfully: {len(events)} events")
        
        return StreamingResponse(
            iter([ics_content]),
            media_type="text/calendar; charset=utf-8",
            headers={
                "Content-Disposition": "attachment; filename=calendar.ics"
            }
        )
        
    except NotImplementedError:
        raise HTTPException(
            status_code=501,
            detail="ICS generation feature is under development"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ICS generation failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"ICS generation failed: {str(e)}"
        )


@router.get("/api/check_health")
async def check_health():
    """
    Returns:
        {
            "status": str,     
            "tesseract_available": bool,
            "message": str
        }
        
    Example:
        ```bash
        curl "http://localhost:8000/api/check_health"
        ```
    """
    try:
        ocr_service = get_ocr_service()
        is_available = ocr_service.is_tesseract_available()
        
        status = "healthy" if is_available else "unhealthy"
        message = "All service normal" if is_available else "Tesseract OCR is not installed"
        
        return {
            "status": status,
            "tesseract_available": is_available,
            "message": message
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=503,
            detail=f"Health check failed: {str(e)}"
        )


