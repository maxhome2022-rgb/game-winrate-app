# 🎮 게임 플레이 시간에 따른 승률 예측

게임 플레이 시간을 슬라이더로 선택하면 예상 승률을 보여주는 데이터 분석 웹앱입니다.
Python과 Streamlit으로 만들었습니다.

## 주요 기능

- 게임 플레이 시간 입력 슬라이더
- 예상 승률 출력 (숫자 + 진행 막대)
- 실제 데이터 산점도 (플레이 시간 vs 승률)

## 사용한 데이터

- [Call of Duty Players Skills (Kaggle)](https://www.kaggle.com/datasets/aishahakami/call-of-duty-players) → `cod.csv`
- 승률 = `wins / (wins + losses) × 100`
- 경기 수가 20회 이상인 플레이어 728명만 사용 (경기 수가 적으면 승률이 불안정함)

## 예측 방식

승률은 플레이 시간이 늘수록 점점 완만하게 오르기 때문에,
플레이 시간에 로그(`log1p`)를 취한 뒤 직선 회귀(`numpy.polyfit`)로 학습합니다.

## 실행 방법

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 배포 (Streamlit Community Cloud)

1. 이 저장소를 GitHub에 올립니다.
2. [share.streamlit.io](https://share.streamlit.io)에서 GitHub 계정으로 로그인합니다.
3. 저장소를 선택하고 Main file path를 `app.py`로 지정한 뒤 Deploy 합니다.

## 바이브 코딩 프롬프트

> 게임 플레이 시간에 따른 승률을 예측하는 데이터 분석 웹앱을 만들고 싶어. Python과 Streamlit을 활용하여 웹앱의 기본 화면을 만들어줘. 제목은 '게임 플레이 시간에 따른 승률 예측'으로 설정하고, 게임 플레이 시간을 입력할 수 있는 슬라이더와 예상 승률을 출력하는 영역을 만들어줘.

## 참고 및 한계

- 플레이 시간만으로 설명되는 승률은 약 34%(R² ≈ 0.34)입니다. 개인별 정확한 예측이 아니라 데이터의 경향을 보여주는 용도입니다.
- 이 데이터의 승률은 중앙값이 약 94%로 매우 높아서, 일반적인 매치 승률과는 다를 수 있습니다.
- `timePlayed`의 단위는 Kaggle 설명에 따라 '시간'으로 표시했습니다. 다르다면 `app.py`의 `TIME_UNIT`을 수정하세요.
