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
        print 'action_assign'
        """ Changes state of picking to available if all moves are confirmed.
        @return: True
        """
        wf_service = netsvc.LocalService("workflow")
        for pick in self.browse(cr, uid, ids):
            if pick.state == 'draft':
                wf_service.trg_validate(uid, 'stock.picking', pick.id, 'button_confirm', cr)
            move_ids = [x.id for x in pick.move_lines if x.state == 'confirmed']
            if not move_ids:
                raise osv.except_osv(_('Warning!'),_('Not enough stock, unable to reserve the products.'))
            
            # set prodlot for every move that has desired_prodlot_id
            for move in self.pool.get('stock.move').browse(cr, uid, move_ids):
                print 'move ' + str(move.id) + " has desired lot " + str(move.desired_prodlot_id)
                if move.desired_prodlot_id:
                    #def onchange_lot_id(self, cr, uid, ids, prodlot_id=False, product_qty=False,loc_id=False, product_id=False, uom_id=False, context=None):
                    #print 'move ' + str(move.id) + " has desired lot " + str(move.desired_prodlot_id)
                    self.pool.get('stock.move').write(cr, uid, [move.id], {'prodlot_id': move.desired_prodlot_id}, context=context)
                    
            self.pool.get('stock.move').action_assign(cr, uid, move_ids)
        return True
        
    _columns = {
        'desired_prodlot_id': fields.related('sale_line_id', 'prodlot_id', type="many2one", relation="stock.production.lot", string="Desired lot", store=False)
    }

stock_move_desired_lot()