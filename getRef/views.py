from django.shortcuts import render
from django.views import View
import datetime
from rest_framework.viewsets import ViewSet

from .WorkWithBudgetAPI.services import GetAllObjects
from .forms import ReferenceForm


class RefFormView(View):
# class RefFormView(ViewSet):
    ref_form = ReferenceForm()

    def get(self, request):
        content = {'form':self.ref_form}
        return render(request, 'getRef/refForm.html', content)

    def post(self, request):
        get_objects = GetAllObjects()
        ref, budget, curent_serializer = get_objects.devide_model_and_serializer(request.POST['reference'])
        page_count = get_objects.get_page_count(ref)
        print(datetime.datetime.now())
        for i in range(1, page_count):
            data = get_objects.get_single_page(ref=ref, page_num=i)
            get_objects.write_data_to_database(data=data, budget=budget, serializer_from_ref=curent_serializer)
        print(datetime.datetime.now())
        return render(request, 'getRef/res.html')

