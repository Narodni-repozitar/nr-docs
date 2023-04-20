import pytest
from invenio_records_resources.services.errors import PermissionDeniedError
from invenio_requests.customizations.event_types import CommentEventType
from invenio_requests.records.api import RequestEvent, RequestEventFormat


def test_custom_type_request(
    app,
    identity_simple,
    identity_simple_2,
    submit_request,
    request_events_service,
    requests_service,
    example_nr_documents,
    users,
    request_record_input_data,
):
    receiver_user = users[1]
    sender_identity = identity_simple
    receiver_identity = identity_simple_2
    request_types = app.extensions["invenio-requests"].request_type_registry
    for request_type in request_types:
        request = submit_request(
            sender_identity,
            data=request_record_input_data,
            topic=example_nr_documents,
            request_type=request_type,
            receiver=receiver_user,
        )
        # assert current_service.read(sender_identity, example_nr_documents["id"])["metadata"][
        #           "status"] == "not approved"
        request_id = request.id

        # approve request by receiver
        payload = {
            "payload": {
                "content": "Ok doc1 is good enough and therefore approved.",
                "format": RequestEventFormat.HTML.value,
            }
        }
        # the sender can't approve the request
        with pytest.raises(PermissionDeniedError):
            requests_service.execute_action(
                sender_identity, request_id, "accept", payload
            )
        # the reciever can
        approve_response = requests_service.execute_action(
            receiver_identity, request_id, "accept", payload
        )
        # assert current_service.read(sender_identity, example_nr_documents["id"])["metadata"][
        #           "status"] == "approved"
        request = approve_response._request
        RequestEvent.index.refresh()

        assert "accepted" == request.status
        events = request_events_service.search(sender_identity, request_id)
        assert 3 == events.total  # two comments and accept log
        hits = list(events.hits)
        assert CommentEventType.type_id == hits[0]["type"]
        assert (
            "Can you approve my document doc1 please?" == hits[0]["payload"]["content"]
        )
        assert (
            "Ok doc1 is good enough and therefore approved."
            == hits[2]["payload"]["content"]
        )
