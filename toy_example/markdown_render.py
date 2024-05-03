data = {
    'subject': '[主旨]',
    'caseId': '[獨特案例編號]',
    'startDate': '[現在日期]',
    'transcript': [
        {'Submitted by': 'Customer', 'content': '我需要學習中文的幫助。你能提供任何資源或建議嗎？'},
        {'Submitted by': 'TAM', 'content': '當然可以！我可以幫你。學習中文可能會有一些挑戰，但是有了正確的資源和練習，你可以有所進步。讓我和你分享一些建議和資源。'},
        {'Submitted by': 'Customer', 'content': '謝謝！我期待你的推薦。'}
    ]
}

markdown_output = ""

for item in data['transcript']:
    markdown_output += "```\nSubmitted by {}\nContent: {}\n```\n\n".format(item['Submitted by'], item['content'])

print(markdown_output)
