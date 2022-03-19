import pandas
import jieba
#定义两个DataFrame合并好评和差评的数据
newdata=pandas.DataFrame(columns=["comment","score"])
newdata1=pandas.DataFrame(columns=["comment","score"])
data1=pandas.read_excel("com_all.xls")
data2=pandas.read_excel("bad_all.xls")
mycut=lambda s:" ".join(jieba.cut(s))
data1_common1=data1.comment.apply(mycut)
data2_common2=data2.comment.apply(mycut)
newdata["comment"]=data1_common1
newdata["score"]=1
newdata1["comment"]=data2_common2
newdata1["score"]=0
#pandas中concat合并并且重新定义索引
newdata=pandas.concat([newdata,newdata1],ignore_index=True)
#comment中有\n，可以去除
newdata["comment"]=newdata["comment"].str.replace("\n","")
#切分测试集、训练集
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(newdata['comment'],
                                newdata['score'], random_state=3, test_size=0.25)
#引入停用词
with open("stopwords.txt",encoding='utf-8') as f:
    stopwords_lst = f.readlines()
stopwords = [x.strip() for x in stopwords_lst]
#使用TF-IDF进行文本转向量处理
from sklearn.feature_extraction.text import TfidfVectorizer
tv = TfidfVectorizer(stop_words=stopwords, max_features=3000, ngram_range=(1,2))
tv.fit(x_train)

#计算分类效果的准确率
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import roc_auc_score, f1_score
classifier = MultinomialNB()
classifier.fit(tv.transform(x_train), y_train)
myscore=classifier.score(tv.transform(x_test), y_test)
print(myscore)

#从京东网找两条评论来测试一下
test1="才买没一星期就送鼠标"
test2="薄，轻，携带方便"
test1=pandas.Series(test1)
test2=pandas.Series(test2)
print(test1)
print(test2)
mytest1=test1.apply(lambda x:" ".join(jieba.cut(x)))
mytest2=test2.apply(lambda x:" ".join(jieba.cut(x)))
test1_score=classifier.predict_proba(tv.transform(mytest1))[:,1]
test2_score=classifier.predict_proba(tv.transform(mytest2))[:,1]
print(test1_score)
print(test2_score)