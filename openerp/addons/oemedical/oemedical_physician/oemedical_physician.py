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


class OeMedicalPhysician(osv.Model):
    _name = 'oemedical.physician'

    def _get_name(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            res[record.id] = record.physician_id.name
        return res
     
    def _fullname_search(self, cr, uid, obj, name, args, context={}):
        if not len(args):
            return []
        for arg in args:
            cr.execute('SELECT partner.id FROM res_partner partner ' \
                'WHERE partner.name ILIKE %s',('%' + arg[2] + '%',), [])
            res = cr.fetchall()
            if not len(res):
                return [('id', '=', '0')]
        return [('id', 'in', [x[0] for x in res])]
        
    _columns = {
        'physician_id': fields.many2one('res.partner', string='Health Professional',required=True , help='Physician' ,domain=[('is_doctor', '=', 1)]  ),
        'code': fields.char(size=256, string='ID'),
        'name': fields.function(_get_name, type='char', string='Health Professional', help="", multi=False, fnct_search=_fullname_search),
        'specialty': fields.many2one('oemedical.specialty', string='Specialty',required=True, help='Specialty Code'),
        'institution': fields.many2one('res.partner', string='Institution', help='Institution where she/he works' ),
        'info': fields.text(string='Extra info'),
    }

OeMedicalPhysician()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
