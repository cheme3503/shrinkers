from django.contrib.auth.decorators import login_required
from shortener.urls.decorators import admin_only
from django.shortcuts import render
from django.db.models.query import Prefetch
from django.db.models import Subquery, OuterRef
from shortener.models import ShortenedUrls, Statistic

@login_required
@admin_only
def url_list(request):
    urls = (
        ShortenedUrls.objects.order_by('-id')
        .prefetch_related(
            Prefetch('creator'),
            Prefetch('creator__user'),
            Prefetch('creator__organization'),
            Prefetch('creator__organization__pay_plan'),
            Prefetch('statistic_set'),
            # Prefetch('statistic_set', queryset=Statistic.objects.filter(web_browser='Google'), to_attr='edge_usage'),
        )
        .all()
    )

    #예
    # a = urls.first().statistic_set.all()
    # subquery = Statistic.objects.filter(shortened_url_id = OuterRef('pk')).order_by('-id')
    # #subquery는 이 단계에서 실행 되지 않음.
    #
    # urls_ = ShortenedUrls.objects.annotate(late_visit_browser= Subquery(subquery.values('web_brwoser')[:1]))
    #
    # for u in urls_:
    #     print(u.id, u.last_visit_browser)

    return render(request, 'admin_url_list.html', {'urls':urls})


