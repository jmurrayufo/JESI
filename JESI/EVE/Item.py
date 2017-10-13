
import copy

from ..esiapi.Universe import Universe
from ..esiapi.Search import Search

class Item:
    def __init__(self,source,make_valid=True,cache=True):
        """Base Item class and interaction point.

        Keywork Arguemnts:
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

        elif type(soruce) == Item:
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
        
        # If we are not a copy, try to create
        if make_valid:
            # TODO: We need to search SQL *first*!
            if self.type_id == None:
                # We need to find out our ID first!
                data = Search().search(self.name, ["inventorytype"], strict=True)
                if len(data['inventorytype']) != 1:
                    raise ValueError(f"Couldn't find {self.name} in search uniquely!")
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
