from unittest.mock import patch, Mock
from api.main import main

@patch("api.main.uvicorn.run")
@patch("api.main.FastAPI")
@patch("api.main.router")
def test_main(router_mock: Mock, fast_api_mock: Mock, uvicorn_mock: Mock):
    app_mock = Mock()
    app_mock.include_router = Mock()
    fast_api_mock.return_value = app_mock
    main()
    fast_api_mock.assert_called_once()
    app_mock.include_router.assert_called_once_with(router_mock, tags=["sensors", "temperature"], prefix="/temperature")
    uvicorn_mock.assert_called_once_with(app_mock, host="0.0.0.0", port=8000, log_level="info", proxy_headers=True)
