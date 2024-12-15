# HuskeyLensの仕様メモ

### 物体認識(Object recognition)
HuskyLens can recognize 20 built-in objects. <br>
aeroplane, bicycle, bird, boat, bottle, bus, car, cat, chair, cow, diningtable, dog, horse, motorbike, person, potted lant, sheep, sofa, train, TV.<br>
メモ：物体認識はモデル学習済みであるが、物体認識機能を使うには、認識したい対象にカメラを向けて学習させる必要がある。学習後、blockとして返却される。識別ID(数字)は学習した順番に割り振られる。例えば、犬を物体認識させたい場合、カメラを犬に向けて学習させる。最初に学習したのが犬であれば犬を認識するとID:1となる。

### 画面サイズ
画面サイズは、320 x 240、中心の座標は (160, 120)







### 関連情報
- https://wiki.dfrobot.com/HUSKYLENS_V1.0_SKU_SEN0305_SEN0336
- https://www.dfrobot.com/blog-13457.html
- https://community.dfrobot.com/projects-HUSKYLENS.html
