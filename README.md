**入门测试**
![这是project的整体流程](doc/image/guide.png)
This is the overall flow of the project.

Based on the project requirements, the following steps were primarily conducted:

Analyzed the data, determining that age (if present) and treatment information are distributed in the description and transcription columns, and identified the presence of case sensitivity, extra spaces, and irrelevant symbols in the data.

Preprocessed the data, including standardizing the encoding, converting to lowercase, and removing extra spaces.

Model selection: Conducted experiments with models such as llama2, llama:7b, and gemma:2b.

Strategy design: Set a series of different parameters for the model's temperature [0.1, 0.4, 0.7] and prompts, selected the best model and summarized future improvement directions after manually annotating some data combined with ChatGPT-4. Due to limited computational resources, the ablation experiment only selected the first 100 data entries, while other experiments selected data from the first 500 to 1000.

Parameter and model selection is as follows:


  model_list = ['gemma:2b','llama2',  'llama_tem_0.1', 'llama_tem_0.4', 'llama_tem_0.7']
 
  treatment_prompts = [   "Question: What patient treatment plan described in this text?",   "Question: Identify the treatment strategy for the patient's diagnosis." ]
 
  age_prompts = [   "Question: What is the patient's age based on this text?",   "Question: What is the patient's age based on this text? Tips: If there is a specific age mentioned in the text, just state 'The patient is X years old.' If the age is not explicit but can be inferred, state the possible age range and provide a brief                 reasoning. If it's not possible to determine, state 'Cannot determine the patient's age.'",   "Question: What is the patient's age based on this text? tip: Please answer very concisely. Example: the patient is 23 years old."
]

After manually annotating a small amount of data and using ChatGPT for selection, it was found that llama2 performed best under the following conditions:


 temp = 0.1
 t_prompt(treatment_prompt) = "Question: What patient treatment plan described in this text?"
 a_prompt(age_prompt) = "Question: What is the patient's age based on this text? tip: Please answer very concisely. Example: the patient is 23 years old."
It's understandable that the performance is better under a temperature of 0.1 because both questions are text extraction QA problems. Except when the patient's age needs to be inferred, which introduces some randomness, excessive diversity in other cases can reduce the model's conciseness and accuracy.

For the two different parameters in treatment_prompt, the most important should be the difference between plan and strategy. The latter focuses on strategy, adding an analysis of the patient's condition to the actual answer.

For age_prompts, the third parameter appeared because, under the first parameter, the answer still contained lengthy speculation and reasoning. However, in the second parameter of age_prompt, even obvious answers would be deduced as unable to find an accurate age and thus estimated. Reducing absolute terms like specific and explicit in the prompts lessened but did not eliminate the tendency for inference.

Optimization: Improved prompts using the Chain of thought method and recorded the results of each iteration.

Using the Cot method, llama2's treatment information performance was better than the best parameters in section 4, while the age was not satisfactory.

During the experiments, it was found that models, even when the text contains clear age information, tend to give an age range if they allow for guessing and inference in the prompts or text.

The four versions of age_prompt had the following characteristics:

csharp
Copy code
       a. Requires finding 'exact' age information, eventually 'estimating' age by synthesizing information
       
       b. Requires collecting age information, eventually 'estimating' age by synthesizing information

       c. Requires collecting age information and giving out the age

       d. Requires collecting information, giving direct age if it exists, otherwise inferring age. Requires 'concise' Q&A
         
However, all four versions were unsatisfactory when facing direct age text but performed better than llama2 in section 4 for inherently inferential age information.
  
  6：总结，缺点和改进：

      I:    由于算力和时间有限，很多数据没有进行完成的测试，消融实验的实际对比也只选取了所有组合前10条结果进行。
      
      II:   对于组合的选择，有一种更好的方法是，写一个自动比对函数，将实验结果重新喂给基准模型或者现有比较优秀的模型，加入对好模型条件的规范限制，让模型自行选择（作者这里将少量数据标签手动提取后，一方面自行比对，一方面喂给chatgpt4加入限制条件后让其判断）。或使用ROUGE score来评价。

      III:  对于模型的改进，可以在II的基础上，在一些复杂或者推断问题时，将问题喂给不同参数下的模型，再传回给基准模型总结综合生成最终回答。

      IV:   Cot在信息总结和推断方面相交于传统prompt更具有优势。然而Cot虽然在面对复杂或者需要推断信息的问题时，往往有着较为优秀的性能，在面对能直接根据文本提取答案的情况时，则会表现的比较保守。




**其他**


1:src主要放置了项目的.py文件和.ipynb文件，data中存放了原始数据和markdown的相关图片，doc中解释了所需要的全部库，和库ollama的布置和相关使用以及创建子模型的方法，result（cleaned_data;llama;llama2,llama2 Alab experiment）存放了各个部分的结果


2:对于ollama，需要先在本地布置并下载对应预训练模型，才能正常执行代码，关于ollama的更多用法，详见ollama原项目：https://github.com/ollama/ollama
  
  具体方法：
  
  1：下载ollama：
    
    window：https://ollama.com/download/OllamaSetup.exe
    
    macos： https://ollama.com/download/Ollama-darwin.zip
   
    linux:  curl -fsSL https://ollama.com/install.sh | sh

  2: 下载对应模型：
    
    ollama run model_name

  ollama支持的模型有

  ![](doc/image/model.png)

  3: 对于自定义温度的子模型，由于ollama不支持在generate中向ollama Api传递温度，需要在命令端执行CLI生成子模型：

          
          echo "FROM model_name" > Modelfile                     #model_name为父模型
          
          echo "PARAMETER temperature temp" >>Modelfile          #temp为自定义温度
          
          ollama create sub_model_name -f Modelfile              #sub_model_name为子模型名称

  显示下列情况则表示个性化子模型成功：
  ![](doc/image/create_sub_model.png)
