from .part_1 import extract_mul_instructions


# Unit test
def test_extract_mul_instructions():
    data = "xmul(2,4)%&mul(3,7)!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    expected = [("2", "4"), ("3", "7"), ("5", "5"), ("11", "8"), ("8", "5")]
    assert extract_mul_instructions(data) == expected


def test_extract_mul_instructions_empty():
    data = ""
    expected = []
    assert extract_mul_instructions(data) == expected


def test_extract_mul_instructions_no_valid():
    data = "xmul(2 ,4)%&do_not_mul(5*,5)+mul(32,64]then(mul(i11,8)mul(l8,5))"
    expected = []
    assert extract_mul_instructions(data) == expected


def test_extract_mul_instructions_mul_at_start():
    data = "mul(2,4)%&mul(3,7)!@^do_not_mul(s5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    expected = [("2", "4"), ("3", "7"), ("11", "8"), ("8", "5")]
    assert extract_mul_instructions(data) == expected


def test_extract_mul_instructions_mul_at_end():
    data = "xmul(2,4^)%&mul(3,7)!@^do_not_mul(#5,5)+mul(32,64]then(mul(11,8)mul(8,5)mul(2,3)"
    expected = [("3", "7"), ("11", "8"), ("8", "5"), ("2", "3")]
    assert extract_mul_instructions(data) == expected


from .part_1 import transform_extracted_tuples_to_int_tuples


def test_clear_data():
    data = "xmul(2,4)%&mul(3,7)!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    extracted_data = extract_mul_instructions(data)
    expected = [(2, 4), (3, 7), (5, 5), (11, 8), (8, 5)]
    assert transform_extracted_tuples_to_int_tuples(extracted_data) == expected


def test_clear_data_empty():
    data = ""
    extracted_data = extract_mul_instructions(data)
    expected = []
    assert transform_extracted_tuples_to_int_tuples(extracted_data) == expected
