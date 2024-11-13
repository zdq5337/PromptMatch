import json
from datetime import datetime
from typing import Any, Union, Optional
from sqlmodel import Session
from model.entity.application import Application  # 假设您的Application类在这个包中


class JsonConverter:
    @staticmethod
    def to_json(data: Any, session: Optional[Session] = None) -> str:
        """
        将给定的数据转换为JSON格式的字符串。

        :param data: 要转换的数据，可以是字典、列表、datetime对象、Application对象等
        :param session: SQLModel会话，用于处理SQLModel对象
        :return: JSON格式的字符串
        """
        if data is None:
            return json.dumps(None)

        if isinstance(data, list):
            # 如果传入的是列表，确保每个元素都可以被序列化
            serializable_data = [item for item in data if
                                 isinstance(item, (dict, list, tuple, str, int, float, bool, type(None))) or
                                 (hasattr(item, 'dict') and callable(item.dict))]
            # 将列表中的SQLModel对象转换为字典
            serializable_data = [item.dict() if callable(item.dict) else item for item in serializable_data]
        elif isinstance(data, dict):
            # 如果传入的是字典，确保所有的值都可以被序列化
            serializable_data = {k: v for k, v in data.items() if
                                 isinstance(v, (dict, list, tuple, str, int, float, bool, type(None))) or
                                 (hasattr(v, 'dict') and callable(v.dict))}
            # 将字典中的SQLModel对象转换为字典
            serializable_data = {k: v.dict() if callable(v.dict) else v for k, v in serializable_data.items()}
        else:
            # 如果传入的是单个对象，确保它可以直接被序列化或者有一个dict方法可以调用
            serializable_data = data.dict() if callable(data.dict) else data

        # 使用json.dumps来序列化数据，包括datetime对象和bytes对象
        return json.dumps(serializable_data, default=JsonConverter._datetime_serializer)

    @staticmethod
    def _datetime_serializer(o: Any) -> Union[str, int, float, list, dict, None]:
        """
        JSON序列化器的辅助方法，用于处理datetime对象和bytes对象。

        :param o: 要序列化的对象
        :return: 序列化后的字符串或列表或字典
        """
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, bytes):
            return o.decode('utf-8')
        raise TypeError(f"类型 {type(o)} 无法序列化为JSON")


# 示例使用
if __name__ == "__main__":
    # 创建一个Application对象
    app = Application(name="Example Application")

    # 使用工具类将Application对象转换为JSON格式的字符串
    json_str = JsonConverter.to_json(app)
    print(json_str)
