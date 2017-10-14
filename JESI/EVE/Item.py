
import copy
import logging

from ..esiapi.Universe import Universe
from ..esiapi.Search import Search
from ..SQL.SQL import SQL

class Item:
    log = logging.getLogger("JESI").getChild(__module__)
    db = SQL()

    def __init__(self,source,make_valid=True,cache=True):
        """Base Item class and interaction point.

        Keyword Arguments:
        source -- Depending on type, will generate the item dynamicaly.
            str: Assumed to be the name of the object.
            int: Assumed to be the type_id of the object.
            Item: Assumed to be Item to copy from.
            Other: Errors out.
        make_valid -- Determine if we should attempt to parse from eve's api
            to complete the Item.
        cache -- Enable caching (read/write to SQL)
        """
        if type(source) == str:
            self.name = source
            self.type_id = None

        elif type(source) == int:
            self.name = None
            self.type_id = source

        elif type(source) == Item:
            self.capacity = source.capacity  #(number, optional): capacity number ,
            self.description = source.description  #(string): description string ,
            self.dogma_attributes = copy.deepcopy(source.dogma_attributes)  #(Array[get_universe_types_type_id_dogma_attribute], optional): dogma_attributes array ,
            self.dogma_effects = copy.deepcopy(source.dogma_effects)  #(Array[get_universe_types_type_id_dogma_effect], optional): dogma_effects array ,
            self.graphic_id = source.graphic_id  #(integer, optional): graphic_id integer ,
            self.group_id = source.group_id  #(integer): group_id integer ,
            self.icon_id = source.icon_id  #(integer, optional): icon_id integer ,
            self.market_group_id = source.market_group_id  #(integer, optional): This only exists for types that can be put on the market ,
            self.mass = source.mass  #(number, optional): mass number ,
            self.name = source.name  #(string): name string ,
            self.packaged_volume = source.packaged_volume  #(number, optional): packaged_volume number ,
            self.portion_size = source.portion_size  #(integer, optional): portion_size integer ,
            self.published = source.published  #(boolean): published boolean ,
            self.radius = source.radius  #(number, optional): radius number ,
            self.type_id = source.type_id  #(integer): type_id integer ,
            self.volume = source.volume  #(number, optional): volume number
        
        elif type(source) == dict:
            self.capacity = source.get('capacity',0)
            self.description = source.get('description','')
            self.dogma_attributes = source.get('dogma_attributes',[])
            self.dogma_effects = source.get('dogma_effects',[])
            self.graphic_id = source.get('graphic_id','')
            self.group_id = source.get('group_id',None)
            self.icon_id = source.get('icon_id',None)
            self.market_group_id = source.get('market_group_id',None)
            self.mass = source.get('mass')
            self.name = source.get('name')
            self.packaged_volume = source.get('packaged_volume',0)
            self.portion_size = source.get('portion_size',0)
            self.published = source.get('published',False)
            self.radius = source.get('radius',0)
            self.type_id = source.get('type_id')
            self.volume = source.get('volume',0)

        # If we are not a copy, try to create
        if make_valid:
            try:
                data = self.db.get_item(self)
            except ValueError:
                if self.type_id == None:
                    # We need to find out our ID first!
                    data = Search().search(self.name, ["inventorytype"], strict=True)
                    if len(data) != 1:
                        raise ValueError(f"Couldn't find '{self.name}' in search uniquely!")
                    self.type_id = data['inventorytype'][0]
                data = Universe().types(self.type_id)
            
            self.capacity = data.get('capacity',0)
            self.description = data.get('description','')
            self.dogma_attributes = data.get('dogma_attributes',[])
            self.dogma_effects = data.get('dogma_effects',[])
            self.graphic_id = data.get('graphic_id','')
            self.group_id = data.get('group_id',None)
            self.icon_id = data.get('icon_id',None)
            self.market_group_id = data.get('market_group_id',None)
            self.mass = data.get('mass')
            self.name = data.get('name')
            self.packaged_volume = data.get('packaged_volume',0)
            self.portion_size = data.get('portion_size',0)
            self.published = data.get('published',False)
            self.radius = data.get('radius',0)
            self.type_id = data.get('type_id')
            self.volume = data.get('volume',0)


    def __str__(self):
        return f"Item<{self.name}>"


    def dict(self):
        """Return a dict that could create this Item
        """
        ret_val = dict()
        ret_val['capacity'] = getattr(self,'capacity',None)
        ret_val['description'] = getattr(self,'description',None)
        ret_val['dogma_attributes'] = getattr(self,'dogma_attributes',None)
        ret_val['dogma_effects'] = getattr(self,'dogma_effects',None)
        ret_val['graphic_id'] = getattr(self,'graphic_id',None)
        ret_val['group_id'] = getattr(self,'group_id',None)
        ret_val['icon_id'] = getattr(self,'icon_id',None)
        ret_val['market_group_id'] = getattr(self,'market_group_id',None)
        ret_val['mass'] = getattr(self,'mass',None)
        ret_val['name'] = getattr(self,'name')
        ret_val['packaged_volume'] = getattr(self,'packaged_volume',None)
        ret_val['portion_size'] = getattr(self,'portion_size',None)
        ret_val['published'] = getattr(self,'published',None)
        ret_val['radius'] = getattr(self,'radius',None)
        ret_val['type_id'] = getattr(self,'type_id')
        ret_val['volume'] = getattr(self,'volume',None)
        return ret_val