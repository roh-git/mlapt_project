# 🚀 프로젝트 환경 세팅 & 사용 가이드 (with uv)

본 프로젝트는 의존성(패키지) 충돌을 방지하고 모든 팀원이 **동일하고 완벽한 환경**에서 작업할 수 있도록 최신 패키지 매니저인 **uv**를 기반으로 세팅되어 있습니다.

pyproject.toml과 uv.lock 파일이 이미 리포지토리에 구성되어 있으므로, 복잡한 pip install 없이 아래 명령어 한 줄이면 자동으로 가상환경이 생성되고 패키지가 설치됩니다!

---

## 💻 초기 세팅 방법 (최초 1회)

### 1. uv 설치하기 (아직 없는 경우)

본인의 컴퓨터에 uv가 없다면 먼저 아래 명령어로 설치해주세요.

- **Windows (PowerShell)**: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **macOS / Linux**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **또는 pip 사용**: `pip install uv`

### 2. 프로젝트 최신화 및 환경 동기화

GitHub에서 코드를 당겨온(pull) 후, 프로젝트 최상단 폴더(이 파일이 있는 위치)에서 아래 명령어를 실행하세요.

```bash
uv sync
```

✨ **끝입니다!** ✨
uv sync 명령어를 치면 알아서 .venv라는 격리된 가상환경이 생성되고, uv.lock에 명시된 버전과 토씨 하나 틀리지 않는 완벽히 동일한 라이브러리들이 빛의 속도로 설치됩니다.

### 3. VSCode에서 인터프리터 선택

패키지가 설치된 후, VSCode 우측 하단이나 커맨드 팔레트(Ctrl+Shift+P)에서 **Python: Select Interpreter**를 클릭하여 폴더 안에 생성된 **.venv**를 선택해주시면 완벽하게 자동완성과 실행이 연동됩니다. (경로 끝에 `.venv/Scripts/python.exe`라고 적힌 것을 고르시면 됩니다.)

### 4. VSCode에서 Jupyter Notebook(.ipynb) 사용하기

우리 프로젝트는 **main_analysis.ipynb** 주피터 노트북 파일 하나만 사용하여 직관적으로 분석을 진행합니다.

1. VSCode에서 main_analysis.ipynb 파일을 엽니다.
2. 우측 상단(또는 셀 실행 시 뜨는 팝업)에서 **Select Kernel (커널 선택)** 을 클릭합니다.
3. **Python Environments** 를 누르고, 목록에서 방금 uv가 만들어준 **.venv** 가상환경을 선택합니다.
4. 이제 모든 패키지가 정상적으로 로드되며, 노트북 셀(Cell)을 마음껏 실행(Shift+Enter)하실 수 있습니다!

---

## 🛠️ 작업 시 참고사항

### 패키지(라이브러리) 추가 및 삭제

프로젝트를 진행하다가 새로운 패키지(예: seaborn, xgboost)가 필요해진 경우, **절대 pip install을 사용하지 마세요!**

- **✅ 올바른 패키지 추가 방법**:
  ```bash
  uv add seaborn xgboost
  ```
  명령어를 치면 패키지가 설치됨과 동시에 pyproject.toml과 uv.lock 파일에 버전 정보가 자동으로 기록됩니다.
  (이후 변경된 이 두 파일을 Git에 Commit & Push 하시면 다른 팀원들도 uv sync 한 줄로 똑같이 패키지를 설치할 수 있습니다.)

- **✅ 패키지 삭제 방법**:
  ```bash
  uv remove 패키지명
  ```

### 다른 팀원이 패키지를 추가해서 Git에 올렸을 때

팀원이 uv add로 새로운 패키지를 추가하고 GitHub에 Push했다면, 내 컴퓨터 환경도 업데이트해야 합니다.

1. 먼저 최신 코드를 당겨옵니다.
   ```bash
   git pull origin main
   ```
2. 변경된 락 파일(uv.lock)을 바탕으로 내 가상환경을 동기화시킵니다.
   ```bash
   uv sync
   ```
3. 이제 팀원이 추가한 패키지가 내 컴퓨터에도 완벽하게 동일한 버전으로 설치됩니다.
