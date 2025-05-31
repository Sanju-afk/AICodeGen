import os
from edenai.workflow import workflow_client


def main():
    client = workflow_client(
        api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZjQ5NjMyNzgtOWFkYS00MjliLWE0NjYtOThmNzJiZjNkYzExIiwidHlwZSI6ImFwaV90b2tlbiJ9.VNcGRZKuOnyQdEgcQgsELR_MMzJ4E-pRQ0GEabiAE6U",
        base_url="http://localhost/v2",
    )

    # response = workflow.create_or_update(data=())
    data = {
        "nodes": [
            {
                "type": "input",
                "name": "Input_Node",
                "data": [
                    {"type": "string", "label": "text", "defaultValue": "Hello, world"}
                ],
            },
            {
                "type": "if",
                "name": "some_if",
                "data": [
                    {
                        "name": "conditions",
                        "value": [
                            {
                                "type": "string",
                                "left": "{{Input_Node.text}}",
                                "operator": "equals",
                                "right": "Hello, world",
                            },
                            "or",
                            {
                                "type": "number",
                                "left": 10,
                                "operator": "gt",
                                "right": 5,
                            },
                        ],
                    },
                    {
                        "name": "true",
                        "value": [
                            {
                                "type": "audio/text_to_speech_async",
                                "name": "some_text_to_speech",
                                "data": [
                                    {"name": "provider", "value": "amazon"},
                                    {
                                        "name": "text",
                                        "value": "explain me: {{Input_Node.text}}",
                                    },
                                    {"name": "language", "value": "en"},
                                    {"name": "option", "value": "MALE"},
                                    {"name": "rate", "value": 10},
                                ],
                            },
                        ],
                    },
                    {"name": "false", "value": []},
                ],
            },
            {
                "type": "output",
                "name": "Output_Node",
                "data": [
                    {
                        "name": "text",
                        "value": "{{some_text_to_speech.audio_resource_url || Input_Node.text }}",
                    },
                ],
            },
        ]
    }

    # data = {
    #     "nodes": [
    #         {
    #             "type": "input",
    #             "name": "Input_Node",
    #             "data": [
    #                 {"type": "string", "label": "text", "defaultValue": "Hello, world"}
    #             ],
    #         },
    #         {
    #             "type": "if",
    #             "name": "some_if",
    #             "data": [
    #                 {
    #                     "name": "conditions",
    #                     "value": [
    #                         {
    #                             "type": "string",
    #                             "left": "{{Input_Node.text}}",
    #                             "operator": "equals",
    #                             "right": "Hello, world",
    #                         },
    #                         "or",
    #                         {
    #                             "type": "number",
    #                             "left": 10,
    #                             "operator": "gt",
    #                             "right": 5,
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "name": "true",
    #                     "value": [
    #                         {
    #                             "type": "audio/text_to_speech_async",
    #                             "name": "some_text_to_speech",
    #                             "data": [
    #                                 {"name": "provider", "value": "amazon"},
    #                                 {
    #                                     "name": "text",
    #                                     "value": "explain me: {{Input_Node.text }}",
    #                                 },
    #                                 {"name": "language", "value": "en"},
    #                                 {"name": "option", "value": "MALE"},
    #                                 {"name": "rate", "value": 10},
    #                             ],
    #                         },
    #                         {
    #                             "type": "audio/speech_to_text_async",
    #                             "name": "some_speech_to_text",
    #                             "data": [
    #                                 {"name": "provider", "value": "openai"},
    #                                 {
    #                                     "name": "file_url",
    #                                     "value": "{{some_text_to_speech.audio_resource_url}}",
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {"name": "false", "value": []},
    #             ],
    #         },
    #         {
    #             "type": "output",
    #             "name": "Output_Node",
    #             "data": [
    #                 {
    #                     "name": "url",
    #                     "value": "{{some_text_to_speech.audio_resource_url}}",
    #                 },
    #                 {
    #                     "name": "text",
    #                     "value": "{{some_speech_to_text.text}}",
    #                 },
    #             ],
    #         },
    #     ]
    # }
    response = client.create_or_update(name="code_testttt", data=data)
    execution = client.execute(
        name="code_testttt", data={"text": "story about lyon, france"}
    )
    print(execution["output"])


if __name__ == "__main__":
    main()
