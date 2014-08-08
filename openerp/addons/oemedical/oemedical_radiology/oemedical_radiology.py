# -*- coding: utf-8 -*-
#/#############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2004-TODAY Tech-Receptives(<http://www.techreceptives.com>)
#    Special Credit and Thanks to Thymbra Latinoamericana S.A.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#/#############################################################################

from osv import osv
from osv import fields
import time


# class oemedical_patient(osv.osv):
#
#     _inherit='oemedical.patient'
#     _name = 'oemedical.patient'
#
#     _columns = {
#
#     }
#
# oemedical_patient()

class oemedical_patient(osv.osv):
    _name = "oemedical.patient"
    _inherit = "oemedical.patient"

    _columns = {
        'radio_scan_ids': fields.one2many('oemedical.patient.radio.scan', 'patient_id', 'Radio Scan'),
    }


class radio_type(osv.osv):
    _name = "oemedical.radio_type"
    _description = "Type of Radio Scan"
    _columns = {
        'name': fields.char('Radio', size=128, help="Radio type, eg ...", required=True),
        'code': fields.char('Code', size=128, help="Short name - code for the test"),
        'info': fields.text('Description'),
    }
    _sql_constraints = [
        ('code_uniq', 'unique (name)', 'The Radio Scan code must be unique')]


class oemedical_patient_radio_scan(osv.osv):
    _name = 'oemedical.patient.radio.scan'

    def _get_default_dr(self, cr, uid, context={}):
        partner_id = self.pool.get('res.partner').search(cr, uid, [('user_id', '=', uid)])
        if partner_id:
            dr_id = self.pool.get('oemedical.physician').search(cr, uid, [('name', '=', partner_id[0])])
            if dr_id:
                return dr_id[0]
                #else:
                #    raise osv.except_osv(_('Error !'),
                #            _('There is no physician defined ' \
                #                    'for current user.'))
        else:
            return False

    _columns = {
        'name': fields.many2one('oemedical.radio_type', 'Radio Type'),
        'date': fields.datetime('Date'),
        'state': fields.selection([('draft', 'Draft'), ('scanned', 'Scanned'), ('cancel', 'Cancel')], 'State',
                                  readonly=True),
        'patient_id': fields.many2one('oemedical.patient', 'Patient'),
        'doctor_id': fields.many2one('oemedical.physician', 'Doctor', help="Doctor who performed the Radio Scan."),

    }

    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'state': lambda *a: 'draft',
        'doctor_id': _get_default_dr,
    }