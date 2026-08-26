# 💡 uv 환경 세팅 이후 실전 사용 가이드

초기 세팅(uv sync)이 끝난 이후, 실제로 프로젝트를 진행하면서 패키지를 추가하거나 삭제할 때, 그리고 작성한 코드를 실행할 때 사용하는 가이드입니다.

---

## 1. 패키지(라이브러리) 추가 및 삭제

프로젝트를 진행하다가 새로운 패키지(예: seaborn, xgboost)가 필요해진 경우, 절대 pip install을 사용하지 마세요!

* **✅ 올바른 패키지 추가 방법**: 
  `ash
  uv add seaborn xgboost
  `
  명령어를 치면 패키지가 설치됨과 동시에 pyproject.toml과 uv.lock 파일에 버전 정보가 자동으로 기록됩니다. 
  (이후 변경된 이 두 파일을 Git에 Commit & Push 하시면 다른 팀원들도 uv sync 한 줄로 똑같이 패키지를 설치할 수 있습니다.)

* **✅ 패키지 삭제 방법**:
  `ash
  uv remove 패키지명
  `

---

## 2. VSCode에서 Jupyter Notebook(.ipynb) 사용하기

우리 프로젝트는 이제 main_analysis.py 대신 **main_analysis.ipynb** 주피터 노트북 파일 하나만 사용하여 직관적으로 분석을 진행합니다.

1. VSCode에서 main_analysis.ipynb 파일을 엽니다.
2. 우측 상단(또는 셀 실행 시 뜨는 팝업)에서 **Select Kernel (커널 선택)** 을 클릭합니다.
3. **Python Environments** 를 누르고, 목록에서 방금 uv가 만들어준 **.venv** 가상환경을 선택합니다. (경로 끝에 .venv/Scripts/python.exe라고 적힌 것을 고르시면 됩니다.)
4. 이제 모든 패키지가 정상적으로 로드되며, 노트북 셀(Cell)을 마음껏 실행(Shift+Enter)하실 수 있습니다!

---

## 3. 다른 팀원이 패키지를 추가해서 Git에 올렸을 때

팀원이 uv add로 새로운 패키지를 추가하고 GitHub에 Push했다면, 내 컴퓨터 환경도 업데이트해야 합니다.

1. 먼저 최신 코드를 땡겨옵니다.
   `ash
   git pull origin main
   `
2. 변경된 락 파일(uv.lock)을 바탕으로 내 가상환경을 동기화시킵니다.
   `ash
   uv sync
   `
3. 이제 팀원이 추가한 패키지가 내 컴퓨터에도 완벽하게 동일한 버전으로 설치됩니다.
