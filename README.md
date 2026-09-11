# CS2Fixes Mapping Launcher

[zer0k-z/cs2kz-mapping](https://github.com/zer0k-z/cs2kz-mapping)을 ZE 맵 제작·테스트용으로 수정한 Windows 런처입니다.

A Windows launcher adapted from [zer0k-z/cs2kz-mapping](https://github.com/zer0k-z/cs2kz-mapping) for Zombie Escape map creation and testing.

<details open>
<summary><strong>🇰🇷 한국어</strong></summary>

## 설치 버전

| 구성 요소 | 버전 |
| --- | --- |
| Metamod:Source | `2.0.0-dev+1403` — Windows |
| CS2Fixes | `v1.20.1` — Source2ZE 공식 Windows 배포판 |

## 준비 사항

- Windows
- Steam, CS2 및 **CS2 Workshop Tools** DLC
- **Python 3.10 이상** (`py` 명령 사용 가능)
- **Git** — Python의 VDF 의존성 설치에 필요
- **Windows 개발자 모드** 또는 **관리자 권한 터미널** — 임시 심볼릭 링크 생성에 필요

설치 및 런처 실행 전에는 **CS2와 Workshop Tools를 종료**하세요.

## 사용법

### 1. 최초 설치

저장소를 내려받아 압축을 풀거나 Git으로 복제한 뒤, **`setup.py`가 있는 폴더에서** 명령 프롬프트 또는 PowerShell을 열고 실행합니다.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe setup.py
```

CS2 설치 위치는 Steam 정보에서 자동으로 찾습니다. Metamod와 CS2Fixes는 CS2의 `game/csgo`에 설치됩니다.

- 기존 CS2Fixes 설정 파일은 유지합니다. 새 설정 파일은 공식 배포판의 기본값을 사용합니다.
- 교체되는 기존 패키지 파일은 런처 폴더의 `backups/`에 백업합니다.
- 기존에 설치된 다른 Metamod 플러그인은 자동으로 끄거나 제거하지 않습니다.
- 설치 과정에서는 FGD, 파티클 편집기, CSM 및 `gameinfo.gi` 설정을 변경하지 않습니다.

### 2. Hammer 실행

설치 이후에는 같은 폴더에서 다음 명령만 실행하면 됩니다.

```powershell
.\.venv\Scripts\python.exe run-mapping.py
```

1. Workshop Tools 창에서 작업할 애드온을 선택합니다.
2. Hammer를 열어 맵을 편집·실행합니다.
3. 런처의 로딩 확인과 원본 파일 복구가 끝날 때까지 터미널을 닫지 마세요.

런처는 `-insecure -gpuraytracing` 옵션을 사용합니다. 공식 매치메이킹용 실행 방식이 아닙니다.

### 3. 플러그인 확인

맵 실행 후 **게임 콘솔**에 입력합니다.

```text
meta version
meta list
```

Metamod 버전이 `2.0.0-dev+1403`인지, CS2Fixes가 정상 로드되었는지 확인하세요. 런처의 DLL 감지는 플러그인 초기화 성공까지 보장하지 않습니다.

## CS2Fixes 설정 적용

CS2 설치 폴더의 다음 파일을 편집합니다.

```text
game/csgo/cfg/cs2fixes/cs2fixes.cfg
```

플러그인은 로딩 시 이 파일을 자동으로 읽습니다. 실행 중 수정한 내용을 다시 적용하려면 **게임 콘솔**에서 입력하세요.

```text
exec_custom cs2fixes/cs2fixes
```

**`.cfg` 확장자는 붙이지 않습니다.** ZE 기능은 자동으로 켜지지 않으므로 [CS2Fixes 위키](https://github.com/Source2ZE/CS2Fixes/wiki)를 참고해 설정하세요.

## 문제 해결

### `WinError 1314` / 심볼릭 링크 권한 오류

Windows 설정에서 **개발자 모드**를 켜거나, 터미널을 **관리자 권한으로 실행**한 뒤 런처 폴더로 이동해 `run-mapping.py`를 다시 실행하세요. `setup.py`부터 재설치할 필요는 없습니다.

### CS2 경로를 찾지 못하는 경우

자동 검색 대신 설치 경로를 지정할 수 있습니다. 아래 자리표시자는 실제 경로로 바꾸세요.

```powershell
.\.venv\Scripts\python.exe setup.py --cs2-path "<CS2 설치 폴더>"
.\.venv\Scripts\python.exe run-mapping.py --cs2-path "<CS2 설치 폴더>"
```

지정한 폴더 아래에 `game/bin/win64/cs2.exe`가 있어야 합니다.

**`verify.py`는 일반 설치·실행에 필요하지 않습니다.** 기존 `gameinfo.gi`를 덮어쓰므로 사용 전 백업하세요.

</details>

<details>
<summary><strong>🇬🇧 English</strong></summary>

## Package versions

| Component | Version |
| --- | --- |
| Metamod:Source | `2.0.0-dev+1403` — Windows |
| CS2Fixes | `v1.20.1` — official Source2ZE Windows release |

## Requirements

- Windows
- Steam, CS2, and the **CS2 Workshop Tools** DLC
- **Python 3.10+**, with the `py` command available
- **Git**, required to install the Python VDF dependency
- **Windows Developer Mode** or an **administrator terminal**, required for temporary symlinks

**Close CS2 and Workshop Tools** before installation or launching.

## Usage

### 1. Initial setup

Download and extract the repository, or clone it with Git. Open Command Prompt or PowerShell **in the folder containing `setup.py`**, then run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe setup.py
```

The CS2 installation is detected from Steam. Metamod and CS2Fixes are installed into CS2's `game/csgo` directory.

- Existing CS2Fixes configuration files are preserved. New configs use official package defaults.
- Replaced package files are backed up to `backups/` in the launcher folder.
- Other installed Metamod plugins are not automatically disabled or removed.
- Setup does not change FGD, particle editor, CSM, or `gameinfo.gi` settings.

### 2. Launch Hammer

After setup, run only this command from the same folder:

```powershell
.\.venv\Scripts\python.exe run-mapping.py
```

1. Select the addon in the Workshop Tools launcher.
2. Open Hammer to edit and run the map.
3. Keep the terminal open until the launcher finishes checking the DLL and restoring the original files.

The launcher uses `-insecure -gpuraytracing`. It is not intended for official matchmaking.

### 3. Verify plugin loading

After running the map, enter these commands in the **game console**:

```text
meta version
meta list
```

Confirm Metamod reports `2.0.0-dev+1403` and CS2Fixes is loaded successfully. DLL detection by the launcher does not guarantee successful plugin initialization.

## Applying CS2Fixes settings

Edit this file inside the CS2 installation:

```text
game/csgo/cfg/cs2fixes/cs2fixes.cfg
```

The plugin automatically reads it when loading. To reapply edits during a running session, enter this in the **game console**:

```text
exec_custom cs2fixes/cs2fixes
```

**Do not include the `.cfg` extension.** ZE features are not automatically enabled; configure them using the [CS2Fixes wiki](https://github.com/Source2ZE/CS2Fixes/wiki).

## Troubleshooting

### `WinError 1314` / symlink permission error

Enable **Developer Mode** in Windows Settings, or open a terminal **as Administrator**, navigate to the launcher folder, and run `run-mapping.py` again. You do not need to repeat installation with `setup.py`.

### CS2 installation not found

Specify the installation directory manually. Replace the placeholder with the actual path:

```powershell
.\.venv\Scripts\python.exe setup.py --cs2-path "<CS2 installation directory>"
.\.venv\Scripts\python.exe run-mapping.py --cs2-path "<CS2 installation directory>"
```

The selected directory must contain `game/bin/win64/cs2.exe`.

**`verify.py` is not needed for normal setup or launching.** It overwrites existing `gameinfo.gi` files, so back them up before use.

</details>

## Credits

- Original launcher / 원본 런처: [zer0k-z/cs2kz-mapping](https://github.com/zer0k-z/cs2kz-mapping)
- Plugin / 플러그인: [Source2ZE/CS2Fixes](https://github.com/Source2ZE/CS2Fixes)
- Plugin loader / 플러그인 로더: [AlliedModders Metamod:Source](https://github.com/alliedmodders/metamod-source)
