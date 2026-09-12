import my_model


def test_model_serializes_and_produces_schema() -> None:
    record = my_model.user.User(name="Test", username="test", password="x", api_key="y")

    dumped = record.model_dump()
    assert dumped["name"] == "Test"

    dumped_json = record.model_dump_json()
    assert '"name":"Test"' in dumped_json.replace(" ", "")

    schema = my_model.user.User.model_json_schema()
    assert "name" in schema["properties"]


def test_model_round_trips_through_validation() -> None:
    broker = my_model.broker.Broker(name="FxPro", user_id=1)
    restored = my_model.broker.Broker.model_validate(broker.model_dump())
    assert restored == broker
