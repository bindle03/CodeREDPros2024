import json
from openai import OpenAI
client = OpenAI(api_key='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')

faq_data = [{
    "question": "How can I get a copy of my invoice or receipt for my subscription payment?",
    "answer": "To obtain a copy of your invoice or receipt for your subscription payment, simply log in to your account and navigate to the 'Billing' section. From there, you can view and download your past invoices and receipts."
},
{
    "question": "How do I update my payment method for my subscription?",
    "answer": "To update your payment method for your subscription, log in to your account and go to the 'Billing' section. From there, you can add, remove, or modify your payment method. Be sure to save your changes to ensure that your subscription remains active."
},{
    "question": "Can I switch to a different pricing plan or downgrade my subscription?",
    "answer": "Yes, you can switch to a different pricing plan or downgrade your subscription at any time. Simply log in to your account and go to the 'Billing' section. From there, you can view and select your desired plan. Please note that if you downgrade your subscription, you may lose access to certain features or services that were available in your previous plan. Additionally, any price changes will take effect at the next billing cycle."
}]

message_objects = []
for faq in faq_data:
    message_objects.append({
        "role": "user", "content": faq['question']
    })
    message_objects.append({
        "role": "assistant", "content": faq['answer']
    })
new_prompt = "How do I switch to a new credit card?"
message_objects.append({"role":"user", "content":new_prompt})
response = client.chat.completions.create(
  model="gpt-3.5-turbo-1106",
  messages=message_objects
)
response_msg = response.choices[0].message.content
print(response_msg)