# 📄 PRD: 구독허브 AI 챗봇 시스템 구축

## 1. 📌 프로젝트 개요

- **목적**: 구독 상품 관련 사용자 문의에 자연어 기반으로 대응하고, 사용자 구독 이력과 외부 후기 데이터 등을 기반으로 개인화된 상담 및 상품 추천이 가능한 AI 챗봇 개발
- **대상 플랫폼**: 구독허브 웹/앱
- **지원 언어**: 한국어 (PoC 단계)

---

## 2. 🧩 전체 아키텍처 구성

1. **데이터 확보 계층**

   - 내부: 사용자 구독 상태, 결제 이력, 상품 메타데이터
   - 외부: 웹 크롤링 통해 후기, 뉴스, 가격정보 수집

2. **NLU 계층**

   - 사용자 질문 intent 분류기
   - 질의 유형별 응답 시나리오 및 룰 매핑
   - LLM 기반 fallback 응답

3. **응답 생성 계층**

   - Rule 기반 응답 처리기
   - LLM 응답 생성기 (context injection 포함)
   - 사용자 맥락 기반 응답 보정기

4. **챗봇 UI 계층**

   - 웹/앱 연동 REST API
   - 프론트에서 질문 전송 및 답변 렌더링

---

## 3. 📂 데이터 확보 계획

### 3.1 구독 상품 후기 수집

- **대상**: 티스토리, 블로그, 커뮤니티, 위키 등
- **도구**:
  - `BeautifulSoup`, `Scrapy` 기반 크롤러
  - `Python` + `Lambda` + `CloudWatch Event` + `S3` 저장
- **형식**:

```json
{
  "title": "넷플릭스 요금제 후기",
  "content": "...",
  "source": "티스토리",
  "published_at": "2024-08-01"
}
```

### 3.2 상품 메타데이터 tagging

- **도구**: `spaCy` NER + 사용자 정의 엔티티
- **예시 태그**:

```
[상품명: Disney+], [가격: 11,000원], [혜택: 첫달 무료]
```

---

## 4. 🤖 자연어 처리 구성

### 4.1 Intent 분류기

- **모델 후보**:
  - baseline: `TF-IDF + Logistic Regression`
  - 발전형: `KoBERT`, `KoMiniLM` fine-tuning
- **데이터**:
  - 수집된 사용자 질문 유형에 대해 intent label 부여
- **예시**:

```json
{
  "question": "넷플릭스 해지는 어떻게 해요?",
  "intent": "해지_방법"
}
```

### 4.2 Intent 분류 항목 예시

| intent | 예시 질문                            |
| ------ | ------------------------------------ |
| 조회   | "내 구독 목록 알려줘"                |
| 비교   | "넷플릭스랑 디즈니플러스 뭐가 달라?" |
| 추천   | "가성비 좋은 OTT 뭐 있어?"           |
| 해지   | "유튜브 프리미엄 해지하고 싶어요"    |
| 고민   | "계속 써야 할지 고민이에요"          |

---

## 5. 🛠 응답 생성 로직

### 5.1 Rule 기반 응답 시스템

- **트리거 조건**: intent가 rule에 정의된 경우
- **데이터 소스**: PostgreSQL / Elasticsearch
- **예시**:

```sql
SELECT * FROM subscription_history WHERE user_id = :user_id AND status = 'active';
```

### 5.2 LLM 기반 응답 (Fallback or Open 질문 대응)

- **모델 후보**:
  - 사내 배포 가능 시: `KoAlpaca`, `KoLLM`, `Ollama`
  - 클라우드 LLM 옵션: OpenAI GPT, Anthropic Claude (PoC 용도)
- **Prompt 예시**:

```
사용자 질문: "유튜브 프리미엄 계속 쓸만해?"
사용자 상태: 최근 3개월 결제 유지 중, 할인 이벤트 없음

[질문에 대해 조언해주세요.]
```

### 5.3 Context Embedding

- **구성요소**:
  - 구독 상품 목록, 상태, 최근 결제금액, 과거 질문 기록
- **개인화 처리 방법**:
  - context vector 생성 → prompt에 injection
  - masking 처리로 개인정보 제외

---

## 6. 📊 후기 요약/감성분석

### 6.1 후기 요약

- **모델**: `pegasus-ko`, `kobart` fine-tune
- **입력**: 장문 후기 텍스트
- **출력**: 핵심만 추린 3\~4줄 요약문

### 6.2 감성분석

- **모델**: `klue/bert-base`
- **레이블**: 긍정 / 부정 / 중립

---
## 7. 🧪 테스트 계획

### 7.1 Intent 분류 테스트

- **테스트셋**: 300건 이상 사용자 질문 수작업 라벨링
- **지표**: Accuracy, Precision, Recall, F1

### 7.2 전체 시나리오 테스트

- **시나리오 기반 테스트**:
  - 대표 질문 유형별 시나리오 20종 이상
- **Fallback 비율 측정**
- **Confusion Matrix 생성**

---

## 8. 📆 일정안 (예시)

| 기간         | 주요 작업 내용                         |
| ------------ | -------------------------------------- |
| 8/5 \~ 8/9   | 크롤링 및 메타데이터 수집기 구성       |
| 8/12 \~ 8/16 | intent 분류기 v1 학습 + 시나리오 정의  |
| 8/19 \~ 8/23 | rule 기반 응답 로직 구현               |
| 8/26 \~ 9/6  | LLM 연동 + context embedding 응답 설계 |
| 9/9 \~ 9/13  | 테스트셋 구성 + 평가                   |
| 9/16         | PoC 완료 및 보고서 작성                |

---

## 9. 🧱 기술 스택

- **언어**: Python, SQL, Shell
- **라이브러리**: Transformers, scikit-learn, spaCy, scrapy
- **서버/인프라**: AWS Lambda, S3, CloudWatch, ECS
- **DB**: PostgreSQL
- **LLM 연동**: Huggingface, Ollama (또는 OpenAI API)

---

## 10. ✅ 구현 우선순위 (PoC)

1. 사용자 질문 intent 분류기 구축 및 시나리오 정의
2. Rule 기반 응답 모듈 개발
3. 후기 크롤링기 + 감성/요약 분석기
4. LLM 연동 fallback 응답
5. 사용자 context 반영 응답 생성

