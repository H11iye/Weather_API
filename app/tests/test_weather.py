from app.main import app

def test_get_weather_endpoint():
    with app.test_client() as client:
        response = client.get('/weather?city=London')
        assert response.status_code == 200
        data = response.get_json()
        assert 'city' in data
        assert 'temperature' in data
        assert 'description' in data