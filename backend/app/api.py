"""
API router definition

- upload
    - /api/upload/img: OCR single image upload
    - /api/upload/imgs: OCR multiple images upload (batch)
    - /api/upload/text: Text parsing
    - /api/upload/patch: Future
- /api/download_ics: Download ICS file
- /api/check_health: Health check
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import Optional, List
import logging
from datetime import datetime

from app.services.ocr_service import get_ocr_service
from app.models.event import EventData, ICSDownloadRequest

logger = logging.getLogger(__name__)

router = APIRouter()


# ===== API =====


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


@router.post("/api/upload/imgs")
async def upload_imgs(
    files: List[UploadFile] = File(...),
    lang: Optional[str] = Query("chi_sim+eng", description="OCR Language")
):
    """
    Batch upload multiple images and extract text via OCR
    
    Args:
        files: Multiple image files (PNG, JPG, JPEG, BMP, TIFF)
        lang: OCR language (default: chi_sim+eng)
        
    Returns:
        {
            "success": bool,
            "results": [
                {
                    "filename": str,
                    "success": bool,
                    "text": str,
                    "length": int,
                    "message": str
                }
            ],
            "total": int,
            "successful": int,
            "failed": int,
            "combined_text": str,
            "combined_length": int
        }
        
    Example:
        ```bash
        curl -X POST "http://localhost:8000/api/upload/imgs" \\
             -F "files=@image1.png" \\
             -F "files=@image2.png" \\
             -H "accept: application/json"
        ```
    """
    try:
        if not files or len(files) == 0:
            raise HTTPException(status_code=400, detail="No files provided")
        
        from app.services.ocr_service import OCRService
        
        ocr_service = OCRService(lang=lang)
        
        if not ocr_service.is_tesseract_available():
            raise HTTPException(
                status_code=503,
                detail="Tesseract OCR is not installed or unavailable"
            )
        
        results = []
        combined_text_parts = []
        successful_count = 0
        
        for file in files:
            # File type check
            if not file.content_type or not file.content_type.startswith("image/"):
                results.append({
                    "filename": file.filename,
                    "success": False,
                    "text": "",
                    "length": 0,
                    "message": f"Unsupported file type: {file.content_type}"
                })
                continue
            
            try:
                image_bytes = await file.read()
                
                if len(image_bytes) == 0:
                    results.append({
                        "filename": file.filename,
                        "success": False,
                        "text": "",
                        "length": 0,
                        "message": "Empty file"
                    })
                    continue
                
                text = ocr_service.extract_text_from_bytes(image_bytes)
                
                if not text or text.strip() == "":
                    results.append({
                        "filename": file.filename,
                        "success": True,
                        "text": "",
                        "length": 0,
                        "message": "Unable to detect text"
                    })
                    logger.warning(f"Unable to detect text: {file.filename}")
                else:
                    results.append({
                        "filename": file.filename,
                        "success": True,
                        "text": text,
                        "length": len(text),
                        "message": "OCR success"
                    })
                    combined_text_parts.append(text)
                    successful_count += 1
                    logger.info(f"OCR success: {file.filename}, length: {len(text)}")
                    
            except Exception as e:
                results.append({
                    "filename": file.filename,
                    "success": False,
                    "text": "",
                    "length": 0,
                    "message": f"OCR failed: {str(e)}"
                })
                logger.error(f"OCR failed for {file.filename}: {str(e)}")
        
        combined_text = '\n'.join(combined_text_parts)
        combined_length = len(combined_text)
        failed_count = len(files) - successful_count
        
        logger.info(f"Batch OCR complete: {len(files)} total, {successful_count} successful, {failed_count} failed")
        
        return {
            "success": True,
            "results": results,
            "total": len(files),
            "successful": successful_count,
            "failed": failed_count,
            "combined_text": combined_text,
            "combined_length": combined_length
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch OCR failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Batch OCR failed: {str(e)}"
        )


@router.post("/api/upload/text")
async def upload_text(
    text: str = Query(..., description="text content"),
    timezone: Optional[str] = Query(None, description="User timezone (IANA format)"),
    #lang: Optional[str] = Query("chi_sim+eng", description="OCR Language")
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


