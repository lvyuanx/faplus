from pydantic import BaseModel, Field
from pydantic_core import PydanticUndefined
from typing import Any, Type, get_args, get_origin


def generate_example(schema: Type[BaseModel]) -> Any:
    """
    根据 Pydantic Schema 自动生成示例数据。

    :param schema: 一个 Pydantic 的 BaseModel 子类
    :return: 生成的示例数据
    """
    example = {}

    # 遍历模型的字段
    for field_name, field_info in schema.model_fields.items():
        # 获取字段的类型和默认值
        field_type = field_info.annotation
        default = field_info.default

        # 如果字段有默认值，则使用默认值
        if default is not PydanticUndefined:
            example[field_name] = default
        else:
            # 根据字段类型生成示例值
            example[field_name] = generate_value_by_type(field_type)

    return example


def generate_value_by_type(field_type: Any) -> Any:
    """
    根据字段类型生成示例值（支持基础类型、嵌套模型、集合类型等）。

    :param field_type: 字段的类型
    :return: 示例值
    """
    origin = get_origin(field_type)
    args = get_args(field_type)

    # 基础类型的示例
    if field_type in [str, int, float, bool]:
        return {
            str: "string",
            int: 0,
            float: 0.0,
            bool: True,
        }[field_type]

    # 字典类型
    if origin is dict:
        key_type, value_type = args or (str, Any)
        return {generate_value_by_type(key_type): generate_value_by_type(value_type)}

    # 列表或集合类型
    if origin in [list, set, tuple]:
        value_type = args[0] if args else Any
        return [generate_value_by_type(value_type)]

    # 嵌套的 Pydantic 模型
    if isinstance(field_type, type) and issubclass(field_type, BaseModel):
        return generate_example(field_type)

    # 未知类型，返回 None
    return None
