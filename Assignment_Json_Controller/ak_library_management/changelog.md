# Changelog

## [18.0.1.0.1] - 2025-03-07 | Assignment Borrow Book Requirement


### changes
- add comodel_name in every relational field 
- use filtered() instead of more for loops and if condition in function 
- manage doc string of every function
- use limit=1 in the search method in action_borrow_books function instead of index 
- required the customer_id field for borrow the books
- fix the error in action_borrow_books function 

## [18.0.1.0.1] - 2025-03-12

### changes
- update the warning message in borrow book requirement when product stock level 0 
- fix the decrease of stock quantity of each product when borrowed


## [18.0.1.0.2] - 17-03-25 | Assignment schedule action and server action

### changes
- update a _cron_notify_due_returns() in borrow book transaction py file as per the requirement 
- use filtered function in action_return_books() where i have use for loops 
- update a varaible name in proper meaningfull


## [18.0.1.0.2] - 17-03-25 | Assignment mail template, mail compose wizard, attach report in mail template

### changes 
- add changelog 
- manage version in manifest
- update doc string of action_send_mail() in library_member py file 
- add module_name in model_id field in borrow_transaction_ir_action xml file 
- update the name of function with _cron_send_overdue_notices in borrow trasaction py file

## [18.0.1.0.3] - 19-03-25 | Assignment Schedule action

### changes 
- use appropriate variable name borrow transaction model py file
- improve the logic of _cron_notify_due_returns() function borrow transaction model 


## [18.0.1.0.3] - 19-03-25 | Assignment Borrow Book Requirement 

### changes
- Multiple warnings display to the user sequentially, when all condition match in borrow book transaction model

## [18.0.1.1.0] - 21-03-25 | Assignment Library report customization 

### changes
- remove the html tag and other from custom_report_library_library and Use Odoo layout instead of HTML.
- use table class for manage width and table format instead of setting a static width.
- Update email and phone details in library_library_report_template
- update version in manifest

## [18.0.1.2.0] - 26-03-25 | Assignment Modify Existing/Base Qweb reports

### changes 
- add report_invoice.xml file for modify base sale order invoice report

## [18.0.1.2.1] - 28-03-25 | Assignment Dynamic HTTP Controller

### changes
- implement slug in res partner model py file 
- create a kanban view in dynamic web page xml file for contact list 
- change the view of partner details from list to form view as per odoo standard 
- manage controller function for partner details and contact list 

## [18.0.1.3.0] - 01-04-25 | Assignment Json Controller

### Added 
- add customer_page xml file for display and fetch the data of contact

## [18.0.1.4.0] - 01-04-25 | Assignment Front-end - Practical Task (POS 18 products section)

### Added
- add product_list_page_view and product_screen xml file in xml folder

## [18.0.1.5.0] - 02-04-25 | Assignment Front-end - Practical Task (Download Product Images)

### Added 
- add product template website view xml file in views 

## [18.0.1.6.0] - 04-04-25 | Assignment Vendor management system

### Added 
- add product_product, product_supllierinfo py file  in models

## [18.0.1.6.1] - 11-04-25 | Assignment modify base report

### changes 
- apply proper space in header section in report_invoice xml file
- and manage payment term in invoice 

## [18.0.1.6.2] - 14-04-25 | Assignment json controller

### changes
- modify controller/main.py file add doc string for particular each functions
- modify customer_page xml file add warning message if user entered wrong email id for fetch data

