## Installation

创建虚拟环境：

```shell
conda env create -f environment.yaml
conda activate pre_music_year
```

##### 	原始数据集下载：

```shell
wget http://millionsongdataset.com/sites/default/files/AdditionalFiles/TRAXLZU12903D05F94.h5
```

处理后数据集下载（建议）：[csv文件](https://drive.google.com/drive/folders/1C5ZQZmKBBvcmk8t37Mo5FS0vZrFe_rKb?usp=share_link)

下载后处理数据集：

```shell
sh ./deal_datasets.sh
```

## 1.题目

<img src="%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%E5%AE%9E%E8%B7%B5.assets/%E6%88%AA%E5%B1%8F2023-01-04%2020.20.50.png" alt="截屏2023-01-04 20.20.50" style="zoom:33%;" />

## 2.数据预处理

 1. #### 读取h5文件，并转化为txt文件

    参考数据集提供代码：https://github.com/tbertinmahieux/MSongsDB/blob/master/PythonSrc/hdf5_getters.py

 2. #### 将txt文件转化为csv文件

    a. 首先将txt文件转化为csv文件，使用python的csv库

    ```python
    import csv
    
    raw_csv_path = "./datasets/raw_data.csv"
    raw_txt_path = "./datasets/YearPredictionMSD.txt"
    
    csvFile = open(raw_csv_path,'w',newline='',encoding='utf-8')
    writer = csv.writer(csvFile)
    csvRow = []
    
    f = open(raw_txt_path,'r',encoding='GB2312')
    for line in f:
        csvRow = line.split(',')
        writer.writerow(csvRow)
    
    f.close()
    csvFile.close()
    ```

    b. 为了后续算法和数据可视化，添加标题行

    ```python
    import csv
    
    raw_csv_path = "./datasets/raw_data.csv"
    addtitle_csv_path = "./datasets/addtitle.csv"
    
    # set title names
    header_list = ['Year']
    for i in range(1,91):
        header_list.append('attr' + str(i))
    
    # read raw csv and insert title
    with open(raw_csv_path, "r") as infile:
        reader = list(csv.reader(infile))
        reader.insert(0, header_list)
    
    with open(addtitle_csv_path, "w") as outfile:
        writer = csv.writer(outfile)
        for line in reader:
            writer.writerow(line)
    ```

    c. 根据题目提示，保留前12个特征，以减少计算量

    ```python
    import csv
    import os
    
    addtitle_csv_path = "./datasets/addtitle.csv"
    delcol_csv_path = "./datasets/data.csv"
    
    # set the index of columes
    cols_to_remove = []
    for i in range(13,91):
        cols_to_remove.append(i) # Column indexes to be removed (starts at 0)
    
    cols_to_remove = sorted(cols_to_remove, reverse=True) # Reverse so we remove from the end first
    row_count = 0 # Current amount of rows processed
    
    with open(addtitle_csv_path, "r") as source:
        reader = csv.reader(source)
        with open(delcol_csv_path, "w", newline='') as result:
            writer = csv.writer(result)
            for row in reader:
                row_count += 1
                print('\r{0}'.format(row_count), end='') # Print rows processed
                for col_index in cols_to_remove:
                    del row[col_index]
                writer.writerow(row)
    
    # remove addtitle csv
    cmd = "rm -rf " + addtitle_csv_path
    os.system(cmd)
    ```

最终效果展示（仅前10行）：
<img src="%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%E5%AE%9E%E8%B7%B5.assets/%E6%88%AA%E5%B1%8F2023-01-04%2020.40.16.png" alt="截屏2023-01-04 20.40.16" style="zoom:50%;" />

## 3.数据特征展示

#### 1.数据统计信息

|       |          Year |         attr1 |         attr2 |         attr3 |         attr4 |         attr5 |         attr6 |         attr7 |         attr8 |         attr9 |        attr10 |        attr11 |        attr12 |
| ----: | ------------: | ------------: | ------------: | ------------: | ------------: | ------------: | ------------: | ------------: | ------------: | ------------: | ------------: | ------------: | ------------: |
| count | 515345.000000 | 515345.000000 | 515345.000000 | 515345.000000 | 515345.000000 | 515345.000000 | 515345.000000 | 515345.000000 | 515345.000000 | 515345.000000 | 515345.000000 | 515345.000000 | 515345.000000 |
|  mean |   1998.397082 |     43.387126 |      1.289554 |      8.658347 |      1.164124 |     -6.553601 |     -9.521975 |     -2.391089 |     -1.793236 |      3.727876 |      1.882385 |     -0.146527 |      2.546063 |
|   std |     10.931046 |      6.067558 |     51.580351 |     35.268585 |     16.322790 |     22.860785 |     12.857751 |     14.571873 |      7.963827 |     10.582861 |      6.530232 |      4.370848 |      8.320190 |
|   min |   1922.000000 |      1.749000 |   -337.092500 |   -301.005060 |   -154.183580 |   -181.953370 |    -81.794290 |   -188.214000 |    -72.503850 |   -126.479040 |    -41.631660 |    -69.680870 |    -94.041960 |
|   25% |   1994.000000 |     39.954690 |    -26.059520 |    -11.462710 |     -8.487500 |    -20.666450 |    -18.440990 |    -10.780600 |     -6.468420 |     -2.293660 |     -2.444850 |     -2.652090 |     -2.550060 |
|   50% |   2002.000000 |     44.258500 |      8.417850 |     10.476320 |     -0.652840 |     -6.007770 |    -11.188390 |     -2.046670 |     -1.736450 |      3.822310 |      1.783520 |     -0.097950 |      2.313700 |
|   75% |   2006.000000 |     47.833890 |     36.124010 |     29.764820 |      8.787540 |      7.741870 |     -2.388960 |      6.508580 |      2.913450 |      9.961820 |      6.147220 |      2.435660 |      7.360330 |
|   max |   2011.000000 |     61.970140 |    384.065730 |    322.851430 |    335.771820 |    262.068870 |    166.236890 |    172.402680 |    126.741270 |    146.297950 |     60.345350 |     88.020820 |     87.913240 |

#### 2.年份数据量分布图

<img src="%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%E5%AE%9E%E8%B7%B5.assets/output.png" alt="output" style="zoom:50%;" />

#### 3.属性的分类散点图

<img src="%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%E5%AE%9E%E8%B7%B5.assets/output1.png" alt="output1" style="zoom:50%;" />

​																													*attr1的分类散点图*

<img src="%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%E5%AE%9E%E8%B7%B5.assets/output2.png" alt="output2" style="zoom:50%;" />

​																													*attr3的分类散点图*

#### 4.属性的箱式图

<img src="%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%E5%AE%9E%E8%B7%B5.assets/output3.png" alt="output3" style="zoom:50%;" />

​																										*attr1的随年份分布的箱式图*

<img src="%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%E5%AE%9E%E8%B7%B5.assets/output4.png" alt="output4" style="zoom:50%;" />

​																												*所有属性的箱式图*

#### 5.变量之间的相关性图

<img src="%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%E5%AE%9E%E8%B7%B5.assets/output5.png" alt="output5" style="zoom:50%;" />

#### 6.按照decade分布的热力图

<img src="%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%E5%AE%9E%E8%B7%B5.assets/output6.png" alt="output6" style="zoom:50%;" />

## 4.分类预测

#### 1.KNN法：

可视化KNN方法的参数一和参数二

<img src="%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%E5%AE%9E%E8%B7%B5.assets/%E6%88%AA%E5%B1%8F2023-01-04%2021.12.20.png" alt="截屏2023-01-04 21.12.20" style="zoom:40%;" />

发现可视化结果的分类效果并不好，输出准确值：

<img src="%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%E5%AE%9E%E8%B7%B5.assets/%E6%88%AA%E5%B1%8F2023-01-04%2021.14.08.png" alt="截屏2023-01-04 21.14.08" style="zoom:50%;" />



#### 2.PCA法：

可视化PCA降维效果（降至3维）

<img src="%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%E5%AE%9E%E8%B7%B5.assets/output7-2838182.png" alt="output7" style="zoom:50%;" />

划分出不同年份

<img src="%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%E5%AE%9E%E8%B7%B5.assets/output8.png" alt="output8" style="zoom:50%;" />

发现降维效果并不理想，存在很多重叠部分，对于分类任务帮助不大



#### 3.SVC法：

SVC的运行时间较长，通过查看SVC的官方文档，原因是因为

> **"The fit time scales at least quadratically with the number of samples and may be impractical beyond tens of thousands of samples."**

算法的时间复杂度大约是样本数量的平方，本实验中样本数量较多，将会导致较长的运行时间



#### 4.随机森林：

使用留出法分割训练集和测试集，输出前100个预测值：

<img src="%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%E5%AE%9E%E8%B7%B5.assets/%E6%88%AA%E5%B1%8F2023-01-04%2021.29.42.png" alt="截屏2023-01-04 21.29.42" style="zoom:50%;" />

测试集标签：

<img src="%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%E5%AE%9E%E8%B7%B5.assets/%E6%88%AA%E5%B1%8F2023-01-04%2021.30.30.png" alt="截屏2023-01-04 21.30.30" style="zoom:50%;" />

随机森林各年份分类概率：

<img src="%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%E5%AE%9E%E8%B7%B5.assets/%E6%88%AA%E5%B1%8F2023-01-04%2021.31.55.png" alt="截屏2023-01-04 21.31.55" style="zoom:50%;" />

预测准确率：

<img src="%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%E5%AE%9E%E8%B7%B5.assets/%E6%88%AA%E5%B1%8F2023-01-04%2021.32.31.png" alt="截屏2023-01-04 21.32.31" style="zoom:50%;" />

可见随机森林法分类准确率达到了100%，可能存在一定程度的过拟合

> 使用留出法将会有多少样本未被投入训练集：

$$
\lim^{}_{m \to \infty}({1-\frac{1}{m}})^m = \frac{1}{e} \approx 0.368
$$



#### 5.深度学习：

使用两层全连接层，一层softmax层作为网络结构，进行分类任务：

```python
def get_network():
    model = kr.models.Sequential()
    model.add(Dense(20, input_shape=(train_features.shape[1],), activation="relu"))
    model.add(Dense(20, activation="relu"))
    model.add(Dense(label_count, activation="softmax"))
    opt = "adam"
    model.compile(loss= "categorical_crossentropy", optimizer=opt, metrics=["accuracy"], )
    return model
```

训练过程：

<img src="../Library/Application%20Support/typora-user-images/%E6%88%AA%E5%B1%8F2023-01-04%2021.42.32.png" alt="截屏2023-01-04 21.42.32" style="zoom:30%;" />

训练结果通过混淆矩阵热力图展示：

<img src="%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%E5%AE%9E%E8%B7%B5.assets/%E6%88%AA%E5%B1%8F2023-01-04%2021.44.01.png" alt="截屏2023-01-04 21.44.01" style="zoom:50%;" />

混淆矩阵：

<img src="%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%E5%AE%9E%E8%B7%B5.assets/%E6%88%AA%E5%B1%8F2023-01-04%2021.44.26.png" alt="截屏2023-01-04 21.44.26" style="zoom:50%;" />

可见对角线上分类的概率最大，说明分类正确，分类效果较好

## 5.实验总结

想法验证，对于结果有轻微的提升：

1.划分训练集和测试集的时候不整体随机划分，而是按照年份随机划分，这样做的好处是数据分布不均匀，有的年份样本量太小，可能该年份没有加入训练集直接加入测试集造成模型未学习到；

2.进行归一化，虽然数据值的大小没有差很多个数量级，但是仍然会对权重产生轻微的影响；

3.尝试了一下深度学习的算法，用全连接网络

4.可以根据相关性图对原始的所有数据进行降维，前12个属性中部分属性对于分类效果不明显，根据原始数据降至12维可能会对最后的结果带来一定的帮助

5.按照decades表示，会减少计算量，更便于验证想法

6.根据数据分布特征，可以尝试核函数

7.许多sklearn的算法不支持GPU加速，因为sklearn在设计时就有意识的设置成CPU，方便跨设备使用，可以手写cuda，加速训练

8.设置验证集，部分算法极有可能过拟合



完整代码：https://github.com/shannonchen37/predict_music_year

