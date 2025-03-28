# Part I. AI란?

인공지능(AI, Artificial Intelligence)이란 무엇이고, 어떻게 만들어졌으며, 무슨 일들을 할 수 있는 지, 그리고 무엇보다도 사람들은 인공지능에 왜 그토록 열광하는 지 등을 이해하기 위한 첫 걸음으로, 일단  Ian Goodfellow, Yoshua Bengio 그리고 Aaron Courville님께서 저술하신 교재[1]에 나와있는 아래의 그림을 한 번 보기로 한다. 

참고로, 요수아 벤지오(Yoshua Bengio)는 제프리 힌튼(Geoffrey Hinton), 얀 르쿤(Yann LeCun), 앤드루 응(Andrew Ng)과 함께 현대 인공지능계의 4대 천왕 중 한 사람으로 잘 알려져 있으며, Ian Goodfellow와 Aaron Courville은 이 분의 제자들이다. 한편, Ian Goodfellow는 Generative Adversarial Networks(GAN, 적대적 생성 모델)을 만들고 논문으로 발표한 컴퓨터 과학자로도 유명하다.


<div style="text-align: center;">
  <img src="https://github.com/iispace/AI/raw/main/Pictures/Relationship%20between%20AI%20technology_.jpg" alter="Relationship between deep learning, representation learning, machine learning, and AI" width=600/><br>
  [Relationship between deep learning, representation learning, machine learning, and AI]
<br>
</div>

<br><br>
위 그림에서는 machine learning이 AI의 범주에 속하는 것으로 표현되고 있으나, 관점에 따라서는 AI가 machine learning의 범주에 속하는 것으로 표현할 수도 있겠다. 이것은 크게 중요한 의미가 있다기 보다는, 기술을 분류하는 기준이 다른 것 뿐이라고 생각된다. 즉, AI(인공지능)을 구현하기 위한 기술로서 바라본다면 machine learning이라는 기법이 당연히 AI의 범주에 속할 것이나, 반대로 machine learning이 구현할 수 있는 것이 무엇인가? 라는 관점으로 본다면 AI는 machine learning에 속하는 것으로 표현될 수 있다고 할 수 있을 것 같다. 그러므로, AI가 더 큰 범위인지 machine learning이 더 큰 범위인지를 굳이 묻는다면, 바라보는 기준에 따라 전자도 될 수 있고 후자도 될 수 있다고 말하고 싶다.  

우리가 잘 알고 있듯이, 아직 인류는 "생명"이 무엇인지에 대한 정의를 명확하게 내리지 못하고 있는데, 이는 "생명"이라 불리우는 개체들의 속성이 너무나 다양하고, 경계가 불분명하며, 각 학문 분야에서 바라보는 시각에 따라 중요하게 여기는 기준도 다르고, 이들이 보여주는 행동 특성 또한 다양하기 때문일 수 있다. 

우리가 대충 "생명"이라 부르는 다양한 객체들은 유기물들의 조합으로 이루어져 있으며, 유기물들은 무기물에서 자연적으로 형성된 것으로 보고있는 현재까지의 과학적 연구[2,3,4]에 따라 생각해보자면, 애초에 무기물이 없다면 "생명"도 있을 것 같지 않은데, 이렇게 본다면 무기물도 "생명"이라 해야 할까? 적어도 아직까지는 어디서부터가 생명이고 어디까지가 생명이 아닌지를 명확히 구분하지 못하고 있는데, 이는 AI(인공지능)도 마찬가지인 것 같다.

<div style="text-align: center;">
  <img src="https://github.com/user-attachments/assets/1728d940-1567-4269-8d0e-6af4b1b5daa1"><br>
  그림출처: Prebiotic Soup--Revisiting the Miller Experiment[3]<br>  
</div>
<br><br>

인공지능이 무엇인지를 정의하려면, 우선 '지능'에 대한 정의가 선행되어야 할 것이다. 그러나, 아직은 학문적 관점과 철학적 관점에 따라 '지능'을 여러가지로 정의하고 있는 형편이다 보니, 여기서는 위키피디아의 정의와 같이, 인공지능이란 인간의 학습능력, 추론능력, 지각능력을 인공적으로 구현하려는 컴퓨터 과학의 세부분야 중 하나[5]로 보고자 한다.



<hr>
참고문헌:

- [1] [MIT Deep Learning Book (beautiful and flawless PDF version)](https://github.com/janishar/mit-deep-learning-book-pdf/blob/master/complete-book-bookmarked-pdf/deeplearningbook.pdf)
- [2] [A Production of Amino Acids Under Possible Primitive Earth Conditions](https://www.science.org/doi/10.1126/science.117.3046.528)
- [3] [Prebiotic Soup--Revisiting the Miller Experiment](https://www.science.org/doi/10.1126/science.1085145)
- [4] [On the origins of cells: a hypothesis for the evolutionary transitions from abiotic geochemistry to chemoautotrophic prokaryotes, and from prokaryotes to nucleated cells](https://pubmed.ncbi.nlm.nih.gov/12594918/)
- [5] [위키피디아 - 인공지능](https://ko.wikipedia.org/wiki/%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5)
  
