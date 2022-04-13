# -*- coding: utf-8 -*-
{
    "name": "custom_sales",
    "summary": """
        Custom extension of the sale_management application.""",
    "description": """
        Relate sale.order with hr.employee.
    """,
    "author": "GoLuuk",
    "website": "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Sales",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "sale_management", "hr"],
    # always loaded
    "data": [
        # 'security/ir.model.access.csv',
        "views/views.xml",
        "views/templates.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
}
