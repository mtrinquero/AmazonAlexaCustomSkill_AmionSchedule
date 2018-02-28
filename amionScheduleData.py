# Mark Trinquero
# Amion Schedule - Get Data
# Note: written in pyton 3

# http://www.amion.com/cgi-bin/ocs?Lo=nwem&Rpt=619

# "http://www.amion.com/cgi-bin/ocs?Lo=#{password}&Rpt=619&Month=#{month}&Year=#{year}")
# {password}
# {month}
# {year}


import csv
import urllib.request
import codecs



API_BASE = "http://www.amion.com/cgi-bin/ocs?Lo=nwem&Rpt=619"


def skip_first(seq, n):
    for i,item in enumerate(seq):
        if i >= n:
            yield item


def lambda_handler(event, context):
    #if (event["session"]["application"]["applicationId"] != "amzn1.ask.skill.f60407b7-975e-4995-a88c-29d31894d039"):
    #    raise ValueError("Invalid Application ID")
    
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

def on_session_started(session_started_request, session):
    print ("Starting new session.")

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "getScheduleData":
        return get_schedule_data(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print ("Ending session.")


def handle_session_end_request():
    card_title = "Amion - Thanks"
    speech_output = "Thank you for using the Amion Schedule skill.  See you next time!"
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def get_welcome_response():
    session_attributes = {}
    card_title = "Amion"
    speech_output = "Welcome to the Alexa Amion Schedule skill. " \
                    "You can ask me if someone is scheduled to work today"
    reprompt_text = "Please ask me if someone is scheduled to work today, " \
                    "for example Paul Trinquero."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_schedule_data(intent):
    session_attributes = {}
    card_title = "Todays Amion Schedule"
    speech_output = "I'm not sure which person you wanted schedule data for. " \
                    "Please try again."
    reprompt_text = "I'm not sure which person you wanted schedule data for. " \
                    "Try asking about Paul Trinquero or Katie Trinquero for example."
    should_end_session = False

    ftpstream = urllib.request.urlopen(API_BASE)
    csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))

    if "employee" in intent["slots"]:
        #employee_name = intent["slots"]["employee"]["value"]
        employee_name = intent["slots"]["employee"][0]

    for line in skip_first(csvfile, 6):
        if line[0] == employee_name:
            speech_output = "schedule for " + employee_name + " is as follows: " + line[3]
        else:
            speech_output = "Employee: " + employee_name + " is not working today"
    reprompt_text = ""

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))





def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }




