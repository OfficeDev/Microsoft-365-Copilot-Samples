from azure.data.tables import TableClient, TableEntity
from datetime import datetime
import json
from config import Settings

class DbEntity:
    def __init__(self, etag, partition_key, row_key, timestamp):
        self.etag = etag
        self.partition_key = partition_key
        self.row_key = row_key
        self.timestamp = timestamp


class DbService:
    def __init__(self, ok_to_cache_locally: bool):
        if not Settings.STORAGE_ACCOUNT_CONNECTION_STRING:
            raise ValueError("STORAGE_ACCOUNT_CONNECTION_STRING is not set")
        self.ok_to_cache_locally = ok_to_cache_locally
        self.entity_cache = []

    async def get_entity_by_row_key(self, table_name: str, row_key: str):
        if not self.ok_to_cache_locally:
            table_client = TableClient.from_connection_string(
                Settings.STORAGE_ACCOUNT_CONNECTION_STRING, table_name
            )
            result = await table_client.get_entity(
                partition_key=table_name, row_key=row_key
            )
            return self.expand_property_values(result)
        else:
            entities = await self.get_entities(table_name)
            filtered_entities = [e for e in entities if e["rowKey"] == row_key]
            if not filtered_entities:
                print("Entity not found")
                return None
            return filtered_entities[0]


    async def get_entities(self, table_name: str):
        try:
            if self.ok_to_cache_locally and self.entity_cache:
                return self.entity_cache
            else:
                table_client = TableClient.from_connection_string(
                Settings.STORAGE_ACCOUNT_CONNECTION_STRING, table_name
            )
            entities = table_client.list_entities()
            self.entity_cache = [
                self.expand_property_values(entity) for entity in entities
            ]
            return self.entity_cache
        except Exception as e:
            print(f"Error fetching entities from table '{table_name}': {e}")


    async def create_entity(self, table_name: str, row_key: str, new_entity):
        entity = self.compress_property_values(new_entity)
        table_client = TableClient.from_connection_string(
        Settings.STORAGE_ACCOUNT_CONNECTION_STRING, table_name
    )
        table_client.create_entity(
        entity={"PartitionKey": table_name, "RowKey": row_key, **entity}
    )

    async def update_entity(self, table_name: str, updated_entity):
        entity = self.compress_property_values(updated_entity)
        table_client = TableClient.from_connection_string(
            Settings.STORAGE_ACCOUNT_CONNECTION_STRING, table_name
        )
        await table_client.update_entity(entity=entity, mode="Replace")

    async def get_next_id(self, table_name: str) -> int:
        try:
            entities = await self.get_entities(table_name)
            return len(entities) + 1
        except Exception as e:
            print("Error fetching entities:", e)
            return -1

    def expand_property_values(self, entity):
        expanded_entity = {}
        for key, value in entity.items():
            expanded_entity[key] = self.expand_property_value(value)
        return expanded_entity

    def expand_property_value(self, value):
        if isinstance(value, str) and (value.startswith("{") or value.startswith("[")):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return value

    def compress_property_values(self, entity):
        compressed_entity = {}
        for key, value in entity.items():
            compressed_entity[key] = self.compress_property_value(value)
        return compressed_entity

    def compress_property_value(self, value):
        if isinstance(value, (dict, list)):
            return json.dumps(value)
        return value
