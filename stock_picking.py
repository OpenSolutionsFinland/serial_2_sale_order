from osv import fields, osv

class stock_picking_serial_from_so(osv.osv):
    _name="stock.picking"
    _inherit="stock.picking"
    
    '''
    def do_partial(self, cr, uid, ids, partial_datas, context=None):
        print 'stock picking'
        print str(partial_datas)
        res = super(stock_picking_serial_from_so, self).do_partial(cr, uid, ids, partial_datas, context=context)
        return res
    '''
    
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
        
    }

stock_picking_serial_from_so()
