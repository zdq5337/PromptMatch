from sqlmodel import Session, create_engine

from setting import config


# Dependency to get the database session
def get_session():
    # 使用 SQLModel.create_engine 创建引擎
    # SQLModel.create_engine()
    engine = create_engine(config['database']['url'])
    with Session(engine) as session:
        yield session
