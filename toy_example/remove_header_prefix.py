def remove_subject_tag(subject):
    return subject.replace("<h1>Subject: ", "").replace("</h1>", "")

# 使用示例
subject = "test by Hugo"
original_subject = f"<h1>Subject: {subject}</h1>"
print(original_subject)
cleaned_subject = remove_subject_tag(original_subject)
print(cleaned_subject)
