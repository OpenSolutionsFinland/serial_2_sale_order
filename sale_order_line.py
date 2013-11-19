from osv import fields, osv
#from datetime import datetime as dt
#from datetime import date
#from datetime import timedelta

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

class sales_order_with_lot(osv.osv_memory):
    _name='sale.order.line'
    _inherit='sale.order.line'
    
    def action_button_confirm(self, cr, uid, ids, context=None):
        # Call superclass handler
        print 'action_button_confirm'
        # check that selected lot has correct product
        so = self.pool.get('sale.order').browse(cr, uid, ids, context)
        for sol in so.order_line:
            if sol.prodlot_id:
                if not sol.product_id.id == osl.prodlot_id.product_id.id:
                    raise osv.except_osv('Error', 'Production lot and product do not match')
        
        res = super(sales_order_with_lot, self).action_button_confirm(cr, uid, ids, context)
        
        return res
        

sales_order_with_lot()
        