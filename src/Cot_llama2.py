import ollama
import clean
import pandas as pd
from tqdm import tqdm

original_data = clean.data()
cleaned_data = original_data.create_save()

batch_size = 100  # 设置一个合适的批处理大小
limited_data = cleaned_data.head(3)  # 如果要处理所有数据，直接使用cleaned_data

client = ollama.Client()

# 准备空列表来保存每个问题的总结
treatment_summaries = []
patient_ages = []

# 使用tqdm显示进度
for index, row in tqdm(limited_data.iterrows(), total=limited_data.shape[0]):
    text = f"{row['description']} {row['transcription']}"

    # 生成治疗计划的总结
    treatment_prompt = (
        "To determine the patient's treatment plan, consider the main health issue, "
        "common treatments, specific medications mentioned in the text, the patient's medical history, and current medications. "
        "Based on this, formulate a concise treatment plan.\n"
        f"{text}\n"
        "What is the concise treatment plan?"
    )

    treatment_response = client.generate(model='llama2', prompt=treatment_prompt)
    treatment_summaries.append(treatment_response['response'])

    # 年龄的提示
    age_prompt = (
        "To determine the patient's age, consider any mention of age in the text, "
        "context clues like medical history, medications, and lifestyle, and the typical age range for the health issues presented. "
        "Combine these insights to make an educated guess about the patient's age.\n"
        f"{text}\n"
        "What is the age of the patient?"
    )

    age_response = client.generate(model='llama2', prompt=age_prompt)
    patient_ages.append(age_response['response'])

    # 每处理完一批数据后保存进度，避免丢失数据
    if index % batch_size == 0 or index == limited_data.shape[0] - 1:
        partial_results_df = pd.DataFrame({
            'Treatment Plan': treatment_summaries,
            'Patient Age': patient_ages
        })
        partial_results_df.to_csv(f'C:\\Users\\Administrator\\Desktop\\st\\summary_results_{index}.csv', index=False)

# 如果需要，保存最终的完整结果
results_df = pd.DataFrame({
    'Treatment Plan': treatment_summaries,
    'Patient Age': patient_ages
})
results_df.to_csv(r'C:\Users\Administrator\Desktop\st\summary_results_final12345.csv', index=False)




'''
version1.0
    treatment_prompt = (f"Question: To determine the patient's treatment plan, consider the following steps:"
                        f"1. Identify the main health issue or diagnosis from the text.)"
                        f"2. Recall common treatments for this condition based on medical standards."
                        f"3. Check the text for any specific medications or treatments mentioned."
                        f"4. Consider the patient's past medical history and current medications."
                        f"5. Formulate a treatment plan that addresses the main health issues and aligns with the information provided."
                        f"Now, based on this text, what is the patient's treatment plan?\n{text}")

    treatment_response = client.generate(model='llama2', prompt=treatment_prompt)
    treatment_summaries.append(treatment_response['response'])

    # 生成患者年龄的问题
    age_prompt = (f"Question: To determine the patient's age, follow these steps:"
                  f"1. Look for any mention of age in the text."
                  f"2. If no exact age is mentioned, consider the context clues (like medical history, medications, lifestyle) to estimate the age range."
                  f"3. Consider the typical age range for the presented health issues or conditions."
                  f"4. Combine these insights to make an educated guess about the patient's age."
                  f"Based on the information in this text, what is the patient's age?\n{text}")
'''



'''
version2.0
treatment_prompt = (
        "To determine the patient's treatment plan, consider the main health issue, "
        "common treatments, specific medications mentioned in the text, the patient's medical history, and current medications. "
        "Based on this, formulate a concise treatment plan.\n"
        f"{text}\n"
        "What is the concise treatment plan?"
    )

    treatment_response = client.generate(model='llama2', prompt=treatment_prompt)
    treatment_summaries.append(treatment_response['response'])

    # 年龄的提示
    age_prompt = (
        "To determine the patient's age, consider any mention of age in the text, "
        "context clues like medical history, medications, and lifestyle, and the typical age range for the health issues presented. "
        "Combine these insights to make an educated guess about the patient's age.\n"
        f"{text}\n"
        "What is the estimated age of the patient?"
    )
'''
