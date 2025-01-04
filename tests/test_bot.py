import json

def test_webhook(client, mock_telegram_api):
    """Проверка обработки вебхука на сервере"""
    update = {
        "update_id": 10000,
        "message": {
            "message_id": 1,
            "from": {"id": 12345, "is_bot": False, "first_name": "Test", "username": "test_user"},
            "chat": {"id": 12345, "first_name": "Test", "type": "private"},
            "date": 1636000000,
            "text": "/start",
        },
    }
    response = client.post("/webhook", data=json.dumps(update), content_type="application/json")
    assert response.status_code == 200
