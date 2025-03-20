# Part II. AI는 어떻게 만들어졌을까?

1. 인공두뇌학

1930년대 ~ 1950대 신경학의 최신 연구는 실제 뇌가 "뉴런"이라는 작은 단위의 신경세포들로 이루어진 전기적인 네트워크라고 보았는데, 이러한 생각을 모방하여 미국의 컴퓨터 과학자이자 수학자였던 노버트 위너(Norbert Wiener)는 전기적 네트워크의 제어를 통해 인공두뇌를 묘사하였다(일명 사이버네틱스). 그리고, 섀넌은 정보 이론을 기반으로 디지털 신호로 묘사했으며, 튜링은 계산 이론을 통해 어떤 형태의 계산도 디지털로 나타낼 수 있음을 보였기 때문에, 인공두뇌의 전자적 구축이 시도될 수 있었다고 한다[1]. 

이후 미국의 신경생리학자이자 EEG(electroencephalograms, 뇌파도)를 연구한 윌리엄 그레이 월터(William Grey Walter)는 적은 수의 뇌세포들을 연결하는 것 만으로도 매우 복잡한 행동들이 발생할 수 있다는 것을 증명하고자 인공두뇌의 아이디어를 기반으로 1948~1949년 컴퓨터를 사용하지 않고 아날로그 회로만을 이용한 최초의 전기 자율로봇을 연구했는데, 이는 전기가 어떻게 엃혀서 두뇌가 작동하게 되는지에 대한 근본적인 비밀을 관찰하는 연구라는 점에서 큰 의미가 있는 것 같다. 이 최초의 전기 자율로봇은 그 모양과 느린 움직임 때문에 거북(tortoises)이라고 불리기도 했다고 한다. 이 로봇은 3개의 바퀴가 있고 빛을 따라가며 (phototaxis) 배터리가 충전될 필요가 있으면 충전소를 찾아갈 수 있었다고. 월터는 그의 동시대 인물인 앨런 튜링과 폰 노이만이 모두 디지털 계산의 견지에서 인공두뇌를 묘사할 때, 순수하게 아날로그 전기를 사용하여 두뇌과정을 모방하는 것의 중요성을 강조했다고 한다[2]. 


<a href="https://images-prod.dazeddigital.com/758/azure/dazed-prod/1060/8/1068945.JPG">
<img src="https://github.com/user-attachments/assets/2b98ebbb-bcb5-4189-9ebf-fd89f291adee" height="200" style="display:inline-block;">
</a>

<a href="https://ko.wikipedia.org/wiki/%ED%81%B4%EB%A1%9C%EB%93%9C_%EC%84%80%EB%84%8C">
<img src="https://github.com/user-attachments/assets/b7817611-cbf3-4c2f-9c35-19e30c4acd5a" height="200" style="display:inline-block;">
</a>

<a href="https://pivotal.digital/insights/1936-alan-turing-the-turing-machine">
<img src="https://github.com/user-attachments/assets/8c2be005-c81a-4f1b-bc1d-7fb1975f2078" height="200" style="display:inline-block;">
</a>

<a href="https://www.researchgate.net/profile/Marcio-Rocha-3/publication/283567826/figure/fig6/AS:669949991346177@1536739933167/Top-left-Grey-Walter-photograph-by-Hans-Moravec-top-right-Walters-machina.jpg">
<img src="https://github.com/user-attachments/assets/74b030e1-a139-4692-9187-42a68ffe238d" height="200" style="display:inline-block;">
</a>
<br>

왼쪽부터 차례대로, [Norbert Wiener], [Claude Elwood Shannon], [Alan Turing & The Turing Machine], and [W. Grey Walter with early tortoise]
<br><br><br>

2. 초기 인공 신경망과 인공지능 연구분야의 탄생, 그리고 인공지능 연구의 첫번째 겨울

인공 신경망의 초석인 인공 뉴런(인공 신경세포)이 Perceptron으로 발전하고, Perceptron이 다시 Multi-Layer Perceptron으로 발전하며 오늘날 우리가 사용하는 복잡한 인공 신경망이 가능해졌다고 할 수 있다. 그 과정을 좀 더 자세히 보면 다음과 같다.<br>

