**入门测试**
![这是project的整体流程](doc/image/guide.png)
这是project的整体流程

根据项目要求，主要做了如下步骤：

  1：分析数据，得出年龄（如果有）和治疗信息分布在description和transcription中， 并发现数据中存在大小写，多余空格和无关符号。
  
  2：数据预处理，对数据进行统一编码，小写，消除多余空格等操作。
  
  3：选择模型：选择模型llama2，llama：7b，gemma:2b进行实验。
  
  4：设计策略：针对模型的温度[0.1,0.4,0.7]和提示词设置了一系列不同的参数，通过手动标注了一定的数据结合chatgpt4后选取最佳的模型和总结未来可改进的方向。由于算力有限，消融实验只选取了前100条数据，其余实验选取了前500到前1000条数据，在手动标注少量数据和使用chatgpt进行选择后发现llama2在
  
  temp为0.1
  
  t_prompt(treatment_prompt)为"Question:What patient treatment plan described in this text?"
  
  a_prompt(age_prompt)为"Question:What is the patient's age based on this text? tip:Please answer very concisely.example:the patient is 23 years old."效果最佳。

  5：优化：使用Chain of thought 对prompt进行改进，并记录每一次的结果。

      使用Cot方法prompt的treatment infor的llama2表现比4中最好参数的llama2要优秀，而age则不尽人意。
      
      在实验过程中发现，使用含有确切，精确等词的文本或者在prompt中明确允许做猜测推断的模型，即使在数据中出现明显的年龄文本，回答都倾向于给出一个年龄区间。

      四版age_prompt的特征信息分别为:    
                
                a.要求找到‘精确’的年龄信息，最后综合信息‘估计’年龄
                
                b.要求收集年龄信息，最后综合信息‘估计’年龄

                c.要求收集年龄信息，给出年龄

                d.要求收集信息，如果存在实际年龄，则直接给出年龄，如果不能，则推断出年龄。要求‘简洁’的问答问题
      
      然而，四个版本在面对存在直接年龄文本的回答都不尽人意，而对本身需要推断的年龄信息表现的比4中的llama2要优秀。
  
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
