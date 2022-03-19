import pandas
import jieba
#import imageio
from wordcloud import WordCloud
data1=pandas.read_excel("com_all.xls")
data2=pandas.read_excel("bad_all.xls")
mycut=lambda s:" ".join(jieba.cut(s))
data1_common1=data1.comment.apply(mycut)
data2_common2=data2.comment.apply(mycut)
print(data1_common1)
print(data2_common2)
print("-----------------")
#读取停用词文件
with open("stopwords.txt","r",encoding="utf8") as f:
    #方法read不是一个列表，readlines输出一个列表
    stop=f.readlines()
#列表中元素\n，需要进行处理
stop_words=[x.strip() for x in stop]
#将集合中的每一个文本去重
stop_words=list(set(stop_words))
print(stop_words)
#切分好评的句子，把句子转成词,切分后的列表中含用\n，将\n替换掉
data1_common1=data1_common1.apply(lambda s:s.replace("\n",""))
other_p=data1_common1.apply(lambda s:s.split(" "))
#对句子词构成的列表遍历，去除停用词
another_p=other_p.apply(lambda x:[i for i in x if i not in stop_words])
print(another_p)
#同理操作差评的词汇
data2_common2=data2_common2.apply(lambda s:s.replace("\n",""))
other_e=data2_common2.apply(lambda s:s.split(" "))
another_e=other_e.apply(lambda x:[i for i in x if i not in stop_words])
print(another_e)
#画好评的词云图
good_post=[]
another_p.apply(lambda x:[good_post.append(i) for i in x])
print(good_post)
wc=WordCloud(background_color="white",max_words=100,max_font_size=100,
             random_state=50,font_path="msyh.ttc")
wc.generate(' '.join(good_post))
wc.to_file("aa.png")
#画差评的词云图
#pic = imageio.imread('white.bmp')	,在wordcloud中mask=pic
error_post=[]
another_e.apply(lambda x:[error_post.append(i) for i in x])
print(error_post)
wc=WordCloud(background_color="white",max_words=100,max_font_size=100,
             random_state=50,font_path="msyh.ttc")
wc.generate(' '.join(error_post))
wc.to_file("bb.png")