from typing import List

from fastapi import Depends, HTTPException
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from sqlmodel import Session

from model.entity.file import File
from model.entity.knowledge_file_relation import KnowledgeFileRelation
from model.request.knowledge_file_request import KnowledgeFileCreateRequest
from model.vo.file_vo import FileVO
from repository.file_repository import FileRepository
from repository.knowledge_file_relation_repository import KnowledgeFileRelationRepository
from repository.knowledge_repository import KnowledgeRepository
from services.components.langchain.v1.loaders.pdf_loaders import py_pdf_ium2_loader
from services.components.langchain.v1.text_splitters.generate_splitter import recursive_character_text_splitter
from services.components.langchain.v1.vectorstores.pgvector import generation_pgvector
from services.database.base import get_session
from setting import config
from utils.aliyun_oss import get_oss_file_url
from utils.download_file import download_file_from_oss
from utils.json_converter import JsonConverter
from utils.logger import logger

save_dir = config['file-path']


class KnowledgeFileService:
    def __init__(self, file_repo: FileRepository = Depends(FileRepository),
                 knowledge_repo: KnowledgeRepository = Depends(KnowledgeRepository),
                 knowledge_file_relation_repo: KnowledgeFileRelationRepository = Depends(
                     KnowledgeFileRelationRepository),
                 session: Session = Depends(get_session)):
        self.file_repo = file_repo
        self.knowledge_repo = knowledge_repo
        self.knowledge_file_relation_repo = knowledge_file_relation_repo
        self.session = session

    def batch_create_knowledge_file_relation(self, knowledge_file_relations: List[KnowledgeFileCreateRequest]) -> bool:
        logger.info(
            f'model-match services:knowledge:KnowledgeFileService:batch_create_knowledge_file_relation knowledge_file_relations: {JsonConverter.to_json(knowledge_file_relations)}')

        MAX_FILE_COUNT = 5
        try:
            with self.session.begin():
                # 遍历 knowledge_file_relations 根据oss地址进行下载到本地
                for knowledge_file_relation in knowledge_file_relations:
                    # 查询当前知识库中是否超过五个文件，
                    file_count = self.knowledge_file_relation_repo.get_knowledge_file_relation_count_by_knowledge_id(
                        knowledge_file_relation.knowledge_id, self.session)

                    knowledge = self.knowledge_repo.get_knowledge_by_id(knowledge_file_relation.knowledge_id,
                                                                        self.session)
                    if file_count >= MAX_FILE_COUNT:
                        raise HTTPException(status_code=500,
                                            detail="The knowledge {" + knowledge.name + "} file count is more than 5.")

                    self.__create_knowledge_file(knowledge_file_relation)

                # TODO 插入知识库 embedding 数据
                # 遍历 knowledge_file_relations 根据oss地址进行插入到知识库
                for knowledge_file_relation in knowledge_file_relations:
                    # See docker command above to launch a postgres instance with pgvector enabled.
                    vectorstore = generation_pgvector()

                    oss_file_url = get_oss_file_url(knowledge_file_relation.oss_path)
                    local_file = download_file_from_oss(oss_file_url, config['file-path'])
                    doc = py_pdf_ium2_loader(
                        local_file)
                    # TODO 循环doc对其中的metadata 添加一些区分字段
                    # https://python.langchain.com/v0.1/docs/integrations/vectorstores/pgvector/
                    splits = recursive_character_text_splitter(chunk_size=1000, chunk_overlap=200, documents=doc)

                    for split in splits:
                        split.metadata['file_id'] = knowledge_file_relation.file_id
                        split.metadata['knowledge_id'] = knowledge_file_relation.knowledge_id
                    vectorstore.add_documents(documents=splits)
            return True
        except Exception as e:
            logger.error(
                f'model-match services:knowledge:KnowledgeFileService:batch_create_knowledge_file_relation Error: {e}')
            raise HTTPException(status_code=500, detail="KnowledgeFileRelation error.")

    def __create_knowledge_file(self, knowledge_file_relation: KnowledgeFileCreateRequest):
        file = File(name=knowledge_file_relation.name,
                    oss_path=knowledge_file_relation.oss_path, size=knowledge_file_relation.size, )
        self.file_repo.create_file(file, self.session)
        self.session.flush()  # 刷新会话以获取自增的ID
        file_id = file.id  # 现在可以访问自增的ID
        knowledge_file_relation.file_id = file_id
        # 创建知识库文件关联
        relation = KnowledgeFileRelation(
            knowledge_id=knowledge_file_relation.knowledge_id,
            file_id=file_id,
        )
        self.knowledge_file_relation_repo.create_knowledge_file_relation(relation, self.session)

    def find_file_by_knowledge_id(self, knowledge_id: int) -> List[FileVO]:
        try:
            # 查询知识库文件关联
            knowledge_file_relations = self.knowledge_file_relation_repo.get_knowledge_file_relation_by_knowledge_id(
                knowledge_id, self.session)
            # 如果knowledge_file_relations为空或者集合长度为0，则返回file空集合
            if knowledge_file_relations is None or len(knowledge_file_relations) == 0:
                return []
            file_ids = [relation.file_id for relation in knowledge_file_relations]
            files = self.file_repo.get_files_by_ids(file_ids, self.session)
            # 转换为VO
            file_vos = [FileVO.model_validate(file) if hasattr(file, 'knowledge_id') else FileVO.model_validate(
                {**file.model_dump(), 'knowledge_id': None}) for file in files]
            # 为file_vos设置knowledge_id
            for file_vo in file_vos:
                file_vo.knowledge_id = knowledge_id
            # 替换oss_path
            for file_vo in file_vos:
                file_vo.oss_path = get_oss_file_url(file_vo.oss_path)
            logger.info(
                f'model-match services:knowledge:KnowledgeFileService:find_file_by_knowledge_id file_vos: {JsonConverter.to_json(file_vos)}')
            return file_vos
        except Exception as e:
            logger.error(
                f'model-match services:knowledge:KnowledgeFileService:find_file_by_knowledge_id Error: {e}')
            raise HTTPException(status_code=500, detail="Find file by knowledge id error.")
        finally:
            self.session.close()

    def remove_knowledge_file(self, file_id: int) -> bool:
        try:
            # 删除文件
            file = self.file_repo.get_file_by_id(file_id, self.session)
            logger.info(
                f'model-match services:knowledge:KnowledgeFileService:remove_knowledge_file file: {JsonConverter.to_json(file)}')
            if file:
                self.file_repo.delete_file(file, self.session)
                # 删除关联
                knowledge_file_relations = self.knowledge_file_relation_repo.get_knowledge_file_relation_by_file_id(
                    file_id, self.session)
                # 如果knowledge_file_relations不为空和长度不为0，则依次删除
                if knowledge_file_relations is not None and len(knowledge_file_relations) != 0:
                    for knowledge_file_relation in knowledge_file_relations:
                        self.knowledge_file_relation_repo.delete_knowledge_file_relation(knowledge_file_relation,
                                                                                         self.session)
            else:
                raise HTTPException(status_code=400, detail="File not found.")
            # 提交事务
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            logger.error(f'model-match services:knowledge:KnowledgeFileService:remove_knowledge_file Error: {e}')
            raise HTTPException(status_code=500, detail="Remove knowledge file error.")
        finally:
            self.session.close()
