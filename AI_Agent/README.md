# AI Agent란?


## 용어 정리

|용어|설명|
|:-|:-|
|Chain-of-thought prompting<br>(사고 흐름 유도 프롬프트)|복잡한 문제를 해결할 때 AI가 중간 사고 과정을 단계별로 표현하도록 유도하는 방법<br>  - AI가 더 정확하고 신뢰할 수 있는 결과를 얻기 위해, 단순히 정답만 내놓는 것이 아니라, 사고의 흐름을 따라가며 단계별로 추론하도록 유도하는 전략 |
|Prompting (프롬프트 작성)|AI에게 특정 방식으로 질문하거나 지시하여 원하는 응답을 유도하는 기술|
|Natural Language Explanation|AI가 단순한 정답만 알려주는 것이 아니라, 그 이유나 과정을 자연어로 설명하도록 하는 방식|
|Program synthesis/execution|프로그램 생성 및 실행. 문제 해결을 위해 코드나 알고리즘을 생성하고 실행하는 것|
|Numeric and logical reasoning|수치 및 논리적 추론. 수학적 계산이나 논리적 판단을 요구하는 문제 해결 능력|
|Intermediate Language Steps|중간 언어 단계. 최종 답을 도출하기 전에 중간 단계의 언어적 표현을 통해 사고 과정을 드러내는 방식|

<br>

## AI Agent(자율 시스템)의 필수 구성 요소 [[1]](#ref_1)

  <img width="995" height="500" alt="image" src="https://github.com/user-attachments/assets/4e9ff736-b885-4443-9142-a74d92a26c5f" />

  - The Model(Brain): 핵심 언어 모델(LM) 또는 기반 모델은 에이전트의 중심 추론 엔진 역할을 하며, 정보를 처리하고, 선택지를 평가하며, 결정을 내임. 모델의 유형(범용, 미세 조정된 모델, 멀티모달 모델 등)은 에이전트의 인지 능력을 결정함.
  
  - Tools(The "Hands"): 외부 서비스와 연결해 정보를 가져오거나 명령을 실행하는 API, 계산이나 분석 또는 이미지 생성 등 다양한 기능을 수행하는 코드 함수, 실시간 정보나 과거 데이터를 검색하기 위한 데이터 저장소로의 접근 등을 실행함으로써 실시간 사실 기반 정보에 접근하는 도구.

    - 언어 모델이 어떤 도구를 사용할지를 계획한 후, 그 도구를 실행하여 얻은 결과를 다음 언어 모델 호출 시 입력 컨텍스트에 포함시켜 더 나은 판단을 가능하게 함.
  
  - Orchestration Layer: 에이전트의 작동 루프를 관리하는 통제 프로세스. 계획 수립, 메모리(상태)관리, 추론 전략 실행 담당. Chain-Of-Thought나 ReAct와 같은 프롬프트 프레임워크와 추론 기법을 활용하여 복잡한 목표를 단계별로 나누고, 언제 사고할지와 언제 도구를 사용할지를 결정함. 또한 이 계층은 에이전트가 '기억'할 수 있도록 메모리 기능을 제공.
    
    - Chain-Of-Thought(CoT): 복잡한 문제를 단계적으로 사고하는 방식
    - ReAct: 사고(Reasoning)와 행동(Action)을 번갈아 수행하는 방식


<br>

# 참고문헌

[1] <a id="ref_1"></a> [Introduction to Agents](https://drive.google.com/file/d/1C-HvqgxM7dj4G2kCQLnuMXi1fTpXRdpx/view)


# 추가 자료
[Agent Development Kit](https://google.github.io/adk-docs/agents/)
  - [Sequential Agents in ADK](https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/)
  - [Parallel Agents in ADK](https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/)
  - [Lopo Agents in ADK](https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/)
