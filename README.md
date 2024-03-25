**入门测试**
![这是project的整体流程](doc/image/guide_line.png)
这是project的整体流程

根据项目要求，主要做了如下步骤：

  1：分析数据，得出年龄（如果有）和治疗信息分布在description和transcription中， 并发现数据中存在大小写，多余空格和无关符号。
  
  2：数据预处理，对数据进行统一编码，小写，消除多余空格等操作。
  
  3：选择模型：选择模型llama2，llama：7b，gemma:2b进行实验。
  
  4：消融实验：针对模型的温度和提示词设置了一系列不同的参数，通过手动标注了一定的数据结合chatgpt4后选取最佳的模型和总结未来可改进的方向。由于算力有限，消融实验只选取了前100条数据，其余实验选取了前500到前1000条数据，在手动标注少量数据和使用chatgpt进行选择后发现llama2在temp为0.1，t_prompt(treatment_prompt)为"Question:What patient treatment plan described in this text?"， a_prompt(age_prompt)为"Question:What is the patient's age based on this text? tip:Please answer very concisely.example:the patient is 23 years old."效果最佳。
  
  5：总结，缺点和改进：

      I:    由于算力和时间有限，很多数据没有进行完成的测试，消融实验的实际对比也只选取了所有组合前10条结果进行。
      
      II:   对于组合的选择，有一种更好的方法是，写一个自动比对函数，将实验结果重新喂给基准模型或者现有比较优秀的模型，加入对好模型条件的规范限制，让模型自行选择（作者这里将少量数据标签手动提取后，一方面自行比对，一方面喂给chatgpt4加入限制条件后让其判断）。

      III:  对于模型的改进，可以在II的基础上，在一些复杂或者推断问题时，将问题喂给不同参数下的模型，再由模型总结综合生成最终回答。




**其他**


1:src主要放置了项目的.py文件和.ipynb文件，data中存放了原始数据和markdown的相关图片，doc中解释了所需要的全部库，和库ollama的布置和相关使用以及创建子模型的方法，result（cleaned_data;llama;llama2,llama2 Alab experiment）存放了各个部分的结果


2:对于ollama，需要先在本地布置并下载对应预训练模型，才能正常执行代码。
  
  具体方法：
  
  1：下载ollama：
    
    window：https://ollama.com/download/OllamaSetup.exe
    
    macos： https://ollama.com/download/Ollama-darwin.zip
   
    linux:  curl -fsSL https://ollama.com/install.sh | sh

  2: 下载对应模型：
    
    ollama run model_name

  ollama支持的模型有

  ![](doc/image/model.png)

  3: 对于自定义温度的子模型：
    
    在命令端执行CLI:
          
          echo "FROM model_name" > Modelfile                     #model_name为父模型
          
          echo "PARAMETER temperature temp" >>Modelfile          #temp为自定义温度
          
          ollama create sub_model_name -f Modelfile              #sub_model_name为子模型名称

  显示下列情况则表示个性化子模型成功：
  ![](doc/image/create_sub_model.png)
