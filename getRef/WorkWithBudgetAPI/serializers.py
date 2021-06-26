from rest_framework import serializers
from getRef.models import Budget, GlavBudgetClass

class BudgetListSerializer(serializers.ListSerializer):

    def save(self):
        # Maps for id->instance and id->data item.
        instance = Budget.objects.all()
        budget_mapping = {budget.code: budget for budget in instance}
        data_mapping = {item['code']: item for item in self.validated_data}

        # Perform creations and updates.
        ret = []
        for budget_code, data in data_mapping.items():
            budget = budget_mapping.get(budget_code, None)
            if budget is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(budget, data))

        # Perform deletions.
        for budget_code, budget in budget_mapping.items():
            if budget_code not in data_mapping:
                budget.delete()

        return ret


class BudgetGovSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'
        # extra_kwargs = {'code': {'validators': []}}
        # list_serializer_class = BudgetListSerializer

    def to_internal_value(self, data):
        if data['enddate'] == '':
            data['enddate'] = None
        if data['parentcode'] == '':
            pass
        elif not int(data['parentcode']):
            data['parentcode'] = ''
        if not Budget.objects.filter(code=data['parentcode']).exists():
            data['parentcode'] = ''
        return super().to_internal_value(data)


class GlavBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlavBudgetClass
        fields = '__all__'

    def to_internal_value(self, data):
        if data['enddate'] == '':
            data['enddate'] = None
        # не понимаю почему, но без capitalize() не работает
        budgetname = Budget.objects.filter(name__iexact=data['budgetname'].capitalize()).first()
        data['budgetname'] = budgetname.code
        return super().to_internal_value(data)