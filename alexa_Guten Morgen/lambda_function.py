

from __future__ import print_function
import requests
import json

host = "YourPublicIP"
password = 'Password' 

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Guten Morgen! Soll ich Kaffee kochen?"
    url = host + "/api/services/light/turn_on"
    headers = {'Content-Type': 'application/json', 'x-ha-access': password}
    payload = {'entity_id': 'light.aufstehen'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    
    reprompt_text = ""
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def create_tasn_attributes(tasn):
    return {"Tassen": tasn}


def Ja_Bitte_session(intent, session):
    card_title = ''
    session_attributes = {}
    

    if 'Tassen' in intent['slots'] and 'value' in intent['slots']['Tassen']:
        tasn = intent['slots']['Tassen']['value']
        session_attributes = create_tasn_attributes(tasn)
   #     print(session_attributes)
        speech_output = "OK, Ich koche " + tasn + " Tassen Kaffe!"
        reprompt_text = "OK?"
        should_end_session = True
        
        print(tasn)
        
        if tasn == "1":
            payload = {'entity_id': 'switch.kaffe'}
            do = 1
        elif tasn == "2":
            payload = {'entity_id': 'switch.kaffe2'}
            do = 1
        elif tasn == "3":
            payload = {'entity_id': 'switch.kaffe3'}
            do = 1
        elif tasn == "4":
            payload = {'entity_id': 'switch.kaffe4'}
            do = 1
        elif tasn == "5":
            payload = {'entity_id': 'switch.kaffe5'}
            do = 1
        elif tasn == "6":
            payload = {'entity_id': 'switch.kaffe5'}
            do = 1
        else:
             speech_output = "Fehler 101"
             do = 0
             payload = {}
             
        if do == 1:
            url = host + "/api/services/switch/turn_on"
            headers = {'Content-Type': 'application/json', 'x-ha-access': password }
        #    payload = {'entity_id': 'switch.kaffe'}
            data = json.dumps(payload)
            r = requests.post(url, data=data, headers=headers)
        else:
            print("Fehler 101")
    else:
        should_end_session = False
        speech_output = "Wie viele Tassen soll ich machen?"
        reprompt_text = "Wie viele Tassen soll ich machen?"
        
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "Ja_Bitte":
        return Ja_Bitte_session(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
