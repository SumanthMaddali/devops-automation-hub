from app.validator import validate_yaml_only


def test_valid_yaml():
    yaml_text = """
    name: test
    value: 123
    """
    result = validate_yaml_only(yaml_text)

    assert result["valid"] is True
    assert result["syntax_errors"] == []
    assert result["parsed"] == {"name": "test", "value": 123}


def test_invalid_yaml():
    invalid_yaml = """
    name test:   # Missing colon
      - item1
    """

    result = validate_yaml_only(invalid_yaml)

    assert result["valid"] is False
    assert len(result["syntax_errors"]) > 0
