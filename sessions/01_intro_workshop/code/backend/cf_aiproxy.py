import requests
import json
import weave
import config

# Initialise the weave project
weave.init('ai-workshop')
# Weave will track the inputs, outputs and code of this function
@weave.op()
def send_ai_proxy_request(config, system_message, user_message):
    url = f"https://gateway.ai.cloudflare.com/v1/{config['account']}/{config['gateway_id']}"
    
    # Construct payload for a single provider
    payload = [
        {
            "provider": config['provider'],
            "endpoint": config['endpoint'],
            "headers": {
                "Authorization": f"Bearer {config['auth_token']}",
                "Content-Type": "application/json"
            },
            "query": {
                "model": config['model'],
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ]
            }
        }
    ]

    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        # Check for successful response
        response.raise_for_status()
        
        # Parse JSON response and extract only the assistant's message content
        result = response.json()
        message_content = result['choices'][0]['message']['content']
        print(message_content)
        return message_content
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except KeyError:
        print("Message content not found in response data.")
    except Exception as err:
        print(f"Other error occurred: {err}")






