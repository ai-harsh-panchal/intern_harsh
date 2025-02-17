# Changelog

Changed
- Created a new menu for the product with the title starting with a capital letter.
- Updated the default value for the "Is Library Book" field to `False`. 
  - Clarification: If the "Is Library Book" checkbox is checked and changed, it is not a required field. This allows flexibility for products that may not always be library books.
- Set the "Available in Stock" field to default to `True`.
  - Verification: This setting is appropriate for both product and book records, ensuring that new entries are marked as available by default unless specified otherwise.

Fixed
- Reviewed the inherited view from `product.product_template_form_view`. Ensured that the correct view is inherited for the task.
- Updated the requirement for custom book fields:
  - All custom book fields are now required only if the "Can be Sold" flag is set to `True` at the product level.
  - Adjusted the base barcode field to not be required if the "Can be Sold" flag is `False`, aligning with assignment requirements.

