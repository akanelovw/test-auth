from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from auth.authentication import JWTAuthentication
from auth.permissions.decorators import permission_check
from .mock.mock_data import MOCK_REPORTS

class ReportView(APIView):
    authentication_classes = [JWTAuthentication]

    @permission_check("reports", "read")
    def get(self, request):

        if request.user.role == "admin":
            return Response(MOCK_REPORTS)

        user_reports = [
            r for r in MOCK_REPORTS if r["owner_role"] == "user"
        ]
        return Response(user_reports)