1943년, 수학자 월터 피츠(Walter Pitts)와 신경심리학자였던 워런 맥컬록(Warren Sturgis McCulloch)은 인간의 신경 세포를 단순화해서 인공적으로 모델링을 함으로써, 신경 네트워크라 부루는 기술을 첫번째로 연구한 사람들로 인식되고 있다. 피츠와 맥컬록이 모델링한 인공 신경세포를 맥컬록-피츠 모델 또는 MCP Neuron이라고 하는데, 이 모델은 AND와 OR, 그리고 NOT 연산을 수행할 수 있었기 때문에 이후 인공 신경망 연구의 초석이 된다. 이 모델이 중요한 이유는 생물학적으로 영감을 받은 알고리즘을 사용하여 논리 게이트를 생성할 수 있는 방법을 보여준 것이기 때문이다. 하지만, MCP Neuron은 너무나 단순한 나머지, 가중치를 학습하는 능력도 없었고, EX-OR도 할 수 없어서 아주 간단한 선형 분리 가능 문제만을 해결할 수 있다는 한계가 있었다. 

<img src="https://github.com/user-attachments/assets/0b6b85dc-61b0-440c-b35c-1e00ae9222cd" height="200" style="display:inline-block;">

<a href="https://jontysinai.github.io/jekyll/update/2017/09/24/the-mcp-neuron.html">
<img src="https://github.com/user-attachments/assets/9179ed3d-450a-476b-9169-64da0496c20f" height="200" style="display:inline-block;">
</a>
<br><br>

MCP Neuron의 탄생한 뒤로 약 13년 후인 1956년에 당시의 선구적인 연구자들이 다트머스 학회에 참석하였는데, 거기서 컴퓨터 과학자이자 인지 과학자였던 John McCarthy가 "인공지능"이라는 용어를 처음 사용하며 여름 연구 프로젝트를 제안하게 되는데, 이 제안이 계기가 되어 인공지능은 마침내 하나의 연구 분야로 공식적으로 자리매김하게 된다. 물리학에 솔베이 회의가 있었다면, 컴퓨터 과학에는 다트머스 회의가 있다고 하고 싶다.

<img src="https://github.com/user-attachments/assets/e489fcc5-c205-4815-a858-98ab79ba2a89" height="200" style="display:inline-block;">
<br><br>

MCP Neuron의 한계 중 하나였던 가중치 학습 문제를 해결한 사람은 미국의 심리학자였던 프랭크 로젠블릿(Frank Rosenblatt)이었다. 그는 1957년에 햅의 학습이론에서 영감을 얻어 가중치(weight)를 학습하는 개념을 MCP Neuron에 추가하여 인공 뉴런의 모델을 개선하게 되었는데, 우리는 이를 Perceptron이라 부른다. 그 당시 뉴욕타임즈는 이 Perceptron을 소개하는 기사에서 조만간 인간과 같은 기계가 탄생할 것이라고 예견하면서 세간의 엄청난 기대를 불러 일으켰다고 합니다. 많은 사람들이 Perceptron을 통해 진짜 인간과 같은 인공지능을 곧 만들 수 있을 것이라고 생각했다고 하니, 얼마나 기대가 컸을까.... Perceptron이 가중치를 학습하는 방법은 아래에 식으로 나타낸 것과 같은 단순한 규칙 기반의 가중치 업데이트 방식이었다. 즉, 오차가 0이 될 때까지 단순히 오차에 학습률을 곱해서 가중치를 업데이트하는 과정을 반복하는 것이다. 그리고 이 Perceptron까지만 해도 활성화 함수로는 sigmoid 함수가 사용되었다고 한다.(ReLU 같은 더 정교한 활성화 함수는 이후에 제안된다)

$$ w_i = w_i + \alpha \cdot e \cdot x_i \hspace{0.2cm}, \hspace{1cm}(w_i: \text{weight for }x_i \hspace{0.2cm}, \hspace{1cm} e = y_i - \hat{y_i}, \hspace{1cm} \alpha: \text{learning rate}) $$
<br>

<a href="http://solarisailab.com/archives/1206">
<img src="https://github.com/user-attachments/assets/abfb8eb3-b05c-43ea-b6d6-a6ea16710a63" height="200" style="display:inline-block;">
</a><br>
(왼쪽) Percentron 이미지 인식 센서와 Frank Rosenblatt, (오른쪽) Mark 1으로 구현된 Frank Rosenblatt의 Perceptron
<br><br>

하지만, Perceptron은 그 당시 사람들의 기대와는 달리, 단순한 선형 분류기였기 때문에 EX-OR 문제를 포함한 복잡한 비선형 문제는 해결할 수 없다는 한계가 있었는데, 이 문제에 대한 해법이 연구되기도 전에 Perceptron으로는 EX-OR 문제는 해결할 수 없다는 것을 Marvin Minsky와 Seymour Papert가 1969년에 수학적으로 증명을 해 버림으로써, 인공지능에 대한 기대와 열기가 급속히 사그라들었다고 한다[3].
<br><br><br>


3. 인공 신경망의 부활

안된다고 가만히 손놓고 있을 인류가 아니었을까? 인공 신경망에 대한 관심히 싸늘하게 식어 있던 기간에도 묵묵히 연구를 이어가는 학자들은 있었는데, 그 중 McClelland, James L., David E. Rumelhart, and Geoffrey E. Hinton이 1986년에 “Parallel Distributed Processing”라는 책을 통해 히든 레이어를 가진 Multi-Layer Perceptrons(MLP)과 Backpropagation Algorithm을 제시하면서 perceptron이 가졌던 문제를 해결할 수 있게 되었다. 기존의 perceptron이 단순 선형 분류기라는 한계에 의해 EX-OR 문제를 해결할 수 없었다면, Multi-Layer Perceptrons(MLP)는 히든 레이어(Hidden Layer)라는 중간 레이어를 추가함으로써, 선형 분류 판별선을 여러개 그리는 효과를 얻을 수 있었고, 그 결과로 EX-OR 문제를 해결할 수 있게 한 것이었다[3].

여기서 잠시 다른 이야기를 하자면, 전기학의 회로 이론에서도 AND, OR, NOT, 또는 EX-OR 연산을 위한 논리 회로를 그릴 수 있다. 그런데, 이 논리 회로에서도 Perceptron 처럼 앞의 세 가지 연산(AND, OR, NOT)은 하나의 레이어로 표현이 되지만, EX-OR 회로는 한 개의 레이어로는 구현하지 못한다. 이를 구현하기 위해서는 아래의 그림처럼 두 개의 레이어를 이어 붙여야만 구현이 가능하다. Geoffrey E. Hinton 등이 MLP를 제안할 때 회로 이론에서 영감을 얻은 것일까? 아니면, 수학적으로 불가능이 증명된 문제라 하더라도 차원을 늘리면 해결되는 경우를 종종 볼 수 있는데, 그러한 수학적 영감을 떠올렸던 것일까?라는 궁금증이 생긴다.

<img src="https://github.com/user-attachments/assets/c09e9090-4701-454e-8606-c149d949ccc8" height="200" style="display:inline-block;">
<br>[AND, OR, NOT, EX-OR의 논리 회로도]<br><br>

다시 하던 이야기로 돌아오면, 비록 EX-OR 문제를 풀 수 있다고는 해도, MLP만으로는 파라미터의 개수가 많아지면서 적절한 weight를 학습하는 것이 매우 어려워진다는 문제가 있었는데, "Parallel Distributed processing"의 저자들은 Back-Propagation Algorithm을 함께 제안해서 이 문제도 해결한 것이었다. Back-Propagation Algorithm은 정방 연산(FeedForward)을 통해 결과 값을 예측한 후, 예측값과 실제값 사이의 오차를 후방(Backward)으로 다시 보내는데, 이 때 미분을 통해 각 레이어의 노드들이 오차값에 미친 영향도를 파악해서 weight를 업데이트할 수 있게 한 것이다. 이러한 MLP는 이후 현재까지도 인공 신경망에서 사용되고 있다. 
<br><br><br>


4. 인공지능 분야의 두 번째 겨울, 기울기 소실 문제
   
Back-propagation과  MLP로 EX-OR 문제도 해결하게 되자, 인공 신경망은 거침 없이 발전할 것만 같았다. 그러나, 안타깝게도, 이번에는 신경망의 깊이, 그러니까 레이어의 갯수가 늘어날 수록 오차가 역전파 되는 과정에서 기울기가 0으로 수렴하는 현상, 즉 Gradient Vanishing 문제가 발행한다는 것이 밝혀지면서 또 한 번의 연구 침체기가 찾아온다.

<img src="https://github.com/user-attachments/assets/5f1f2f29-82d7-42a1-a2e8-5514238262d0" width="500" style="display:inline-block;">
<img src="https://github.com/user-attachments/assets/0c4065a9-f94b-4786-ba85-9fb27af17db8" height="200" style="display:inline-block;">
<br>&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;Gradient Vanishing Problem in Deep Neural Networks,   &nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp; Sigmoid 함수값과 미분값(기울기) 곡선<br>
<br>

