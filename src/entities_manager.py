from typing import Any, Iterator, Dict
from collections import OrderedDict


class EntitiesManager:
    def __init__(self):
        self._class_to_entities = OrderedDict()      # 1. Dict[str, List[Entity]]
        self._group_to_entities = OrderedDict()                 # 2. Dict[Any, List[Entity]]

    def add_entity(self, entity):
        for class_name in entity:
            if class_name not in self._class_to_entity:
                self._class_to_entity[class_name] = list()
            self._class_to_entity[class_name].append(entity)

    def remove_entity(self, entity):
        for class_name in entity:
            self._class_to_entity[class_name].remove(entity)

    def add_group(self, group_name):
        if group_name in self._group_to_entities:
            print(f"EntitiesManager - Name of the group already in use: {group_name}")
        self._group_to_entities[group_name] = list()

    def add_entity_to_group(self, group_name, entity):
        self._group_to_entities[group_name].append(entity)

    def remove_entity_from_group(self, group_name, entity):
        self._group_to_entities[group_name].remove(entity)

    def discharge_entity_from_all_groups(self, entity: Entity) -> None:
        for group_name in self._group_to_entities:
            if entity in self._group_to_entities[group_name]:
                self._group_to_entities[group_name].remove(entity)

    def delete_group(self, group_name):
        del self._group_to_entities[group_name]

    def delete_group_and_its_entities(self, group_name: Any) -> None:
        for entity in self._group_to_entities[group_name]:
            for class_name in entity:
                self._class_to_entity[class_name].remove(entity)
        del self._group_to_entities[group_name]

    def unregister_and_discharge_entity_from_all_groups(self, entity: Entity) -> None:
        self.discharge_entity_from_all_groups(entity)
        self.unregister_entity(entity)

    def register_and_enlist_entity(self, entity: Entity, *groups_names) -> None:
        self.register_entity(entity)
        for group_name in groups_names:
            if group_name not in self._group_to_entities:
                self._group_to_entities[group_name] = list()
            self._group_to_entities[group_name].append(entity)

    def get_entity_groups(self, entity: Entity) -> set:
        groups = set()
        for group_name in self._group_to_entities:
            if entity in self._group_to_entities[group_name]:
                groups.add(group_name)
        return groups

    def get_all_entities_of_group(self, group_name: Any) -> Iterator[Entity]:
        def group_entities_generator() -> Iterator[Entity]:
            for entity in self._group_to_entities[group_name]:
                yield entity
        return group_entities_generator()

    def get_all_entities_with_component_class(self, class_name: str) -> Iterator[Entity]:
        def compo_entities_generator() -> Iterator[Entity]:
            for entity in self._class_to_entity[class_name]:
                yield entity
        return compo_entities_generator()

    def get_all_instances_of_component_class(self, class_name: str) -> Iterator[Any]:
        def compo_instances_generator() -> Iterator[Any]:
            for entity in self._class_to_entity[class_name]:
                yield entity[class_name]
        return compo_instances_generator()

