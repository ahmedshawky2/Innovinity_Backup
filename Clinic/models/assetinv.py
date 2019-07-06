from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError


import logging
_logger = logging.getLogger(__name__)


class assetinv (models.Model):
    _inherit = 'account.asset.asset'
    x_dep_rate = fields.Char(string = "Depreciations Rate",compute='deprate')
    x_total_monthe  = fields.Integer(string ="Total Months" ,compute='TotalMonths', required=False)

    @api.depends('x_total_monthe')
    @api.one
    def deprate(self):
        if( not self.value or self.value == 0):
            self.x_dep_rate = 0;
        else:
            self.x_dep_rate = round(((self.value / self.x_total_monthe)*(100*12)/self.value),0)

            if float(self.x_dep_rate) > 100:
                self.x_dep_rate = 100

    @api.one
    def TotalMonths(self):
        self.x_total_monthe = self.method_number * self.method_period


