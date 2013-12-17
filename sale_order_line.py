from osv import fields, osv
from openerp import netsvc

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
    _name='sale.order'
    _inherit='sale.order'
    
    def action_button_confirm(self, cr, uid, ids, context=None):
        # Call superclass handler
        print 'action_button_confirm'
        # check that selected lot has correct product
        sos = self.pool.get('sale.order').browse(cr, uid, ids, context)
        for so in sos:
            for sol in so.order_line:
                if sol.prodlot_id:
                    if not sol.product_id.id == sol.prodlot_id.product_id.id:
                        raise osv.except_osv('Error', 'Production lot and product do not match')
        
        res = super(sales_order_with_lot, self).action_button_confirm(cr, uid, ids, context)
        
        return res
        

sales_order_with_lot()


# adds desired lot_id to stock.move
class stock_move_desired_lot(osv.osv_memory):
    _name='stock.move'
    _inherit='stock.move'
   
    def action_assign(self, cr, uid, ids, *args):
        """ Changes state to confirmed or waiting.
        @return: List of values
        """
       
        todo = []
        for move in self.browse(cr, uid, ids):
            if move.state in ('confirmed', 'waiting'):
                todo.append(move.id)
            if move.desired_lot_id:
                print 'move ' + str(move.id) + ' has desired lot ' + str(move.desired_lot_id)
                self.write(cr, uid, [move.id], {'prodlot_id': move.desired_lot_id})
        res = self.check_assign(cr, uid, todo)
        return res

    _columns = {
        'desired_prodlot_id': fields.related('sale_line_id', 'prodlot_id', type="many2one", relation="stock.production.lot", string="Desired lot", store=False)
    }
    
stock_move_desired_lot()