# filepath: server/utils/validators.py

def validate_dog_age(age):
    """
    Validates a dog's age to ensure it's within acceptable bounds.
    
    Args:
        age: The age value to validate (should be an integer)
        
    Returns:
        int: The validated age
        
    Raises:
        ValueError: If age is None, not an integer, or outside the range 0-20
        
    Examples:
        >>> validate_dog_age(5)
        5
        >>> validate_dog_age(0)
        0
        >>> validate_dog_age(20)
        20
        >>> validate_dog_age(-1)
        Traceback (most recent call last):
        ...
        ValueError: Age must be between 0 and 20 years
        >>> validate_dog_age(21)
        Traceback (most recent call last):
        ...
        ValueError: Age must be between 0 and 20 years
        >>> validate_dog_age(None)
        Traceback (most recent call last):
        ...
        ValueError: Age cannot be empty
        >>> validate_dog_age("5")
        Traceback (most recent call last):
        ...
        ValueError: Age must be an integer
    """
    if age is None:
        raise ValueError("Age cannot be empty")
    
    # Check for boolean values explicitly since bool is a subclass of int in Python
    if isinstance(age, bool) or not isinstance(age, int):
        raise ValueError("Age must be an integer")
    
    if age < 0 or age > 20:
        raise ValueError("Age must be between 0 and 20 years")
    
    return age


def validate_dog_age_safe(age):
    """
    A safe version of validate_dog_age that returns a tuple indicating success.
    
    Args:
        age: The age value to validate
        
    Returns:
        tuple: (is_valid: bool, result: int | str)
               If valid: (True, validated_age)
               If invalid: (False, error_message)
               
    Examples:
        >>> validate_dog_age_safe(5)
        (True, 5)
        >>> validate_dog_age_safe(-1)
        (False, 'Age must be between 0 and 20 years')
        >>> validate_dog_age_safe(None)
        (False, 'Age cannot be empty')
    """
    try:
        validated_age = validate_dog_age(age)
        return (True, validated_age)
    except ValueError as e:
        return (False, str(e))


if __name__ == "__main__":
    # Run doctests
    import doctest
    doctest.testmod()
    
    # Additional manual tests
    print("Running manual tests...")
    
    # Test valid ages
    valid_ages = [0, 1, 5, 10, 15, 20]
    print("Testing valid ages:")
    for age in valid_ages:
        try:
            result = validate_dog_age(age)
            print(f"  Age {age}: ✓ Valid (returned {result})")
        except ValueError as e:
            print(f"  Age {age}: ✗ Unexpected error - {e}")
    
    # Test invalid ages
    invalid_ages = [-1, -10, 21, 25, 50, None, "5", 5.5]
    print("\nTesting invalid ages:")
    for age in invalid_ages:
        try:
            validate_dog_age(age)
            print(f"  Age {age}: ✗ Should have failed but didn't")
        except ValueError as e:
            print(f"  Age {age}: ✓ Correctly rejected - {e}")
    
    # Test safe version
    print("\nTesting safe validation:")
    test_ages = [5, -1, None, "invalid"]
    for age in test_ages:
        is_valid, result = validate_dog_age_safe(age)
        status = "✓" if is_valid else "✗"
        print(f"  Age {age}: {status} {result}")
