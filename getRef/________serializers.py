from rest_framework import serializers
from .models import Budget, GlavBudgetClass


class BudgetGovSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'

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