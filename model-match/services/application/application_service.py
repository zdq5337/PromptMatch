from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlmodel import Session

from constants.large_model_enum import LargeModelName
from model.entity.application import Application
from model.entity.application_knowledge_relation import ApplicationKnowledgeRelation
from model.request.application_request import ApplicationCreateRequest, ApplicationEditRequest
from model.vo.application_vo import ApplicationVO
from repository.application_knowledge_relation_repository import ApplicationKnowledgeRelationRepository
from repository.application_repository import ApplicationRepository
from repository.knowledge_repository import KnowledgeRepository
from services.database.base import get_session
from utils.json_converter import JsonConverter
from utils.logger import logger


class ApplicationService:
    def __init__(self, application_repo: ApplicationRepository = Depends(ApplicationRepository),
                 application_knowledge_relation_repo: ApplicationKnowledgeRelationRepository = Depends(
                     ApplicationKnowledgeRelationRepository),
                 knowledge_repo: KnowledgeRepository = Depends(KnowledgeRepository),
                 session: Session = Depends(get_session)):
        self.application_repo = application_repo
        self.application_knowledge_relation_repo = application_knowledge_relation_repo
        self.knowledge_repo = knowledge_repo
        self.session = session

    def get_all_applications(self) -> List[ApplicationVO]:
        applications = self.application_repo.get_all_applications(self.session)
        logger.info(
            f"model-match services:application:ApplicationService:get_all_applications applications: {JsonConverter.to_json(applications)}")
        application_vos = [ApplicationVO.from_orm(application) for application in applications]

        for application_vo in application_vos:
            for model in LargeModelName:
                # 检查每个模型的 vendor_name 是否与 application 中的 model_name 匹配
                if model.vendor_name == application_vo.model_name:
                    # 如果找到匹配项，标识为true
                    application_vo.model_name_valid = True
                    break
        logger.info(
            f"model-match services:application:ApplicationService:get_all_applications application_vos: {JsonConverter.to_json(application_vos)}")
        return application_vos

    def get_application_by_id(self, application_id: int) -> Optional[ApplicationVO]:
        application = self.application_repo.get_application_by_id(application_id, self.session)
        logger.info(
            f"model-match services:application:ApplicationService:get_application_by_id application: {JsonConverter.to_json(application)}")
        if application:
            application_vo = ApplicationVO.from_orm(application)

            for model in LargeModelName:
                # 检查每个模型的 vendor_name 是否与 application 中的 model_name 匹配
                if model.vendor_name == application.model_name:
                    # 如果找到匹配项，标识为true
                    application_vo.model_name_valid = True
                    break

            # 添加知识库信息
            knowledge_relations = self.application_knowledge_relation_repo.get_application_knowledge_relation_by_application_id(
                application_id, self.session)
            knowledge_vos = []
            for knowledge_relation in knowledge_relations:
                knowledge = self.knowledge_repo.get_knowledge_by_id(knowledge_relation.knowledge_id, self.session)
                knowledge_vos.append(knowledge)
            application_vo.knowledge_vos = knowledge_vos
            logger.info(
                f"model-match services:application:ApplicationService:get_application_by_id application_vo: {JsonConverter.to_json(application_vo)}")
            return application_vo
        else:
            return None

    def create_application(self, application_create_request: ApplicationCreateRequest) -> bool:
        # 将验证后的数据转换为Application模型
        application = Application(**application_create_request.dict())
        try:
            with (self.session.begin()):
                self.application_repo.create_application(application, self.session)
                self.session.flush()  # 刷新会话以获取自增的ID
                application_id = application.id  # 现在可以访问自增的ID

                modelNameValid = False
                for model in LargeModelName:
                    # 检查每个模型的 vendor_name 是否与 application 中的 model_name 匹配
                    if model.vendor_name == application.model_name:
                        # 如果找到匹配项，标识为true
                        modelNameValid = True
                        break
                if not modelNameValid:
                    raise HTTPException(status_code=400, detail="Model name is not found, Please check the model name.")

                if application_create_request.knowledge_ids is not None and len(
                        application_create_request.knowledge_ids) > 0:
                    # 创建应用知识库关联
                    for knowledge_id in application_create_request.knowledge_ids:
                        application_knowledge_relation = ApplicationKnowledgeRelation(application_id=application_id,
                                                                                      knowledge_id=knowledge_id)
                        self.application_knowledge_relation_repo.create_application_knowledge_relation(
                            relation=application_knowledge_relation,
                            session=self.session
                        )
                return True
        except Exception as e:
            logger.error(
                f'model-match services:application:ApplicationService:create_application Error: {e}')
            raise HTTPException(status_code=500, detail="Create application error.")

    def update_application(self, application_edit_request: ApplicationEditRequest) -> bool:
        application_id = application_edit_request.id
        application = self.application_repo.get_application_by_id(application_id, self.session)
        if application:
            try:
                with (self.session.begin()):
                    # 判断application_edit_request.model_name的值是否为空
                    if application_edit_request.model_name is not None and len(application_edit_request.model_name) > 0:
                        # 判断所关联模型是否可用
                        for model_name in application_edit_request.model_name:
                            # TODO 去缓存中对比是否存在该模型
                            print(model_name)

                    # 修改应用信息
                    new_application = Application(**application_edit_request.dict())
                    self.application_repo.update_application(application, new_application, self.session)

                    # 删除应用知识库关联
                    self.application_knowledge_relation_repo.delete_by_application_id(
                        application_id, self.session)

                    if application_edit_request.knowledge_ids is not None and len(
                            application_edit_request.knowledge_ids) > 0:
                        # 创建应用知识库关联
                        for knowledge_id in application_edit_request.knowledge_ids:
                            application_knowledge_relation = ApplicationKnowledgeRelation(application_id=application_id,
                                                                                          knowledge_id=knowledge_id)
                            self.application_knowledge_relation_repo.create_application_knowledge_relation(
                                relation=application_knowledge_relation,
                                session=self.session
                            )
                    return True
            except Exception as e:
                logger.error(
                    f'model-match services:application:ApplicationService:update_application Error: {e}')
                raise HTTPException(status_code=500, detail="Update application error.")
        else:
            raise HTTPException(status_code=404, detail="Application not found, Please check the application id.")
