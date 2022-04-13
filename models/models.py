# -*- coding: utf-8 -*-
import random
from odoo import models, fields, api


class CustomEmployee(models.Model):
    _inherit = "hr.employee"

    ONLINE = "online"
    BUSY = "busy"
    OFFLINE = "offline"
    session_status = fields.Selection(
        [(ONLINE, "Online"), (BUSY, "Busy"), (OFFLINE, "Offline")]
    )
    order_ids = fields.One2many("sale.order", "employee_id")
    total_orders = fields.Integer(
        compute="_compute_total_orders", default=0, store=True
    )

    @api.depends("order_ids")
    def _compute_total_orders(self):
        for employee in self:
            employee.total_orders = len(employee.order_ids)


class CustomSale(models.Model):
    _inherit = "sale.order"

    employee_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Employee",
        compute="_compute_employee",
        store=True,
    )

    @api.depends("state")
    def _compute_employee(self):
        for order in self:
            if not order.employee_id and order.state == "sale":
                # try to get an employee that is online
                employee = self._get_employee(
                    self.env["hr.employee"].search(
                        [("session_status", "=", "online")], order="total_orders asc"
                    )
                )
                # if not online employee, try to get an employee that is busy
                if not employee:
                    employee = self._get_employee(
                        self.env["hr.employee"].search(
                            [("session_status", "=", "busy")], order="total_orders asc"
                        )
                    )
                # if no online or busy employee, get any employee with the least amount of orders
                if not employee:
                    employee = self._get_employee(
                        self.env["hr.employee"].search([], order="total_orders asc")
                    )
                print(employee)
                order.employee_id = employee.id

    def _get_employee(self, employees):
        # get the records
        employees = self.env["hr.employee"].browse(employees)

        print("------------ EMPLOYEE: " + str(employees))
        if len(employees) > 0:
            return employees[0]

        return None
