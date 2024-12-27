from pytest import fixture

description = """
--- Part Two ---
While the Elves get to work printing the correctly-ordered updates, you have a little time to fix the rest of them.

For each of the incorrectly-ordered updates, use the page ordering rules to put the page numbers in the right order. For the above example, here are the three incorrectly-ordered updates and their correct orderings:

75,97,47,61,53 becomes 97,75,47,61,53.
61,13,29 becomes 61,29,13.
97,13,75,29,47 becomes 97,75,47,29,13.
After taking only the incorrectly-ordered updates and ordering them correctly, their middle page numbers are 47, 29, and 47. Adding these together produces 123.

Find the updates which are not in the correct order. What do you get if you add up the middle page numbers after correctly ordering just those updates?
"""

from .part_2 import get_incorrect_order_updates, reorder_updates
from .part_1 import find_middle_page_numbers


@fixture
def page_data():
    page_ordering_rules = [
        "47|53", "97|13", "97|61", "97|47", "75|29",
        "61|13", "75|53", "29|13", "97|29", "53|29",
        "61|53", "97|53", "61|29", "47|13", "75|47",
        "97|75", "47|61", "75|61", "47|29", "75|13", "53|13"
    ]
    pages_to_produce = [
        "75,47,61,53,29",
        "97,61,53,29,13",
        "75,29,13",
        "75,97,47,61,53",
        "61,13,29",
        "97,13,75,29,47"
    ]
    return page_ordering_rules, pages_to_produce


def test_get_incorrect_order_updates(page_data):
    page_ordering_rules = [list(map(int, rule.split('|'))) for rule in page_data[0]]
    pages_to_produce = [list(map(int, page.split(','))) for page in page_data[1]]
    incorrect_updates = get_incorrect_order_updates(page_ordering_rules, pages_to_produce)
    expected = [
        [75,97,47,61,53],
        [61,13,29],
        [97,13,75,29,47]
    ]
    assert incorrect_updates == expected


def test_reorder_updates(page_data):
    page_ordering_rules = [list(map(int, rule.split('|'))) for rule in page_data[0]]

    incorrect_updates = [
        [75,97,47,61,53],
        [61,13,29],
        [97,13,75,29,47]
    ]

    reordered = reorder_updates(ordering_rules=page_ordering_rules,
                                pages=incorrect_updates)
    expected = [
        [97,75,47,61,53],
        [61,29,13],
        [97,75,47,29,13]
    ]
    assert reordered == expected


def test_calculate_middle_sum():
    reordered_updates = [
        "97,75,47,61,53",
        "61,29,13",
        "97,75,47,29,13"
    ]
    converted_pages = [list(map(int, page.split(','))) for page in reordered_updates]
    middle_pages = find_middle_page_numbers(converted_pages)

    assert sum(middle_pages) == 123
