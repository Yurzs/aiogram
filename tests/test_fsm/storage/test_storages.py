import pytest

from aiogram.fsm.storage.base import BaseStorage, StorageKey
from aiogram.fsm.storage.mongo import MongoStorage


@pytest.mark.parametrize(
    "storage",
    [
        pytest.lazy_fixture("redis_storage"),
        pytest.lazy_fixture("mongo_storage"),
        pytest.lazy_fixture("memory_storage"),
    ],
)
class TestStorages:
    async def test_set_state(self, storage: BaseStorage, storage_key: StorageKey):
        assert await storage.get_state(key=storage_key) is None

        await storage.set_state(key=storage_key, state="state")
        assert await storage.get_state(key=storage_key) == "state"
        await storage.set_state(key=storage_key, state=None)
        assert await storage.get_state(key=storage_key) is None

    async def test_set_data(self, storage: BaseStorage, storage_key: StorageKey):
        assert await storage.get_data(key=storage_key) == {}
        assert await storage.get_value(storage_key=storage_key, dict_key="foo") is None
        assert (
            await storage.get_value(storage_key=storage_key, dict_key="foo", default="baz")
            == "baz"
        )

        await storage.set_data(key=storage_key, data={"foo": "bar"})
        assert await storage.get_data(key=storage_key) == {"foo": "bar"}
        assert await storage.get_value(storage_key=storage_key, dict_key="foo") == "bar"
        assert (
            await storage.get_value(storage_key=storage_key, dict_key="foo", default="baz")
            == "bar"
        )

        await storage.set_data(key=storage_key, data={})
        assert await storage.get_data(key=storage_key) == {}
        assert await storage.get_value(storage_key=storage_key, dict_key="foo") is None
        assert (
            await storage.get_value(storage_key=storage_key, dict_key="foo", default="baz")
            == "baz"
        )

    async def test_update_data(self, storage: BaseStorage, storage_key: StorageKey):
        assert await storage.get_data(key=storage_key) == {}
        assert await storage.update_data(key=storage_key, data={"foo": "bar"}) == {"foo": "bar"}
        assert await storage.update_data(key=storage_key, data={}) == {"foo": "bar"}
        assert await storage.get_data(key=storage_key) == {"foo": "bar"}
        assert await storage.update_data(key=storage_key, data={"baz": "spam"}) == {
            "foo": "bar",
            "baz": "spam",
        }
        assert await storage.get_data(key=storage_key) == {
            "foo": "bar",
            "baz": "spam",
        }
        assert await storage.update_data(key=storage_key, data={"baz": "test"}) == {
            "foo": "bar",
            "baz": "test",
        }
        assert await storage.get_data(key=storage_key) == {
            "foo": "bar",
            "baz": "test",
        }


@pytest.mark.asyncio
async def test_motor_asyncio_client(mongo_server):
    from motor.motor_asyncio import AsyncIOMotorClient

    client = AsyncIOMotorClient(mongo_server)
    storage = MongoStorage(client=client)
    storage_key = StorageKey(chat_id=CHAT_ID, user_id=USER_ID)

    await storage.set_state(storage_key, "test")
    assert await storage.get_state(storage_key) == "test"

    await storage.set_data(storage_key, {"key": "value"})
    assert await storage.get_data(storage_key) == {"key": "value"}

    await storage.set_state(storage_key, None)
    assert await storage.get_state(storage_key) is None

    await storage.set_data(storage_key, {})
    assert await storage.get_data(storage_key) == {}

    await storage.close()


@pytest.mark.asyncio
async def test_pymongo_async_client(mongo_server):
    from pymongo.asynchronous.mongo_client import AsyncMongoClient

    client = AsyncMongoClient(mongo_server)
    storage = MongoStorage(client=client)
    storage_key = StorageKey(chat_id=CHAT_ID, user_id=USER_ID)

    await storage.set_state(storage_key, "test")
    assert await storage.get_state(storage_key) == "test"

    await storage.set_data(storage_key, {"key": "value"})
    assert await storage.get_data(storage_key) == {"key": "value"}

    await storage.set_state(storage_key, None)
    assert await storage.get_state(storage_key) is None

    await storage.set_data(storage_key, {})
    assert await storage.get_data(storage_key) == {}

    await storage.close()
