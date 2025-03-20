# Part II. AI는 어떻게 만들어졌을까?

1. 인공두뇌학과 초기 신경 네트워크

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
<br>

한편 1943년, 수학자 월터 피츠(Walter Pitts)와 신경심리학자였던 워런 맥컬록(Warren Sturgis McCulloch)은 인간의 신경 세포를 단순화해서 인공적으로 모델링을 함으로써, 신경 네트워크라 부루는 기술을 첫번째로 연구한 사람들로 인식되고 있다. 피츠와 맥컬록이 모델링한 인공 신경세포를 맥컬록-피츠 모델 또는 MCP Neuron이라고 하는데, 이 모델은 AND와 OR, 그리고 NOT 연산을 수행할 수 있었기 때문에 이후 인공 신경망 연구의 초석이 된다. 이 모델이 중요한 이유는 생물학적으로 영감을 받은 알고리즘을 사용하여 논리 게이트를 생성할 수 있는 방법을 보여준 것이기 때문이다. 하지만, MCP Neuron은 너무나 단순한 나머지, 가중치를 학습하는 능력도 없었고, EX-OR도 할 수 없어서 아주 간단한 선형 분리 가능 문제만을 해결할 수 있다는 한계가 있었다. 

<img src="https://github.com/user-attachments/assets/0b6b85dc-61b0-440c-b35c-1e00ae9222cd" height="200" style="display:inline-block;">

<a href="https://jontysinai.github.io/jekyll/update/2017/09/24/the-mcp-neuron.html">
<img src="https://github.com/user-attachments/assets/9179ed3d-450a-476b-9169-64da0496c20f" height="200" style="display:inline-block;">
</a>
<br><br>

MCP Neuron의 탄생한 뒤로 약 13년 후인 1956년에 당시의 선구적인 연구자들이 다트머스 학회에 참석하였는데, 거기서 컴퓨터 과학자이자 인지 과학자였던 John McCarthy가 "인공지능"이라는 용어를 처음 사용하며 여름 연구 프로젝트를 제안하게 되는데, 이 제안이 계기가 되어 인공지능은 마침내 하나의 연구 분야로 공식적으로 자리매김하게 된다. 물리학에 솔베이 회의가 있었다면, 컴퓨터 과학에는 다트머스 회의가 있다고 하고 싶다.

<img src="https://github.com/user-attachments/assets/e489fcc5-c205-4815-a858-98ab79ba2a89" height="200" style="display:inline-block;">
<br><br>

MCP Neuron의 한계 중 하나였던 가중치 학습 문제를 해결한 사람은 미국의 심리학자였던 프랭크 로젠블릿(Frank Resenblatt)이었다. 그는 햅의 학습이론에서 영감을 얻어 가중치(weight)를 학습하는 개념을 MCP Neuron에 추가하여 인공 뉴런의 모델을 개선하게 되었는데, 우리는 이를 Perceptron이라 부른다. Perceptron이 가중치를 학습하는 방법은 단순한 규칙 기반의 가중치 업데이트 방식이다. 

$$ \sum_{i=1}^{n} i = \frac{n(n+1)}{2} $$

<br><br>


2. 

<hr>

참고문헌:
- [1] [위키피디아 - 인공지능의 탄생](https://ko.wikipedia.org/wiki/%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5)
- [2] [William Grey Walter](http://www.aistudy.com/pioneer/Walter.G.htm)
