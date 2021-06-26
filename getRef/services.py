import requests
from .________serializers import BudgetGovSerializer, GlavBudgetSerializer
from .models import Budget, GlavBudgetClass


class GetAllObjects():

    def get_data_from_reference(self, reference:str, page_size=1000, required_status='ACTIVE'):
        main_ref = 'http://budget.gov.ru/epbs/registry/7710568760-BUDGETS/data'
        ref = reference.split('?')[0]
        if ref == main_ref:
            serializer = BudgetGovSerializer
            budget = Budget
        else:
            serializer = GlavBudgetSerializer
            budget = GlavBudgetClass
        page = requests.get(f'{ref}?pageSize={page_size}&filterstatus={required_status}')
        data = []
        for i in range(1, page.json().get('pageCount')+1):
            page_num = requests.get(
                f'{ref}?pageSize={page_size}&filterstatus={required_status}&pageNum={i}').json().get('data')
            data += page_num
        return data, budget, serializer

    def write_data_to_database(self, data, budget, serializer_from_ref):
        for obj_data in data:
            code_field = obj_data.get('code')
            obj = budget.objects.filter(code=code_field).first()
            serializer = serializer_from_ref(instance=obj, data=obj_data)
            serializer.is_valid()
            serializer.save()
        return serializer