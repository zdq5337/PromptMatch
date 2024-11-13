from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Depends

from model.request.file_request import FileUploadRequest
from model.response_model import ResponseModel
from model.vo.file_vo import FileUrlVO, FilePathVO
from services.file.file_service import FileService

router = APIRouter()


@router.post("/upload", response_model=ResponseModel, status_code=HTTPStatus.OK)
async def upload_file(service: Annotated[FileService, Depends(FileService)], file: UploadFile = File(...),
                      file_path: str = None):
    if not file_path:
        return ResponseModel.fail("文件路径不能为空")

    file_data = await file.read()
    file_name = file.filename
    file_url = service.upload_file(file_data, f"{file_path}/{file_name}")
    if not file_url:
        return ResponseModel.fail("上传文件失败")
    return ResponseModel.ok(FileUrlVO(file_url=file_url))


@router.get("/path", response_model=ResponseModel, status_code=HTTPStatus.OK)
async def get_file_path(service: Annotated[FileService, Depends(FileService)], fileName: str):
    file_path = service.get_file_url(fileName)
    if not file_path:
        return ResponseModel.fail("没有此文件")
    return ResponseModel.ok(FilePathVO(oss_path=file_path))
