from django.http import JsonResponse
from events.api_views import ConferenceListEncoder
from .models import Presentation
from events.models import Conference
from common.json import ModelEncoder
from django.views.decorators.http import require_http_methods
import json


class PresentationListEncoder(ModelEncoder):
    model = Presentation
    properties = ["title"]

    def get_extra_data(self, o):
        return {"status": o.status.name}


class PresentationDetailEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
        "synopsis",
        "created",
        "conference",
    ]

    encoders = {
        "conference": ConferenceListEncoder(),
    }


@require_http_methods(["GET", "POST"])
def api_list_presentations(request, conference_id):
    """
    Lists the presentation titles and the link to the
    presentation for the specified conference id.

    Returns a dictionary with a single key "presentations"
    which is a list of presentation titles and URLS. Each
    entry in the list is a dictionary that contains the
    title of the presentation, the name of its status, and
    the link to the presentation's information.

    {
        "presentations": [
            {
                "title": presentation's title,
                "status": presentation's status name
                "href": URL to the presentation,
            },
            ...
        ]
    }
    """
    if request.method == "GET":
        presentations = Presentation.objects.filter(conference=conference_id)
        # for p in Presentation.objects.filter(conference=conference_id)
        return JsonResponse(
            {"presentations": presentations},
            encoder=PresentationListEncoder,
        )
    else:  # "POST"
        content = json.loads(request.body)
        try:
            # get the Conference object and put it in the content dict
            conference = Conference.objects.get(id=conference_id)
            content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )
        presentation = Presentation.create(**content)
        return JsonResponse(
            presentation, encoder=PresentationDetailEncoder, safe=False
        )


# @require_http_methods(["DELETE", "GET", "PUT"])
def api_show_presentation(request, pk):

    """
    Returns the details for the Presentation model specified
    by the pk parameter.

    This should return a dictionary with the presenter's name,
    their company name, the presenter's email, the title of
    the presentation, the synopsis of the presentation, when
    the presentation record was created, its status name, and
    a dictionary that has the conference name and its URL

    {
        "presenter_name": the name of the presenter,
        "company_name": the name of the presenter's company,
        "presenter_email": the email address of the presenter,
        "title": the title of the presentation,
        "synopsis": the synopsis for the presentation,
        "created": the date/time when the record was created,
        "status": the name of the status for the presentation,
        "conference": {
            "name": the name of the conference,
            "href": the URL to the conference,
        }
    }
    """
    # if request.method == "GET":
    presentation = Presentation.objects.get(id=pk)
    return JsonResponse(
        presentation,
        encoder=PresentationDetailEncoder,
        safe=False,
    )


#    # elif request.method == "DELETE":
#         count, _ = Presentation.objects.get(id=pk)
#         return JsonResponse({"deleted": count > 0})
#     else:  # "PUT" update
#         content = json.loads(request.body)
#         print("content", content)
#         try:
#             print("tryblock")
#             # # Get the Conference object and put it in the content dict
#             presentation = Presentation.objects.get(id=pk)
#             # presentation = conference.presentations
#             # print("test", conference)
#             return JsonResponse(
#                 presentation, encoder=PresentationDetailEncoder, safe=False
#             )
#             # content["conference"] = conference
#         except Conference.DoesNotExist:
#             return JsonResponse(
#                 {"message": "Invalid conference id"},
#                 status=400,
#             )
