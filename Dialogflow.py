import json
import os
from google.cloud import storage
from google.cloud import dialogflow
import logging

PRJ_ID = os.getenv("PRJ_ID")
# TELEGRAM_ID = os.getenv("TELEGRAM_ID")
LANGUAGE_CODE = "ru"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


def explicit():

    storage_client = storage.Client.from_service_account_json(
        "private_key.json"
    )

    buckets = list(storage_client.list_buckets())
    logging.info(buckets)


def detect_intent_texts(session_id, text, project_id=PRJ_ID, language_code=LANGUAGE_CODE):

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    query_text = response.query_result.query_text
    is_fallback = response.query_result.intent.is_fallback
    intent_display_name = response.query_result.intent.display_name
    int_detection_accuracy = response.query_result.intent_detection_confidence
    fulfillment_text = response.query_result.fulfillment_text

    return (
        fulfillment_text,
        intent_display_name,
        int_detection_accuracy,
        is_fallback
    )


def create_intent(
    project_id,
    display_name,
    training_phrases_parts,
    message_texts
):

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)


    # messages = []
    # for msg_text in message_texts:
    #     text = dialogflow.Intent.Message.Text(text=(msg_text,))
    #     message = dialogflow.Intent.Message(text=text)
    #     messages.append(message)

    text = dialogflow.Intent.Message.Text(text=tuple(message_texts))
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    logging.info("Intent created: {}".format(response))


def train_agent(project_id):

    agents_client = dialogflow.AgentsClient()
    parent = dialogflow.AgentsClient.common_project_path(project_id)
    response = agents_client.train_agent(
        request={"parent": parent}
    )

    logging.info(f"Обучение выполнено: {response.done()}")


def main():
    with open("qa_dataset\qa_base.json", "r", encoding='utf-8') as my_file:
        questions = json.load(my_file)

    intent_display_names = list(questions.keys())

    for intent_name in intent_display_names:
        intent_questions = questions[intent_name]["questions"]
        intent_answer = questions[intent_name]["answer"]
        create_intent(
            PRJ_ID,
            intent_name,
            intent_questions,
            intent_answer
        )
        train_agent(PRJ_ID)

if __name__=="__main__":
    main()