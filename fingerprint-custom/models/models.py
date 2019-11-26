# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pandas as pd
import http.client
import requests
import datetime
import json
from operator import attrgetter
from datetime import timedelta
from zk import ZK, const
import logging
_logger = logging.getLogger(__name__)

class zkattendance(models.Model):
    _inherit = 'hr.attendance'

    def getAttendance(self):

        active_devices = self.env['devices'].search([('status', '=', True)])

        for d in active_devices:
            ipaddress = d[0]['ip_address']
            port = d[0]['port']
            zk = ZK(ipaddress, port=int(port), timeout=60)
            _logger.info('d maged ! "%s"' % (str(d)))

            _logger.info('Connecting to device ...')
            conn = zk.connect()
            conn.disable_device()
            _logger.info('Disconnected device ...')

            listof_attendance = conn.get_attendance()

            #_logger.info('listof_attendance maged ! "%s"' % (str(listof_attendance)))

            list_of_user_checkin_timestamp = []
            list_of_user_checkout_timestamp = []
            fullFinalList = []
            garbageList = []
            removeList = []
            cloneList = listof_attendance

            #_logger.info('cloneList maged ! "%s"' % (str(cloneList)))

            for index in cloneList:
                #_logger.info('index maged ! "%s"' % (str(index)))

                removeList.clear()
                user1_id = index.user_id
                checkType1 = index.punch
                _time1 = index.timestamp

                #_logger.info('user1_id maged ! "%s"' % (str(user1_id)))
                #_logger.info('checkType1 maged ! "%s"' % (str(checkType1)))
                #_logger.info('_time1 maged ! "%s"' % (str(_time1)))

                list_of_user_checkin_timestamp.clear()
                list_of_user_checkout_timestamp.clear()
                _time1_convert = datetime.datetime.strptime(str(_time1), '%Y-%m-%d %H:%M:%S').date()
                _time1_convert_dateTimeFull = datetime.datetime.strptime(str(_time1), '%Y-%m-%d %H:%M:%S')

                go = True
                # print(index)
                # print(len(removeList))

                if go:
                    notFound = True
                    for index2 in range(len(listof_attendance)):

                        #_logger.info('index2 maged ! "%s"' % (str(index2)))

                        user2_id = listof_attendance[index2].user_id
                        checkType2 = listof_attendance[index2].punch
                        _time2 = listof_attendance[index2].timestamp

                        #_logger.info('user2_id maged ! "%s"' % (str(user2_id)))
                        #_logger.info('checkType2 maged ! "%s"' % (str(checkType2)))
                        #_logger.info('_time2 maged ! "%s"' % (str(_time2)))

                        _time2_convert = datetime.datetime.strptime(str(_time2), '%Y-%m-%d %H:%M:%S').date()
                        _time2_convert_dateTimeFull = datetime.datetime.strptime(str(_time2), '%Y-%m-%d %H:%M:%S')

                        if (user2_id == user1_id and checkType2 == 0 and (_time1_convert == _time2_convert)
                                and _time2_convert_dateTimeFull >= datetime.datetime.strptime(
                                    str(_time2_convert) + ' 05:00', '%Y-%m-%d %H:%M')):
                            # timestamp = myFile.values[index2][1]
                            list_of_user_checkin_timestamp.append(_time2_convert_dateTimeFull)
                            garbageList.append([user1_id, _time2_convert_dateTimeFull])
                            removeList.append(listof_attendance[index2])
                            notFound = True

                            # print(str(user1_id) + "==>" + str(_time1_convert_dateTimeFull) + "<====>" +
                            # str(user2_id) + "==>" + str(_time2_convert_dateTimeFull))
                    # print(removeList)
                    # print("----------------check in remove list-----------------------------")
                    # print(len(removeList))
                    # print("**********")
                    # removeList = list(dict.fromkeys(removeList))
                    # print("**********")
                    # print(len(removeList))
                    for s in removeList:
                        listof_attendance.remove(s)

                    for index3 in range(len(listof_attendance)):

                        #_logger.info('index3 maged ! "%s"' % (str(index3)))

                        removeList.clear()
                        user3_id = listof_attendance[index3].user_id
                        checkType3 = listof_attendance[index3].punch
                        _time3 = listof_attendance[index3].timestamp

                        #_logger.info('user3_id maged ! "%s"' % (str(user3_id)))
                        #_logger.info('checkType3 maged ! "%s"' % (str(checkType3)))
                        #_logger.info('_time3 maged ! "%s"' % (str(_time3)))

                        _time3_convert = datetime.datetime.strptime(str(_time3), '%Y-%m-%d %H:%M:%S').date()
                        _time3_convert_dateTimeFull = datetime.datetime.strptime(str(_time3), '%Y-%m-%d %H:%M:%S')

                        if (user3_id == user1_id and checkType3 == 1):

                            if _time1_convert == _time3_convert:
                                list_of_user_checkout_timestamp.append(_time3_convert_dateTimeFull)
                                garbageList.append([user1_id, _time3_convert_dateTimeFull])
                                removeList.append(listof_attendance[index3])
                                # print(str(user1_id) + "==>" + str(_time1_convert_dateTimeFull) + "<====>" +
                                # str(user3_id) + "==>" + str(_time3_convert_dateTimeFull))
                                notFound = True

                            elif _time1_convert + timedelta(days=1) == _time3_convert \
                                    and _time3_convert_dateTimeFull \
                                    <= datetime.datetime.strptime(str(_time1_convert + timedelta(days=1)) + ' 04:59',
                                                                  '%Y-%m-%d %H:%M'):
                                list_of_user_checkout_timestamp.append(_time3_convert_dateTimeFull)
                                garbageList.append([user1_id, _time3_convert_dateTimeFull])
                                removeList.append(listof_attendance[index3])
                                # print(str(user1_id) + "==>" + str(_time1_convert_dateTimeFull) + "<====>" +
                                # str(user3_id) + "==>" + str(_time3_convert_dateTimeFull))
                                notFound = True
                    for s in removeList:
                        listof_attendance.remove(s)

                    if len(list_of_user_checkin_timestamp) > 0 and len(list_of_user_checkout_timestamp) > 0:
                        min_timestamp = sorted(list_of_user_checkin_timestamp, reverse=True)[
                            len(list_of_user_checkin_timestamp) - 1]
                        max_timestamp = sorted(list_of_user_checkout_timestamp, reverse=True)[0]
                        fullFinalList.append([user1_id, min_timestamp, max_timestamp])

                    '''else:
                        if len(list_of_user_checkin_timestamp) > 0 and len(list_of_user_checkout_timestamp) <= 0:
                            min_timestamp = sorted(list_of_user_checkin_timestamp, reverse=True)[
                                len(list_of_user_checkin_timestamp) - 1]
                            max_timestamp = sorted(list_of_user_checkin_timestamp, reverse=True)[0]
                            fullFinalList.append([user1_id, min_timestamp, max_timestamp])

                        elif len(list_of_user_checkin_timestamp) <= 0 and len(list_of_user_checkout_timestamp) > 0:
                            min_timestamp = sorted(list_of_user_checkout_timestamp, reverse=True)[
                                len(list_of_user_checkout_timestamp) - 1]
                            max_timestamp = sorted(list_of_user_checkout_timestamp, reverse=True)[0]
                            fullFinalList.append([user1_id, min_timestamp, max_timestamp])'''

            *fullFinalList, = map(list, {*map(tuple, fullFinalList)})

            for x in fullFinalList:
                #_logger.info('x maged ! "%s"' % (str(x)))

                check_full_record = self.env['hr.attendance'].search([('employee_id', '=', int(x[0])),
                                                                      ('check_in','=',x[1]),
                                                                      ('check_out','=',x[2])])

                if check_full_record:
                    pass
                else:
                    check_update_record = self.env['hr.attendance'].search([('employee_id', '=', int(x[0])),
                                                                          ('check_in', '=', x[1])])

                    if check_update_record:
                        check_update_record[0]['check_out'] = x[2]
                    else:
                        try:
                            self.env['hr.attendance'].create({
                                'employee_id': int(str(x[0])),
                                'check_in': x[1],
                                'check_out': x[2],
                            })
                        except:
                            pass

        return True


class zkdevices(models.Model):
    _name = 'devices'

    ip_address = fields.Char(name="IP Address", index=True, default="0.0.0.0")
    port = fields.Char(name="Port Number", index=True, default="5005")
    status = fields.Boolean(name="Status", index=True, default=True)