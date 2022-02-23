from pydantic import BaseModel
from typing import TypeVar, Generic, List, Optional, Dict

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class Pagination():

    def __init__(
            self,
            data: List[SchemaType],
            page_size: int,
            page: int,
            model_name: str):
        self.model_name = model_name
        self.data = data
        self.total = len(self.data)
        self.page_size = page_size
        self.page = page
        self.pagination = self._mk_pagination()
        

    def _mk_pagination(self):
        skip = self.page-1 * self.page_size #0
        limit = skip + self.page_size # 2
        pagination = {}
        previous = f'/{self.model_name}?page_num={self.page-1}&page_size={self.page_size}'
        nextt =  f'/{self.model_name}?page_num={self.page+1}&page_size={self.page_size}'
        if self.page > 1:
            pagination['previous'] = previous
        else:
            pagination['previous'] = None
        
        if limit >= self.total: #we dont have more pages to get!
            pagination['next'] = None
        else: #We have pages to get!
            pagination['next'] = nextt
            
        return pagination

    def mk_dict(self):
        dictt = {
            'data': self.data,
            'total': self.total,
            'page_size': self.page_size,
            'current_page': self.page,
            'pagination': self.pagination
        }
        return dictt






