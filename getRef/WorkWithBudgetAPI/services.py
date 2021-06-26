import requests
from django.db import IntegrityError

from .serializers import BudgetGovSerializer, GlavBudgetSerializer
from getRef.models import Budget, GlavBudgetClass


class GetAllObjects():

    def get_page_count(self, reference:str, page_size:int=1000, required_status:str='ACTIVE'):
        '''Get count of pages by page_size and STATUS'''

        page = requests.get(f'{reference.split("?")[0]}?pageSize={page_size}&filterstatus={required_status}')
        return page.json().get('pageCount')+1


    def devide_model_and_serializer(self, reference:str, default_budget_model:object=Budget,
                                    other_model:object=GlavBudgetClass):
        '''Devide our model. If main_ref is like below, then choose default model,
         owervise other_model'''

        main_ref = 'http://budget.gov.ru/epbs/registry/7710568760-BUDGETS/data'
        ref = reference.split('?')[0]
        if ref == main_ref:
            serializer = BudgetGovSerializer
            budget = default_budget_model
        else:
            serializer = GlavBudgetSerializer
            budget = other_model
        return ref, budget, serializer


    def get_single_page(self, ref:str, page_num:int=1, page_size:int=1000, required_status:str='ACTIVE'):
        '''Get data from page with page_num'''
        single_page = requests.get(
                f'{ref}?pageSize={page_size}&filterstatus={required_status}&pageNum={page_num}').json().get('data')
        print('page_number - ', page_num)
        return single_page

    def write_data_to_database(self, data:dict, budget:object, serializer_from_ref:object):
        '''Write or owerwrite all data in database
        , choose model(budget) and serializer '''
        for obj_data in data:
            unique_field = obj_data.get('code')
            obj = budget.objects.filter(code=unique_field).first()
            serializer = serializer_from_ref(instance=obj, data=obj_data)
            serializer.is_valid()
            serializer.save()
