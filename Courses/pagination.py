from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    page_size = 10                        # return 10 items by default
    page_size_query_param = 'page_size'   # client can request ?page_size=25
    max_page_size = 100                   # but never more than 100 at once

    def get_paginated_response(self, data):
        return Response({
            "success": True,
            "pagination": {
                "total": self.page.paginator.count,
                "page_size": self.page_size,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            },
            "results": data
        })
