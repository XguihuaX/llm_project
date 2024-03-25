import clean
import pandas as pd
from tqdm import tqdm
import ollama

original_data = clean.data()
cleaned_data = original_data.create_save()

batch_size = 100  # 设置一个合适的批处理大小
limited_data = cleaned_data.head(100)  # 如果要处理所有数据，直接使用cleaned_data
client = ollama.Client()
# 实验参数设置
temperatures = [0.1, 0.4, 0.7]
treatment_prompts = [
    "Question:What patient treatment plan described in this text?",
    "Question:Identify the treatment strategy for the patient's diagnosis."
]
age_prompts = [
    "Question:What is the patient's age based on this text?",
    "Question:What is the patient's age based on this text? Tips: If there is a specific age mentioned in the text, "
    "just state 'The patient is X years old.' If the age is not explicit but can be inferred, "
    "state the possible age range and provide a brief reasoning. If it's not possible to determine, state 'Cannot determine the patient's age.'",
    "Question:What is the patient's age based on this text? tip:Please answer very concisely.example:the patient is 23 years old."
]

# 设置保存文件的目录
save_directory = r'C:\Users\Administrator\Desktop\st\abla'

# 进行消融实验
for temperature in temperatures:
    for t_index, t_prompt in enumerate(treatment_prompts, start=1):
        for a_index, a_prompt in enumerate(age_prompts, start=1):
            treatment_summaries = []
            patient_ages = []
            for index, row in tqdm(limited_data.iterrows(), total=limited_data.shape[0]):
                text = row['description'] + " " + row['transcription']

                # 生成治疗计划的总结
                treatment_response = client.generate(model=f'llama_tem_{temperature}', prompt=f"{t_prompt}\n{text}")
                treatment_summaries.append(treatment_response['response'])

                # 生成患者年龄的问题
                age_response = client.generate(model=f'llama_tem_{temperature}', prompt=f"{a_prompt}\n{text}")
                patient_ages.append(age_response['response'])

            # 构建文件名以反映温度和提示词的使用，并指定保存目录
            filename = f"{save_directory}\\temp_{temperature}_{t_index}{a_index}.csv"
            results_df = pd.DataFrame({
                'Treatment Plan': treatment_summaries,
                'Patient Age': patient_ages
            })
            results_df.to_csv(filename, index=False)

for t_index, t_prompt in enumerate(treatment_prompts, start=1):
    for a_index, a_prompt in enumerate(age_prompts, start=1):
        treatment_summaries = []
        patient_ages = []
        for index, row in tqdm(limited_data.iterrows(), total=limited_data.shape[0]):
            text = row['description'] + " " + row['transcription']

            # 生成治疗计划的总结
            treatment_response = client.generate(model='llama2', prompt=f"{t_prompt}\n{text}")
            treatment_summaries.append(treatment_response['response'])

            # 生成患者年龄的问题
            age_response = client.generate(model='llama2', prompt=f"{a_prompt}\n{text}")
            patient_ages.append(age_response['response'])

        # 构建文件名以反映温度和提示词的使用，并指定保存目录
        filename = f"{save_directory}\\llama2_{t_index}{a_index}.csv"
        results_df = pd.DataFrame({
            'Treatment Plan': treatment_summaries,
            'Patient Age': patient_ages
        })
        results_df.to_csv(filename, index=False)
limited_data.to_csv(filename,index=False)