


from ..sdk.workflow import workflow_client


client = workflow_client(
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZjQ5NjMyNzgtOWFkYS00MjliLWE0NjYtOThmNzJiZjNkYzExIiwidHlwZSI6ImFwaV90b2tlbiJ9.VNcGRZKuOnyQdEgcQgsELR_MMzJ4E-pRQ0GEabiAE6U"
)

# response = workflow.create_or_update(data=())
data = {
    "nodes": [
        {
            "type": "input",
            "name": "Input_Node",
            "data": [
                {"type": "string", "label": "text", "defaultValue": "Hello, world!"}
            ],
        },
        {
            "type": "text/chat",
            "name": "some_chat",
            "data": [
                {"name": "provider", "value": "openai/gpt-4o"},
                {"name": "text", "value": "explain me: {{Input_Node.text}}"},
            ],
        },
        {
            "type": "translation/automatic_translation",
            "name": "Translation",
            "data": [
                {"name": "provider", "value": "google"},
                {"name": "text", "value": "{{some_chat.generated_text}}"},
                {"name": "source_language", "value": "en"},
                {"name": "target_language", "value": "nl"},
            ],
        },
        {
            "type": "text/keyword_extraction",
            "name": "Keywords",
            "data": [
                {"name": "provider", "value": "openai"},
                {"name": "text", "value": "{{Translation.text}}"},
            ],
        },
        {
            "type": "code",
            "name": "some_code",
            "data": [
                {
                    "name": "code",
                    "value": "const valueFromInput = {{ Input_Node.text }};\n  const valueFromNode = {{ some_chat.generated_text }};  \nfunction greet(msg) {\n  return `welcome ${msg}!`;\n};\n\nreturn {\n input: greet(valueFromInput),\n node: greet(valueFromNode),\n};",
                }
            ],
        },
        {
            "type": "output",
            "name": "Output_Node",
            "data": [{"name": "items", "value": "{{Keywords.items[*].keyword}}"}],
        },
    ]
}

response = client.create_or_update(name="code_test", data=data)
execution = client.execute(name="code_test", data={"text": "explain me rats"})
print(execution["output"]["items"])
