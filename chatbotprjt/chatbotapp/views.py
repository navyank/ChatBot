from django.http import JsonResponse
import json
from django.shortcuts import render

def send_message(request):
    if request.method == 'POST':
        user_input = request.POST.get('userInput', '')
        chat_body = request.POST.get('chatBody', '')

        user_message = f'<div class="chat-message user-message">{user_input}</div>'
        user_input = ''.join(e for e in user_input if e.isalnum() or e.isspace())  # Remove non-alphanumeric characters
        chat_body += user_message

        greetings = ["hello", "good morning", 'hey', 'good afternoon', 'good evening', 'howdy', "whats up", 'yo']
        if user_input.lower() in [greeting.lower() for greeting in greetings]:
            response = user_input.capitalize() + ', how may we assist you? Are you looking for a language tutor?'
            bot_message = f'<div class="chat-message bot-message">{response}</div>'
            chat_body += bot_message
            return JsonResponse({'chat_body': chat_body})

        try:
            with open('qa.json') as json_file:
                data = json.load(json_file)
                found = False
                for item in data:
                    if item['question'].lower() in user_input.lower():
                        bot_message = f'<div class="chat-message bot-message">{item["answer"]}</div>'
                        chat_body += bot_message
                        found = True
                if not found:
                    bot_message = '<div class="chat-message bot-message">Sorry, I cannot have an answer for the question right now.</div>'
                    chat_body += bot_message

                    # Show suggestions based on user input
                    for item in data:
                        if user_input.lower() in item['question'].lower():
                            suggestion = f'<div class="chat-message bot-message suggestion" onclick="selectSuggestion(\'{item["question"]}\')">{item["question"]}</div>'
                            chat_body += suggestion
                return JsonResponse({'chat_body': chat_body})
        except Exception as e:
            print(f'Error fetching JSON: {e}')
            # Display error message if JSON data cannot be fetched
            bot_message = '<div class="chat-message bot-message">Sorry, I cannot retrieve the data right now.</div>'
            chat_body += bot_message
            return JsonResponse({'chat_body': chat_body})

    return JsonResponse({'error': 'Invalid request method'})

def clear_messages(request):
    if request.method == 'POST':
        chat_body = request.POST.get('chatBody', '')
        # Remove all chat messages except the default message
        chat_messages = chat_body.split('<div class="chat-message')
        updated_chat_body = ''
        for message in chat_messages:
            if message.strip().startswith('user-message') or message.strip().startswith('bot-message'):
                updated_chat_body += f'<div class="chat-message{message}'
        return JsonResponse({'chat_body': updated_chat_body})

    return JsonResponse({'error': 'Invalid request method'})

def select_suggestion(request):
    if request.method == 'POST':
        question = request.POST.get('question', '')
        return JsonResponse({'user_input': question})

    return JsonResponse({'error': 'Invalid request method'})
def chatbot(request):
    return render(request,"index.html")
