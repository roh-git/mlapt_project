# 🚀 팀원들을 위한 Python 환경 초고속 세팅 가이드 (with uv)

본 프로젝트는 의존성(패키지) 충돌을 방지하고 모든 팀원이 **동일하고 완벽한 환경**에서 작업할 수 있도록 최신 패키지 매니저인 **uv**를 기반으로 세팅되어 있습니다.

pyproject.toml과 uv.lock 파일이 이미 리포지토리에 구성되어 있으므로, 복잡한 pip install 없이 아래 명령어 한 줄이면 자동으로 가상환경이 생성되고 패키지가 설치됩니다!

---

## 💻 초기 세팅 방법 (최초 1회)

### 1. uv 설치하기 (아직 없는 경우)
본인의 컴퓨터에 uv가 없다면 먼저 아래 명령어로 설치해주세요.
- **Windows (PowerShell)**: powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
- **macOS / Linux**: curl -LsSf https://astral.sh/uv/install.sh | sh
- **또는 pip 사용**: pip install uv

### 2. 프로젝트 최신화 및 환경 동기화
GitHub에서 코드를 댕겨온(pull) 후, 프로젝트 최상단 폴더(이 파일이 있는 위치)에서 아래 명령어를 실행하세요.
`ash
uv sync
`

✨ **끝입니다!** ✨
uv sync 명령어를 치면 알아서 .venv라는 격리된 가상환경이 생성되고, uv.lock에 명시된 버전과 토씨 하나 틀리지 않는 완벽히 동일한 라이브러리들이 **빛의 속도**로 설치됩니다.

---

## 🛠️ 작업 시 참고사항

* **VSCode 환경**: 패키지가 설치된 후, VSCode 우측 하단이나 커맨드 팔레트(Ctrl+Shift+P)에서 Python: Select Interpreter를 클릭하여 폴더 안에 생성된 .venv를 선택해주시면 완벽하게 자동 완성과 실행이 연동됩니다.
* **패키지 추가 설치가 필요할 때**: 그냥 pip install을 쓰지 마시고, uv add [패키지명] (예: uv add scikit-learn)을 입력하세요. 자동으로 pyproject.toml과 uv.lock이 업데이트됩니다! 업데이트된 파일은 잊지 말고 꼭 Git에 Commit & Push 해주세요!
