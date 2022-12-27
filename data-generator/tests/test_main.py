"""test main module."""
import pytest
from unittest.mock import patch

@pytest.mark.unit
class TestMainModule:
    def test_insert_generator(self):
        """test insert generator."""
        with patch("generator.insert.InsertGenerator") as mock_insert_generator:
            from generator.main import main
            main()
            mock_insert_generator.assert_called_once_with()
            mock_insert_generator.return_value.run.assert_called_once_with()
