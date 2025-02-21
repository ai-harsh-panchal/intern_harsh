# Changelog

- action_book_list` Method:
        - Use a unified action dictionary for better readability.
        - Dynamically set the `name`, `view_mode`, and `domain` based on the number of book records.
        - Align logic with reference implementation for consistency and scalability.


- revert_changes` Method:
    - Optimized the record deletion mechanism by combining the search criteria using the `in` operator.
    - Replaced the loop with a single `.unlink()` call on the result set, reducing redundancy and improving performance.

- compute_count_book` Method:
    - Simplified the computation logic:
        - Utilized a list comprehension to strip and prepare book names.
        - Replaced iterative counting with a single call to `.search_count` using a domain with the `in` operator.


