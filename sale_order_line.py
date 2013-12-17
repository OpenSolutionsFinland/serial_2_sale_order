from osv import fields, osv
from openerp import netsvc

class lot_to_sale_order_line(osv.osv):
    _name='sale.order.line'
    _inherit='sale.order.line'
    ''''''
    def _sel_func(self, cr, uid, context=None):
        print '_sel_func'
        obj = self.pool.get('stock.production.lot')
        #sol = self.pool.get('sale.order.line').browse(cr, uid, context['active_id'], context)('product_id', '=', sol.product_id)
        ids = obj.search(cr, uid, [])
        res = obj.read(cr, uid, ids, ['name', 'id'], context)
        res = [(r['id'], r['name']) for r in res]
        return res
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0, uom=False, qty_uos=0, uos=False, name='', partner_id=False, lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        print 'product_id_change'
        print 'product ' + str(product)
        
        res = super(lot_to_sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty=qty, uom=uom, qty_uos=qty_uos, uos=uos, name='', partner_id=partner_id, lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag, context=context)
        print res
        return res
    
    _columns = {
        #'dd': fields.function(_get_date, method=True, type='char',store=True, string='Delivery date'),
        'prodlot_id': fields.many2one('stock.production.lot', 'Lot', domain="[('product_id', '=', product_id)]")
    }
    
    _defaults = {
        #'delivery_date':  lambda self, cr, uid, ctx: self._get_delivery_date(cr,uid,'sale.order.line', ctx),
    }

lot_to_sale_order_line()

class sales_order_with_lot(osv.osv):
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
class stock_move_desired_lot(osv.osv):
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
            if move.desired_prodlot_id:
                print 'move ' + str(move.id) + ' has desired lot ' + str(move.desired_prodlot_id.id)
                self.write(cr, uid, [move.id], {'prodlot_id': move.desired_prodlot_id.id})
                # notify move that prodlot has changed
                self.onchange_lot_id(move.prodlot_id,move.product_qty, move.location_id, move.product_id, move.product_uom)
        res = self.check_assign(cr, uid, todo)
        return res

    _columns = {
        'desired_prodlot_id': fields.related('sale_line_id', 'prodlot_id', type="many2one", relation="stock.production.lot", string="Desired lot", store=False)
    }
    
stock_move_desired_lot()