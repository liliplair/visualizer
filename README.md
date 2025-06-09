# visualizer

辅助深度学习模型中Attention模块可视化的小工具，通过装饰函数，修改函数的字节码，将待捕获变量与原返回值打包处理后返回原值，从而跟踪模型中参数变化，并保持原结果不变

旨在便携地捕获模型训练、推理过程中的变量，包括可变参数、张量等，同时减少代码改动，可随时关闭，并减小开销

对于单变量、列表、元组可以主动 detach ，但不支持字典

在[Visualizer](https://raw.githubusercontent.com/luo3300612/Visualizer/refs/heads/main/README.md)基础上修改：
- 增加了多变量的捕获功能  
- 增加了对闭包变量的捕获功能

具体用法和测试在 test.ipynb

## references
[Visualizer](https://raw.githubusercontent.com/luo3300612/Visualizer/refs/heads/main/README.md)

[字节码：分析 Python 执行的终极利器](https://zhuanlan.zhihu.com/p/382180226)
