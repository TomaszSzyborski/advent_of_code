import copy

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
from part_1 import get_print_data, find_middle_page_numbers

def get_incorrect_order_updates(page_ordering_rules: list[list[int]], pages_to_produce: list[list[int]]):
    incorrect_order_updates = []
    for update in pages_to_produce:
        if not is_in_correct_order(page_ordering_rules, update):
            incorrect_order_updates.append(update)

    return incorrect_order_updates


def is_in_correct_order(ordering_rules, pages):
    for rule in ordering_rules:
        before, after = rule
        if before not in pages or after not in pages:
            continue
        if pages.index(before) > pages.index(after):
            return False
    return True


def reorder_updates(pages: list[list[int]], ordering_rules: list[list[int]]) -> list[list[int]]:
    reordered = []
    for page in pages:
        new_page = copy.deepcopy(page)
        while not is_in_correct_order(ordering_rules, new_page):
            for rule in ordering_rules:
                before, after = rule
                applicable = before in new_page and after in new_page
                if applicable:
                    before_index = new_page.index(before)
                    after_index = new_page.index(after)
                    if before_index > after_index:
                        new_page[before_index], new_page[after_index] = new_page[after_index], new_page[before_index]
        reordered.append(new_page)
    return reordered


def main():
    page_ordering_rules, pages_to_produce = get_print_data("puzzle_input.txt")
    page_ordering_rules = [list(map(int, rule.split('|'))) for rule in page_ordering_rules]
    pages_to_produce = [list(map(int, page.split(','))) for page in pages_to_produce]
    incorrect_order_updates = get_incorrect_order_updates(page_ordering_rules, pages_to_produce)
    print(incorrect_order_updates)
    reordered_updates = reorder_updates(incorrect_order_updates, page_ordering_rules)
    middle_page_numbers = find_middle_page_numbers(reordered_updates)
    print(sum(middle_page_numbers))


if __name__ == '__main__':
    main()
    #6370 correct at first attempt