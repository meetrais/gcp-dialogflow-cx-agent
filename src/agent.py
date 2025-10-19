# -*- coding: utf-8 -*-

# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,

# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import uuid
from dotenv import load_dotenv

from google.cloud.dialogflowcx_v3beta1.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3beta1.types import session as session_types

load_dotenv(override=True)


def detect_intent_texts(
    project_id, location_id, agent_id, session_id, texts, language_code="en"
):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_path = f"projects/{project_id}/locations/{location_id}/agents/{agent_id}/sessions/{session_id}"
    
    # Construct the regional endpoint from the location ID
    api_endpoint = f"{location_id}-dialogflow.googleapis.com"
    client_options = {"api_endpoint": api_endpoint}
    session_client = SessionsClient(client_options=client_options)

    text_input = session_types.TextInput(text=texts[0])
    query_input = session_types.QueryInput(text=text_input, language_code=language_code)
    request = session_types.DetectIntentRequest(
        session=session_path, query_input=query_input
    )
    response = session_client.detect_intent(request=request)

    return response.query_result


def main():
    """The main entry point for the application."""
    project_id = os.environ.get("PROJECT_ID")
    location_id = os.environ.get("LOCATION_ID")
    agent_id = os.environ.get("AGENT_ID")

    session_id = str(uuid.uuid4())
    texts = ["Hello"]

    if "your-gcp-project-id" in project_id or "your-agent-location" in location_id or "your-agent-id" in agent_id:
        print("Please set the PROJECT_ID, LOCATION_ID, and AGENT_ID in the .env file.")
        return

    response = detect_intent_texts(project_id, location_id, agent_id, session_id, texts)
    print("Response from Dialogflow CX:")
    print(response)


if __name__ == "__main__":
    main()
