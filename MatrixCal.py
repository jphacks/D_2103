import numpy as np # numpyモジュールのインポート
import numpy.linalg as LA # linalgモジュールはLAとしてimportするのが慣例。

input_num_a1 = 1
input_num_a2 = 2
input_num_b1 = 3
input_num_b2 = 4
a = np.array([input_num_a1,input_num_a2]) #中に数字を入れる
b = np.array([input_num_b1,input_num_b2])
np.dot(a,b) #行列の内積

input_num_p1 = 1
input_num_p2 = 2
input_num_p3 = 3
input_num_p4 = 2
input_num_p5 = 1 #pの行列
input_num_q1 = 1
input_num_q2 = 1
input_num_q3 = 1
input_num_q4 = 1
input_num_q5 = 1
input_num_q6 = 1 #qの行列

p = np.array([input_num_p1, input_num_p2, input_num_p3, input_num_p4, input_num_p5])
q = np.array([input_num_q1, input_num_q2, input_num_q3, input_num_q4, input_num_q5, input_num_q6]) # 2つの１次元配列を作る。
np.outer(p,q) # 外積を求める

input_num_c1 = 1
input_num_c2 = 2
input_num_c3 = 3
input_num_c4 = 4

c = np.array([[input_num_c1, input_num_c2],[input_num_c3, input_num_c4]]) # 固有値、固有ベクトルを求める
LA.eig(c)

input_num_d1 = 1
input_num_d2 = 2
input_num_d3 = 3
input_num_d4 = 4

d = np.array([[input_num_d1 ,input_num_d2], [input_num_d3, input_num_d4]]) # 2×2の行列で試す。

w,v = LA.eig(d) # この場合ではwが固有値、vが固有ベクトルに相当する。
print(w)
print(v)

input_num_f1 = 4
input_num_f2 = 6
input_num_f3 = 8
input_num_f4 = 3
input_num_f5 = 3
input_num_f6 = 9
input_num_f7 = 4
input_num_f8 = 6
input_num_f9 = 5
input_num_f10 = 4

f = np.array([[input_num_f1, input_num_f2, input_num_f3, input_num_f4, input_num_f5],
              [input_num_f6, input_num_f7, input_num_f8, input_num_f9, input_num_f10]])
np.sum(f, axis=0) # 行方向に足し合わせる