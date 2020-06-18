import django_filters
from django_filters import DateFilter, CharFilter
from .models import *

class UpdateFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_posted", lookup_expr="gte")
    end_date = DateFilter(field_name="date_posted", lookup_expr="lte")
    title = CharFilter(field_name="title", lookup_expr="icontains")
    content = CharFilter(field_name="content", lookup_expr="icontains")
    # first_name = CharFilter(field_name="student__first_name", lookup_expr="icontains")
    class Meta:
        model = Update
        fields = ['title', 'content','student']
        exclude=['date_posted']
