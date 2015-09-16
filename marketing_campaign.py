# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2015-Today BrowseInfo (<http://www.browseinfo.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

import time
from datetime import datetime

from openerp import api
from openerp.osv import fields, osv


class marketing_campaign_activity(osv.osv):
    _inherit = "marketing.campaign.activity"
    _description = "Campaign Activity"

    _columns = {
        'expect_email_accounts': fields.char(string='Except Email Accounts'),
    }

    def _process_wi_email(self, cr, uid, activity, workitem, context=None):
        print '\n _process_wi_email of activity',activity,workitem.res_id,context,activity.expect_email_accounts
        except_email_list = []
        if activity.expect_email_accounts and workitem.partner_id:
            except_email_list = activity.expect_email_accounts.split(',')
            part_email = workitem.partner_id.email and workitem.partner_id.email.split('@') or []
            print '\n partner_id',workitem.partner_id.email,except_email_list,part_email
            if len(part_email) == 2:
                part_email = '@' + part_email[1]
                if part_email in except_email_list:
                    print '\n part_email',part_email,except_email_list
                    return None
                else:
                    return self.pool.get('email.template').send_mail(cr, uid,
                                            activity.email_template_id.id,
                                            workitem.res_id, context=context)
        else:
            return self.pool.get('email.template').send_mail(cr, uid,
                        activity.email_template_id.id,
                        workitem.res_id, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
