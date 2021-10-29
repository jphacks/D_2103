import numpy as np # numpyモジュールのインポート
import numpy.linalg as LA # linalgモジュールはLAとしてimportするのが慣例。

matrix = "0" #0は足し算、1は引き算、2は内積、3は外積、その他は固有値、固有ベクトル
if matrix == "0":
  input_num_e1 = 1
  input_num_e2 = 2
  input_num_f1 = 3
  input_num_f2 = 4

  e = np.array([[input_num_e1, input_num_e2]])
  f = np.array([[input_num_f1, input_num_f2]]) #２つの行列の足し算
  g = e + f

  print(g)

elif matrix == "1":
  input_num_h1 = 1
  input_num_h2 = 2
  input_num_i1 = 3
  input_num_i2 = 4

  h = np.array([[input_num_h1, input_num_h2]])
  i = np.array([[input_num_i1, input_num_i2]]) #２つの行列の引き算
  j = h - i

  print(j)

elif matrix == "2":
  input_num_a1 = 1
  input_num_a2 = 2
  input_num_b1 = 3
  input_num_b2 = 4

  a = np.array([input_num_a1,input_num_a2]) #中に数字を入れる
  b = np.array([input_num_b1,input_num_b2])
  np.dot(a,b) #行列の内積

  print(np.dot(a,b)
  )
elif matrix == "3":
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

  print(np.outer(p,q))

else:
  input_num_d1 = 1
  input_num_d2 = 2
  input_num_d3 = 3
  input_num_d4 = 4

  d = np.array([[input_num_d1 ,input_num_d2], [input_num_d3, input_num_d4]]) # 2×2の行列で試す。

  w,v = LA.eig(d) # この場合ではwが固有値、vが固有ベクトルに相当する。

  print(w)
  print(v)