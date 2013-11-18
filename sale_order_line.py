from osv import fields, osv
from datetime import datetime as dt
from datetime import date
from datetime import timedelta

class lot_to_sale_order_line(osv.osv_memory):
    _name='sale.order.line'
    _inherit='sale.order.line'
    
    _columns = {
        #'dd': fields.function(_get_date, method=True, type='char',store=True, string='Delivery date'),
        'prodlot_id': fields.many2one('stock.production.lot', 'Lot')
    }
    
    _defaults = {
        #'delivery_date':  lambda self, cr, uid, ctx: self._get_delivery_date(cr,uid,'sale.order.line', ctx),
    }

lot_to_sale_order_line()