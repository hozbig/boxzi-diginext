import requests
import uuid

from django.shortcuts import redirect
from account.models import User
from lowercase_booleans import true, false

from .models import PersonalTest

def generate_uuid4():
    return str(uuid.uuid4())

COSTUMER_ID = "611b67a1d95ab95f5c735f8d"
CAMPAIGN_ID = "6678271fa09ce71ba13d8cb3"
ANDAZE_TOKEN = None

def update_validate_token():
    global ANDAZE_TOKEN
    url = "https://api.andaze.io/graphql"  # Replace with your GraphQL endpoint
    headers = {
        "Content-Type": "application/json"
    }
    query = """
    mutation partnerLogin($phone: String!, $password: String!) {
        partnerLogin(data: { phone: $phone, password: $password }) {
            bearerToken
        }
    }
    """
    variables = {
        "phone": "09120244206",
        "password": "Dg@123"
    }
    payload = {
        "query": query,
        "variables": variables
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        json_response = response.json()
        if "data" in json_response and "partnerLogin" in json_response["data"]:
            ANDAZE_TOKEN = json_response["data"]["partnerLogin"]["bearerToken"]
        else:
            raise Exception("Invalid response structure")
    else:
        raise Exception(f"Query failed with status code {response.status_code}")


def send_user_information(user_obj:User, road):
    if user_obj.user_of_personal_test.exists():
        return redirect("router")

    try:
        user_first_name = user_obj.first_name
        user_last_name = user_obj.last_name
        user_phone_number = user_obj.phone_number
        reference_uuid4 = generate_uuid4()
        
        url = "https://api.andaze.io/graphql"  # Replace with your GraphQL endpoint
        headers = {
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {ANDAZE_TOKEN}"
        }
        query = """
        mutation addParticipantsForPartner(
            $customerId: String!
            $campaignId: String!
            $reference: String!
            $participant: CreateParticipantInput!
            $assessments: [String!]
        ) {
            addParticipantsForPartner(
                customerId: $customerId
                campaignId: $campaignId
                reference: $reference
                participant: $participant
                assessments: $assessments
            ) {
                campagin {
                    id
                }
            }
        }
        """
        
        variables = {
            "customerId": COSTUMER_ID,
            "campaignId": CAMPAIGN_ID,
            "reference": reference_uuid4,
            "participant": {
                "firstName": user_first_name,
                "lastName": user_last_name,
                "phone": user_phone_number,
                "completeProfile": false
            },
            "assessments": ["ead23a32ba4eb97851b7d7079d79c00c"]
        }

        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)

        if response.status_code == 401:
            update_validate_token()
            send_user_information(user_obj, road)
        if response.status_code == 400:
            send_user_information(user_obj, road)
        
        if response.status_code == 200:
            json_response = response.json()
            accepted = True
            
            if "data" in json_response and json_response["data"] == "null":
                # Make "first_response_of_sending_information_is_accepted" False if the user was already in Andaze campaign
                accepted = False
            
            object = PersonalTest(
                user = user_obj,
                road = road,
                reference_id = reference_uuid4,
                first_response_of_sending_information_is_accepted = accepted,
            )
            object.save()
            
        else:
            pass
            # raise Exception(f"Query failed with status code {response.status_code}")
    except:
        pass


def get_user_data(user_obj:User):
    personal_test_object = PersonalTest.objects.filter(user=user_obj, first_response_of_sending_information_is_accepted=True).last()

    if not personal_test_object.final_user_result_url == None:
        return personal_test_object.final_user_result_url

    try:
        url = "https://api.andaze.io/graphql"  # Replace with your GraphQL endpoint
        headers = {
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {ANDAZE_TOKEN}"
        }
        query = """
        query evaluationsForPartner(
            $limit: Float!
            $skip: Float!
            $campaign: String!
            $type: EvaluationTypeEnum!
            $reference: String!
        ) {
            evaluationsForPartner(
            limit: $limit
            skip: $skip
            campaign: $campaign
            type: $type
            reference: $reference
        ) {
        id
        assessment
        type
        assessmentObj {
        id
        name
        title
        summary
        questionsCount
        }
        company {
        id
        name
        }
        party {
        id
        firstName
        lastName
        phone
        }
        }
        }
        """
        
        variables = {
            "limit": 100,
            "skip": 0,
            "type": "DONE",
            # "type": "DONE",
            "campaign": "6678271fa09ce71ba13d8cb3",
            "reference": personal_test_object.reference_id
        }

        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)


        if response.status_code == 401:
            update_validate_token()
            get_user_data(user_obj)
        if response.status_code == 400:
            get_user_data(user_obj)
        
        if response.status_code == 200:
            json_response = response.json()
            
            evaluationId = json_response["data"]["evaluationsForPartner"][0]["id"]
            url_result = f"http://azmoon.andaze.io/exames/result/forPartner?exameId={evaluationId}&exameType=neopir"
            return url_result
    except:
        pass
