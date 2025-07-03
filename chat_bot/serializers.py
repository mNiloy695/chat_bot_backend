from rest_framework import serializers

from .models import ChatModel
from datetime import date
from openai import OpenAI
from django.conf import settings

import tiktoken



def count_token(text, model="deepseek-chat"):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Use a fallback encoding if model is not recognized
        encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    return len(tokens)


from rest_framework import serializers
from .models import ChatModel
from datetime import date
from openai import OpenAI
from django.conf import settings
import tiktoken


def count_token(text, model="deepseek/deepseek-r1-0528:free"):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


class ChatModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatModel
        fields = '__all__'
        read_only_fields = ['response_data', 'input_token', 'created','user']

    def create(self, validated_data):
        input_data = validated_data.get('input_data')
        user = validated_data.get("user")
    
        input_token = count_token(input_data, model="deepseek/deepseek-r1-0528:free")

        if input_token > 3000:
            raise serializers.ValidationError({"error": "The max limit of input token is 3000!"})

        today = date.today()
        message_count_today = ChatModel.objects.filter(user=user, created__date=today).count()

        if message_count_today >= 80:
            raise serializers.ValidationError({"error": "You have exceeded today's message limit!"})

        try:
            client = OpenAI(
                api_key=settings.OPENAI_API_KEY,  
                base_url="https://openrouter.ai/api/v1"
            )

            response = client.chat.completions.create(
               model= "deepseek/deepseek-r1-0528:free", 
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": input_data}
                ],
                # extra_headers={
                #     "HTTP-Referer": "http://127.0.0.1:8000/",  # Your site URL (important for OpenRouter)
                #     "X-Title": "chatbot"  # Optional site name
                # }
            )

            # acces the content
            response_text = response.choices[0].message.content.strip()

        except Exception as e:
            raise serializers.ValidationError({"error": f"OpenRouter error: {str(e)}"})

        validated_data['response_data'] = response_text
        validated_data['input_token'] = input_token

        return super().create(validated_data)
