# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import datetime
from datetime import date
import logging
_logger = logging.getLogger(__name__)


class hrContractExtend(models.Model):

    _inherit = "hr.contract"

    basic_insurance_salary = fields.Monetary('Basic Social Insurance Salary', digits=(16, 2), track_visibility="always",
                           help="Employee's monthly basic social insurance salary.",index=True,store=True)

    var_insurance_salary = fields.Monetary('Variable Social Insurance Salary', digits=(16, 2), track_visibility="always",
                           help="Employee's monthly variable social insurance salary.",index=True,store=True)