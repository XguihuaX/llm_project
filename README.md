![这是project的整体流程](doc/image/guide_line.png)
这是project的整体流程

根据项目要求，主要做了如下步骤：

  1：分析数据，得出年龄（如果有）和治疗信息分布在description和transcription中， 并发现数据中存在大小写，多余空格和无关符号。
  
  2：数据预处理，对数据进行统一编码，小写，消除多余空格等操作。
  
  3：选择模型：选择模型llama2，llama：7b，gemma:2b进行实验。
  
  4：消融实验：针对模型的温度和提示词设置了一系列不同的参数，通过手动标注了一定的数据结合chatgpt4后选取最佳的模型和总结未来可改进的方向。由于算力有限，消融实验只选取了前100条数据，llama和llama2分别选取了前500和前2000条数据。
  
  5：总结。


src主要放置了项目的.py文件，data中存放了原始数据和markdown的相关图片，doc中解释了所需要的全部库，和库ollama的布置和相关使用以及创建子模型的方法，result（cleaned_data;llama;llama2,llama2 Alab experiment）存放了各个部分的结果


