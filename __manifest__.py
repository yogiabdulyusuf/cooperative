{
	"name": "Cooperative",
	"version": "1.0", 
	"depends": [
		"base",
		"account",
		"account_voucher",
	],
	"author": "jakc-labs",
	"category": "Cooperative",
	'website': 'http://www.jakc-labs.com',
	"description": """

Cooperative
======================================================================

* this is my Cooperative system module
* created menu:
* created object
* created views
* logic:

""",
	"data": [
		"view/billing_view.xml",
		"view/membership_view.xml",
		"view/savings_view.xml",
		"view/loan_view.xml",
		"view/deposit_view.xml",
		"view/settings_view.xml",
		"view/top_menu.xml",
		"data/ir_sequence.xml",
	],
	"installable": True,
	"auto_install": False,
    "application": True,
}