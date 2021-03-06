from pydantic import BaseModel, create_model
from typing import TypeVar, Generic, List, Optional, Dict

SchemaType = TypeVar("SchemaType", bound=BaseModel)


#TODO
# def pagination( 
#         data: List[SchemaType],
#         page_size: int,
#         page: int,
#         path_name: str,
#         total_count: int
# )-> dict:
#     skip = (page-1) * page_size 
#     limit = skip + page_size # the limit id that i will collect
#     pagination = {
#         'data': data,
#         'total': total_count,
#         'page_size': page_size,
#         'current_page': page,
#         'first_pagge': 1,
#         'last_page': 0
#     }
#     def make_pagination(limit:int,  ):
#         pass

#     def get_next(limit:int, total_count:int, path_name:str, page:int):
#         nextt =  f'{path_name}?page_num={page+1}&page_size={page_size}'
#         if limit >= total_count: #we dont have more pages to get!
#             pagination['next_page'] = None
#         else: #We have pages to get!
#             pagination['next_page'] = nextt

#     def get_previous(path_name:str, page:int):
#         previous = f'{path_name}?page_num={page-1}&page_size={page_size}'
#         if page > 1:
#             pagination['previous_page'] = previous
#         else:
#             pagination['previous_page'] = None


#     return make_pagination()

class Pagination():

    def __init__(
            self,
            data: List[SchemaType],
            page_size: int,
            page: int,
            path_name: str,
            total_count: int):
        self.path_name = path_name
        self.data = data
        self.total_count = total_count
        self.page_size = page_size
        self.page = page
        self.pagination = self._mk_pagination()
        

    def _mk_pagination(self) -> dict:
        skip = (self.page-1) * self.page_size 
        limit = skip + self.page_size # the limit id that i will collect
        pagination = {}
        previous = f'{self.path_name}?page_num={self.page-1}&page_size={self.page_size}'
        nextt =  f'{self.path_name}?page_num={self.page+1}&page_size={self.page_size}'
        if self.page > 1:
            pagination['previous'] = previous
        else:
            pagination['previous'] = None
        
        if limit >= self.total_count: #we dont have more pages to get!
            pagination['next'] = None
        else: #We have pages to get!
            pagination['next'] = nextt
            
        return pagination


    def mk_dict(self) ->dict:
        dictt = {
            'data': self.data,
            'total': self.total_count,
            'page_size': self.page_size,
            'current_page': self.page,
            'pagination': self.pagination
        }
        return dictt

'''
This class must be inherit from a more specific schema page,
for example User inherith this to make UserPageOut.
'''
class PageResponse(BaseModel):
    #data: List[SchemaType] # Must be substituted for a more specific schemaType, like UserOut
    total: int
    page_size: int
    current_page: int
    pagination: Dict[str,Optional[str]]

'''
Useful for path operation response_model=page_response(model_out=specific_schema)
Used with validation
'''
def page_response(model_out: SchemaType, name: str):
    
    page_model = create_model(
        name, 
        total=(int, ...),
        page_size=(int, ...),
        current_page=(int, ...),
        pagination=(Dict[str,Optional[str]], ...),
        data= (List[model_out],...),
        __base__=BaseModel
    )
    return page_model