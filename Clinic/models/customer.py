from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError


import logging
_logger = logging.getLogger(__name__)


class customer (models.Model):
    _inherit = 'res.partner'
    x_child_name = fields.Char(string="Child/Sub Name", required=True, index=True, track_visibility=True,default="Parent")
    x_cr = fields.Char(string="Commercial Registration", required=False, index=True, track_visibility=False)



    _sql_constraints = [('constrainname','UNIQUE (phone,x_child_name)','Customer Phone And Child Name already exists'), ]
