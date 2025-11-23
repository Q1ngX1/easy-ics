"""
API router definition

Endpoints:
- Health Check:
    - GET  /api/check_health: Service health status and OCR availability

- Image Processing (OCR):
    - POST /api/upload: Unified OCR image upload (single or multiple images)

- Text Processing:
    - POST /api/upload/text: Parse text and extract calendar events

- ICS Generation:
    - POST /api/download_ics: Generate and download ICS calendar file

Authentication: None (public API)
Rate Limiting: None (consider adding for production)
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


# ===== Helper Functions =====

async def _process_ocr_files(files_list: List[UploadFile], lang: str):
    """
    Shared OCR processing logic for single and multiple files
    
    Args:
        files_list: List of UploadFile objects
        lang: OCR language
        
    Returns:
        Dictionary containing processing results
    """
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
    
    for file in files_list:
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
    failed_count = len(files_list) - successful_count
    
    return {
        "results": results,
        "total": len(files_list),
        "successful": successful_count,
        "failed": failed_count,
        "combined_text": combined_text,
        "combined_length": combined_length
    }


# ===== API =====


@router.post("/api/upload")
async def upload(
    file: Optional[UploadFile] = File(None),
    files: Optional[List[UploadFile]] = File(None),
    lang: Optional[str] = Query("chi_sim+eng", description="OCR Language")
):
    """
    Unified image upload endpoint handling both single and multiple files.
    
    Args:
        file: Single image file (PNG, JPG, JPEG, BMP, TIFF)
        files: Multiple image files
        lang: OCR language (default: chi_sim+eng)
        
    Returns:
        Single file: 
        {
            "success": bool,
            "text": str,
            "filename": str,
            "length": int,
            "message": str
        }
        
        Multiple files:
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
    """
    try:
        # Validate input: exactly one of file or files must be provided
        if file and files:
            raise HTTPException(
                status_code=400,
                detail="Provide either 'file' (single) or 'files' (multiple), not both"
            )
        
        if not file and not files:
            raise HTTPException(
                status_code=400,
                detail="No files provided. Provide either 'file' (single) or 'files' (multiple)"
            )
        
        # Process based on input type
        if file:
            # Single file upload
            logger.info(f"Processing single file: {file.filename}")
            result = await _process_ocr_files([file], lang)
            
            # Return simplified format for single file
            single_result = result["results"][0]
            return {
                "success": True,
                "text": single_result["text"],
                "filename": single_result["filename"],
                "length": single_result["length"],
                "message": single_result["message"]
            }
        
        else:
            # Multiple files upload
            if not files or len(files) == 0:
                raise HTTPException(status_code=400, detail="No files provided")
            
            logger.info(f"Processing {len(files)} files")
            result = await _process_ocr_files(files, lang)
            
            # Return detailed format for multiple files
            logger.info(f"Batch OCR complete: {result['total']} total, {result['successful']} successful, {result['failed']} failed")
            
            return {
                "success": True,
                "results": result["results"],
                "total": result["total"],
                "successful": result["successful"],
                "failed": result["failed"],
                "combined_text": result["combined_text"],
                "combined_length": result["combined_length"]
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )


@router.post("/api/upload/text")
async def upload_text(
    text: str = Query(..., description="text content"),
    timezone: Optional[str] = Query(None, description="User timezone (IANA format)"),
):
    """
    Parse text content and extract calendar events.
    
    Workflow:
    1. Validate input text
    2. Clean and normalize text
    3. Extract date/time information
    4. Extract title, location, description
    5. Determine priority and other event details
    6. Return parsed Event objects
    
    Args:
        text: plain text content containing event information
        timezone: Optional user timezone (e.g., 'Asia/Shanghai')
        
    Returns:
        {
            "success": bool,
            "events": List[dict],  # List of parsed events
            "count": int,          # Number of events extracted
            "timezone": str,       # User timezone
            "message": str
        }
    
    Example:
        ```bash
        curl -X POST "http://localhost:8000/api/upload/text" \\
          -H "Content-Type: application/json" \\
          -d '{"text": "Meeting on 2025-11-22 at 14:30 in Conference Room A", "timezone": "Asia/Shanghai"}'
        ```
    """
    try:
        # Step 1: Validate input
        if not text or text.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="Content cannot be empty"
            )
        
        logger.info(f"Starting text parsing workflow - Input length: {len(text)}")
        
        # Step 2: Initialize parser service
        from app.services.parser_service import get_parser_service
        parser_service = get_parser_service()
        
        # Step 3: Parse text and extract events
        events = parser_service.parse(text, timezone=timezone)
        
        if not events:
            logger.warning("No events extracted from text")
            return {
                "success": False,
                "events": [],
                "count": 0,
                "timezone": timezone or "default",
                "message": "No events could be extracted from the provided text"
            }
        
        # Step 4: Convert Event objects to dictionaries for JSON response
        events_dict = [event.to_dict() for event in events]
        
        logger.info(f"Text parsing success - Extracted {len(events)} event(s), timezone: {timezone or 'default'}")
        
        return {
            "success": True,
            "events": events_dict,
            "count": len(events),
            "timezone": timezone or "default",
            "message": f"Successfully extracted {len(events)} event(s) from text"
        }
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error in text parsing: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(e)}"
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
    Generate and download ICS calendar file from event data.
    
    Workflow:
    1. Validate event data
    2. Parse datetime strings (ISO 8601 format)
    3. Create Event objects
    4. Generate ICS content
    5. Stream ICS file to client
    
    Request:
    {
        "events": [
            {
                "title": "Event Title" (required),
                "start_time": "2025-11-22T14:00:00" (required, ISO 8601),
                "end_time": "2025-11-22T15:00:00" (required, ISO 8601),
                "location": "Event Location" (optional),
                "description": "Event Description" (optional)
            }
        ]
    }
    
    Returns:
        ICS file (text/calendar) as stream for download
        Filename: calendar.ics
    
    Error Responses:
        400: Events list is empty or invalid format
        422: Datetime format is incorrect (not ISO 8601)
        500: ICS generation failed
    
    Example:
        curl -X POST http://localhost:8000/api/download_ics \\
          -H "Content-Type: application/json" \\
          -d '{
            "events": [{
              "title": "Team Meeting",
              "start_time": "2025-11-22T14:00:00",
              "end_time": "2025-11-22T15:00:00",
              "location": "Conference Room A"
            }]
          }'
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


