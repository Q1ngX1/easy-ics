"""
API 路由定义
提供图片上传、OCR 识别、文本解析和 ICS 文件生成的接口
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional
import logging
from io import BytesIO

from app.services.ocr_service import get_ocr_service

logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter()


@router.post("/api/ocr/upload")
async def upload_image_for_ocr(
    file: UploadFile = File(..., description="上传的图片文件"),
    lang: Optional[str] = Form(None, description="OCR 识别语言，如 'chi_sim+eng'")
):
    """
    上传图片并进行 OCR 识别
    
    Args:
        file: 上传的图片文件 (支持 PNG, JPG, JPEG, BMP, TIFF 等格式)
        lang: 可选的识别语言设置
        
    Returns:
        JSON 响应，包含识别的文本内容
        
    Example:
        ```bash
        curl -X POST "http://localhost:8000/api/ocr/upload" \\
             -F "file=@/path/to/image.png" \\
             -F "lang=chi_sim+eng"
        ```
    """
    try:
        # 验证文件类型
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件类型: {file.content_type}，请上传图片文件"
            )
        
        # 读取图片数据
        image_bytes = await file.read()
        
        if len(image_bytes) == 0:
            raise HTTPException(status_code=400, detail="上传的文件为空")
        
        # 获取 OCR 服务
        ocr_service = get_ocr_service()
        
        # 如果指定了语言，创建新的服务实例
        if lang:
            from app.services.ocr_service import OCRService
            ocr_service = OCRService(lang=lang)
        
        # 执行 OCR 识别
        text = ocr_service.extract_text_from_bytes(image_bytes)
        
        if not text:
            logger.warning(f"Unable to identify text from the image: {file.filename}")
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "text": "",
                    "message": "Unable to identify text from the image",
                    "filename": file.filename
                }
            )
        
        logger.info(f"Success identify: {file.filename}, text length: {len(text)}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "text": text,
                "filename": file.filename,
                "length": len(text)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OCR service fail: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"OCR service fail: {str(e)}"
        )


@router.post("/api/text/parse")
async def parse_text_to_events(text: str = Form(..., description="待解析的文本内容")):
    """
    解析文本内容，提取日历事件信息
    
    Args:
        text: 待解析的文本（可以是 OCR 识别结果或用户直接输入）
        
    Returns:
        解析后的事件列表
        
    Note:
        此功能需要实现 parser_service.py
    """
    # TODO: 实现文本解析逻辑
    raise HTTPException(
        status_code=501,
        detail="文本解析功能正在开发中，请等待 parser_service 实现"
    )


@router.post("/api/ics/generate")
async def generate_ics_file():
    """
    根据事件数据生成 ICS 日历文件
    
    Returns:
        ICS 文件（可下载）
        
    Note:
        此功能需要实现 ics_service.py
    """
    # TODO: 实现 ICS 生成逻辑
    raise HTTPException(
        status_code=501,
        detail="ICS 生成功能正在开发中，请等待 ics_service 实现"
    )


@router.post("/api/process")
async def process_image_to_ics(
    file: UploadFile = File(..., description="上传的图片文件")
):
    """
    一站式服务：上传图片 -> OCR 识别 -> 文本解析 -> 生成 ICS 文件
    
    Args:
        file: 上传的图片文件
        
    Returns:
        ICS 日历文件（可下载）
        
    Note:
        此功能需要完整实现所有服务模块
    """
    # TODO: 实现完整的处理流程
    raise HTTPException(
        status_code=501,
        detail="完整流程功能正在开发中"
    )


@router.get("/api/ocr/health")
async def check_ocr_health():
    """
    检查 OCR 服务健康状态
    
    Returns:
        OCR 服务状态信息
    """
    try:
        ocr_service = get_ocr_service()
        is_available = ocr_service.is_tesseract_available()
        
        if is_available:
            languages = ocr_service.get_available_languages()
            return {
                "status": "healthy",
                "tesseract_available": True,
                "supported_languages": languages,
                "default_language": ocr_service.lang
            }
        else:
            return JSONResponse(
                status_code=503,
                content={
                    "status": "unhealthy",
                    "tesseract_available": False,
                    "message": "Tesseract OCR 不可用，请检查安装"
                }
            )
    except Exception as e:
        logger.error(f"健康检查失败: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "error",
                "message": str(e)
            }
        )