위의 오른쪽에 있는 그림은 그 당시 사용되던 활성화 함수인 sigmoid 함수의 함수값(빨간색)과, 함수값을 미분하여 구한 순간 변화량 즉, 기울기(파랑색)를 보여주는 그래프이다. 그래프의 왼쪽과 오른쪽 끝으로 갈수록 기울기가 0으로 수렴하는 것이 보일 것이다. 이것이 바로 기울기가 없어지게 되는 문제의 핵심이었으며, 이후 ReLU(Rectified Linear Unit) 함수와 같이 기울기가 0으로 수렴하지 않는 활성화 함수들이 제안되면서 이 문제 또한 극복하게 된다.

<img src="https://github.com/user-attachments/assets/6232b55c-ddad-4df3-8beb-b11f80343766" height="200" style="display:inline-block;">
<br>&nbsp; &nbsp;&nbsp;&nbsp;ReLU 함수값과 기울기 곡선
<br><br>

  
5. 새로운 인경 신경망 구조, CNN의 탄생

1989년에 Yann LeCun은, 카나다와 스웨덴의 두 신경과학자였던 데이비드 허벨(David H. Hubel)과 톨스텐 위젤(Torsten Wiesel)의 고양이 시각 피질 연구에서 영감을 얻어서, 국소 영역의 정보를 거르는 일종의 작은 필터인 kernel(weight sharing)을 신경망에 도입하고 이를 통해 convolutional feature map을 생성하는 새로운 인공 신경망 구조인 CNN을 제안함으로써 이미지 분야에서도 인공지능이 본격적으로 적용되기 시작하였다[4]. 이후, Yann LeCun과 Yoshua Bengio, Leon Bottou, 그리고 Patrick Haffner는 1998년에 "Gradient-Based Learning Applied to Document Recognition"이라는 제목의 논문에서 CNN(Convolutional Neural Networks) 구조로 개발한 모델인 LeNet-5 통해, 2차원 입력 데이터(2D shaped) 상의 변화를 인식하고 분류할 수 있는 CNN 모델의 우수성을 발표하였다.
<br><br>


6. 적응적 가중치 수정 개념의 도입

인공 신경망에서 Back-propagation을 통해 가중치를 조정하는 역할을 하는 것을 optimizer라 한다. 이 optimizer는 신경망의 후방으로 오차값을 역전파하면서 각 레이어마다 있는 노드들의 기울기(해당 노드가 계산된 오차에 영향을 미친 정도)를 알아내고, 이를 기반으로 가중치를 업데이트하는데, 모델의 현재 상황에 관계 없이 무조건 동일한 학습률을 적용해서 업데이트하는 대신, 상황에 따라 적응적으로 가중치를 달리 업데이트하는 Adaptive optimizer(적응적 최적화기)가 제안되면서 특정 분야에서는 인공 신경망의 성능이 개선되기도 하였다. 그런데, 사실 이 "적응적"이라는 개념은 일찍이  1960에 미국 스탠포드 대학의 교수였던 Bernard Widrow와 그의 제자 Ted Hoff가 가중치를 조정할 수 있는 적응적 인공신경망인 ADALINE을 제안한 것에서부터 발전된 것이라고 할 수 있다. ADALINE은 아래의 그림과 같이 소프트웨어가 아니라 전기적으로 설계되고 구현된 기계장치였다.

<a href="https://en.wikipedia.org/wiki/ADALINE">
<img src="https://github.com/user-attachments/assets/1b34fcac-4279-403e-bb79-0ded1c49ce9e" height="200" style="display:inline-block;"></a>
<br>[ADALINE]
<br><br>

컴퓨터는 0과 1의 이진수로 모든 것을 처리하는 장치이고, 전기적인 논리 회로 또한 On과 Off 두 가지 상태를 가지고 입력을 처리하고 출력을 생성하는 것임을 고려해 본다면, EX-OR 문제의 해법과 적응적 가중치 개념의 도입에서 처럼, 이 둘은 서로 영감을 주고 받을 수 있는 영역이 많이 있을 것 같다.

<hr>

참고문헌:
- [1] [위키피디아 - 인공지능의 탄생](https://ko.wikipedia.org/wiki/%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5)
- [2] [William Grey Walter](http://www.aistudy.com/pioneer/Walter.G.htm)
- [3] [딥러닝의 역사](http://solarisailab.com/archives/1206)
- [4] [Handwritten digit recognition with a back-propagation network](https://proceedings.neurips.cc/paper/1989/file/53c3bce66e43be4f209556518c2fcb54-Paper.pdf)
 
