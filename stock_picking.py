from osv import fields, osv

class stock_picking_serial_from_so(osv.osv):
    _name="stock.picking"
    _inherit="stock.picking"
    
    def do_partial(self, cr, uid, ids, partial_datas, context=None):
        print 'stock picking'
        print str(partial_datas)
        res = super(stock_picking_serial_from_so, self).do_partial(cr, uid, ids, partial_datas, context=context)
        return res

    _columns = {
        
    }

stock_picking_serial_from_so()
