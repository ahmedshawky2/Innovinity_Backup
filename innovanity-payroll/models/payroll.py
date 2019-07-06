# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import datetime
from datetime import date
import logging
_logger = logging.getLogger(__name__)


class taxation(models.Model):
    _inherit = 'hr.payslip'

    @api.multi
    def get_salary_m_taxes(self, emp_id, netgross):

        emp_rec = self.env['hr.contract'].search([('employee_id', '=', int(emp_id))])
        dt_start = emp_rec.date_start
        salary = netgross
        _logger.debug('dt_start maged ! "%s"' % (str(dt_start)))
        _logger.debug('salary maged ! "%s"' % (str(salary)))
        result = 0.0

        today = date.today()
        _logger.debug('today maged ! "%s"' % (str(today)))

        start_month =datetime.strptime(str(dt_start),"%Y-%m-%d").month
        _logger.debug('start_month maged ! "%s"' % (str(start_month)))
        start_year =datetime.strptime(str(dt_start),"%Y-%m-%d").year
        _logger.debug('start_year maged ! "%s"' % (str(start_year)))

        current_month = today.month
        _logger.debug('current_month maged ! "%s"' % (str(current_month)))
        current_year = today.year
        _logger.debug('current_year maged ! "%s"' % (str(current_year)))

        exempt_month_slary = 0.0

        if int(current_year) > int(start_year):
            exempt_month_slary = (8000/12)
            _logger.debug('current_year > start_year ==> exempt_month_slary maged ! "%s"' % (str(exempt_month_slary)))

        elif int(current_year) == int(start_year):
            exempt_month_slary = (8000) / (13 - start_month)
            _logger.debug(' current_year == start_year ==> exempt_month_slary maged ! "%s"' % (str(exempt_month_slary)))

        else:
            exempt_month_slary = (8000/12)
            _logger.debug('else ==> exempt_month_slary maged ! "%s"' % (str(exempt_month_slary)))

        personal_exempt = (1/12)*7000

        _logger.debug('personal_exempt maged ! "%s"' % (str(personal_exempt)))

        after_personal_exempt = netgross - personal_exempt

        _logger.debug('after_personal_exempt maged ! "%s"' % (str(after_personal_exempt)))

        tax10 = 0.0
        tax15 = 0.0
        tax20 = 0.0
        tax22_5 = 0.0

        net_salary_after_tax = 0.0

        if after_personal_exempt < 0:
            #net_salary_after_tax = salary
            #result = net_salary_after_tax
            result = tax10 + tax15 + tax20 + tax22_5
            _logger.debug('after_personal_exempt < 0 ==> result maged ! "%s"' % (str(result)))
            return result

        ##if 0 < after_personal_exempt <= (8000/12):
        if 0 < after_personal_exempt <= exempt_month_slary:
            #net_salary_after_tax = salary
            #result = net_salary_after_tax
            result = tax10 + tax15 + tax20 + tax22_5
            _logger.debug('0 < after_personal_exempt <= exempt_month_slary ==> result maged ! "%s"' % (str(result)))
            return result

        else:

            ##after_personal_exempt = after_personal_exempt - (8000/12)
            after_personal_exempt = after_personal_exempt - exempt_month_slary
            _logger.debug('after_personal_exempt maged ! "%s"' % (str(after_personal_exempt)))

            ##if (8000/12) < after_personal_exempt <= (22000/12):
            if exempt_month_slary < after_personal_exempt <= (22000/12):
                tax10 = after_personal_exempt * 0.1
                _logger.debug('exempt_month_slary < after_personal_exempt <= (22000/12) ==> tax10 maged ! "%s"' % (str(tax10)))
                #net_salary_after_tax = salary - tax10
                #result = net_salary_after_tax
                result = tax10 + tax15 + tax20 + tax22_5
                _logger.debug('exempt_month_slary < after_personal_exempt <= (22000/12) ==> result maged ! "%s"' % (str(result)))
                return result

            if (22000/12) < after_personal_exempt <= (37000/12):
                tax10 = (2200/12)
                _logger.debug('(22000/12) < after_personal_exempt <= (37000/12) ==> tax10 maged ! "%s"' % (str(tax10)))
                after_tax10_salary = after_personal_exempt - (22000/12)
                _logger.debug('(22000/12) < after_personal_exempt <= (37000/12) ==> after_tax10_salary maged ! "%s"' % (str(after_tax10_salary)))
                tax15 = after_tax10_salary * 0.15
                _logger.debug('(22000/12) < after_personal_exempt <= (37000/12) ==> tax15 maged ! "%s"' % (str(tax15)))
                #net_salary_after_tax = salary - tax10 - tax15
                #result = net_salary_after_tax
                result = tax10 + tax15 + tax20 + tax22_5
                _logger.debug('(22000/12) < after_personal_exempt <= (37000/12) ==> result maged ! "%s"' % (str(result)))
                return result

            if (37000/12) < after_personal_exempt <= (155000/12):
                tax10 = (2200/12)
                _logger.debug('(37000/12) < after_personal_exempt <= (155000/12) ==> tax10 maged ! "%s"' % (str(tax10)))
                after_tax10_salary = after_personal_exempt - (22000/12)
                _logger.debug('(37000/12) < after_personal_exempt <= (155000/12) ==> after_tax10_salary maged ! "%s"' % (str(after_tax10_salary)))
                tax15 = (2250/12)
                _logger.debug('(37000/12) < after_personal_exempt <= (155000/12) ==> tax15 maged ! "%s"' % (str(tax15)))
                after_tax15_salary = after_tax10_salary - (15000 / 12)
                _logger.debug('(37000/12) < after_personal_exempt <= (155000/12) ==> after_tax15_salary maged ! "%s"' % (str(after_tax15_salary)))
                tax20 = after_tax15_salary * 0.2
                _logger.debug('(37000/12) < after_personal_exempt <= (155000/12) ==> tax20 maged ! "%s"' % (str(tax20)))
                #net_salary_after_tax = salary - tax10 - tax15 - tax20
                #result = net_salary_after_tax
                result = tax10 + tax15 + tax20 + tax22_5
                _logger.debug('(37000/12) < after_personal_exempt <= (155000/12) ==> result maged ! "%s"' % (str(result)))
                return result


            if (155000/12) < after_personal_exempt:
                tax10 = (2200/12)
                _logger.debug('(155000/12) < after_personal_exempt ==> tax10 maged ! "%s"' % (str(tax10)))
                after_tax10_salary = after_personal_exempt - (22000/12)
                _logger.debug('(155000/12) < after_personal_exempt ==> after_tax10_salary maged ! "%s"' % (str(after_tax10_salary)))
                tax15 = (2250/12)
                _logger.debug('(155000/12) < after_personal_exempt ==> tax15 maged ! "%s"' % (str(tax15)))
                after_tax15_salary = after_tax10_salary - (15000/12)
                _logger.debug('(155000/12) < after_personal_exempt ==> after_tax15_salary maged ! "%s"' % (str(after_tax15_salary)))
                tax20 = (31000/12)
                _logger.debug('(155000/12) < after_personal_exempt ==> tax20 maged ! "%s"' % (str(tax20)))
                after_tax20_salary = after_tax15_salary - (155000/12)
                _logger.debug('(155000/12) < after_personal_exempt ==> after_tax20_salary maged ! "%s"' % (str(after_tax20_salary)))
                tax22_5 = after_tax20_salary * 0.225
                _logger.debug('(155000/12) < after_personal_exempt ==> tax22_5 maged ! "%s"' % (str(tax22_5)))
                #net_salary_after_tax = salary - tax10 - tax15 - tax20 - tax22_5
                #result = net_salary_after_tax
                result = tax10 + tax15 + tax20 + tax22_5
                _logger.debug('(155000/12) < after_personal_exempt ==> result maged ! "%s"' % (str(result)))
                return result

    @api.multi
    def get_insurance_company_share(self, emp_id):
        emp_rec = self.env['hr.contract'].search([('employee_id', '=', int(emp_id))])
        dt_start = emp_rec.date_start
        basic_salary = emp_rec.wage
        result = 0.0
        result = basic_salary * 0.26
        return result

    @api.multi
    def get_social_insurance(self, emp_id):
        emp_rec = self.env['hr.contract'].search([('employee_id', '=', int(emp_id))])
        dt_start = emp_rec.date_start
        basic_salary = emp_rec.wage
        result = 0.0
        result = (basic_salary * 0.40) * -1
        return result

    @api.multi
    def sum_inputs_codes(self, payslip_id, code, contract_id):

        _logger.debug('self.id maged ! "%s"' % (str(payslip_id)))
        _logger.debug('code maged ! "%s"' % (str(code)))
        _logger.debug('contract_id maged ! "%s"' % (str(contract_id)))

        inputs = self.env['hr.payslip.input'].search([('payslip_id','=',payslip_id)])
        _logger.debug('inputs maged ! "%s"' % (str(inputs)))

        result = 0.0

        for input in inputs:
            if input[0]['code'] == code and int(input[0]['contract_id']) == contract_id:
                result = result + input[0]['amount']

        _logger.debug('result maged ! "%s"' % (str(result)))

        return result