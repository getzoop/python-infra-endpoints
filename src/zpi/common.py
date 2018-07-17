import json
from abc import ABC
from enum import Enum

import stringcase


class BaseSerialiazable(ABC):
    excludedFieldsFromJson = []

    def _exclude_attribute_from_json(self, attr_name):
        """exclude fields from final json"""
        self.excludedFieldsFromJson.append("_" + attr_name)

    def to_json(self):
        """Serialize class to JSON"""
        return json.dumps(self.__serialize())

    def __serialize(self):
        """Transforms all classes properties into a dict"""
        class_dict = vars(self)

        new_dict = dict()
        for key, item in class_dict.items():

            if key in self.excludedFieldsFromJson:
                continue

            new_key = stringcase.camelcase(key.strip("_"))

            if type(item) == list:
                new_dict[new_key] = [dep.__serialize() for dep in item]
            elif isinstance(item, Enum) is True:
                new_dict[new_key] = item.name
            else:
                new_dict[new_key] = item

        return new_dict
