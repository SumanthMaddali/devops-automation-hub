from app.validator import validate_yaml_only

def test_valid_yaml():
    text = "key: value"
    result = validate_yaml_only(text)
    assert result["valid"] is True
    assert result["syntax_errors"] == []

def test_invalid_yaml():
    text = "key value"  # missing colon
    result = validate_yaml_only(text)
    assert result["valid"] is False
    assert len(result["syntax_errors"]) > 0
