from model.entity.file import File
from fastapi import HTTPException
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime



class FileRepository:

    def get_file_by_id(self, file_id: int, session: Session) -> Optional[File]:
        file = session.query(File).filter(File.id == file_id, File.deleted.is_(False)).first()
        if file:
            session.refresh(file)
        return file

    def get_files_by_ids(self, file_ids: List[int], session: Session) -> List[Optional[File]]:
        sql = select(File).where(File.id.in_(file_ids))
        return session.exec(sql).all()
        # files = (
        #     session.query(File)
        #     .filter((File.id.in_(file_ids), File.deleted.is_(False)))
        #     .all()
        # )
        #
        # for file in files:
        #     session.refresh(file)
        #
        # return files

    def get_all_files(self, session: Session) -> List[File]:
        files = session.query(File).filter(File.deleted.is_(False)).all()
        for file in files:
            session.refresh(file)
        return files

    def create_file(self, file: File, session: Session) -> File:
        session.add(file)
        return file

    def update_file(self, file_id: int, new_file: File, session: Session) -> File:
        old_file = self.get_file_by_id(file_id, session)
        if old_file:
            for key, value in new_file.model_dump().items():
                setattr(old_file, key, value)
            session.commit()
            return old_file
        else:
            raise HTTPException(status_code=404, detail="File not found")

    def delete_file(self, file: File, session: Session) -> File:
        file.deleted = True  # 逻辑删除
        file.update_time = datetime.now()  # 更新时间
        return file

    def batch_create_files(self, files: List[File], session: Session) -> List[File]:
       session.bulk_save_objects(files)
       session.commit()
       return files

    def batch_delete_files(self, file_ids: List[int], session: Session) -> List[File]:
        files_to_delete = [self.get_file_by_id(file_id, session) for file_id in file_ids]
        non_existing_or_deleted_ids = [file_id for file_id in file_ids if not self.get_file_by_id(file_id)]

        if non_existing_or_deleted_ids:
            raise HTTPException(status_code=404,
                                detail=f"Files with IDs {non_existing_or_deleted_ids} not found or already deleted.")

        for file in files_to_delete:
            file.deleted = True  # 逻辑删除
            file.update_time = datetime.now()  # 更新时间

        session.commit()
        return files_to_delete
