
import copy

from ..esiapi import Universe

class Item:
    def __init__(self,source,make_valid=True):
        """Base Item class and interaction point
        """
        if type(source) == str:
            self.name = source

        elif type(source) == int:
            self.type_id = source

        elif type(soruce) == Item:
            self.name = soruce.name
            self.type_id = soruce.type_id
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
            pass
            



    def __str__(self):
        return f"Item<{self.name}>"
