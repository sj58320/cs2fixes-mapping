# CS2Fixes Mapping Launcher

[zer0k-z/cs2kz-mapping](https://github.com/zer0k-z/cs2kz-mapping)을 ZE 맵 제작·테스트용으로 수정한 Windows 런처입니다.

A Windows launcher adapted from [zer0k-z/cs2kz-mapping](https://github.com/zer0k-z/cs2kz-mapping) for Zombie Escape map creation and testing.

<details open>
<summary><strong>🇰🇷 한국어</strong></summary>

## 설치 버전

| 구성 요소 | 버전 |
| --- | --- |
| Metamod:Source | `2.0.0-dev+1472` — Windows |
| CS2Fixes | `v2.0` — Source2ZE 공식 Windows 배포판 (KHook 기반) |

## 준비 사항

- Windows, Steam, CS2
- **CS2 Workshop Tools** DLC — Steam 라이브러리에서 CS2 우클릭 → **속성** → **DLC** → **Counter-Strike 2 Workshop Tools** 체크

설치 및 실행 전에는 **CS2와 Workshop Tools를 종료**하세요.

## 사용법

### 1. 내려받기

[Releases](https://github.com/sj58320/cs2fixes-mapping/releases/latest)의 **Assets**에서 `setup.exe`와 `run-mapping.exe`를 받아 **같은 폴더**에 둡니다. CS2 설치 폴더 밖의 전용 폴더를 권장합니다.

코드 서명이 없는 실행 파일이라 **Windows의 PC 보호**(SmartScreen) 창이 뜨면 **추가 정보** → **실행**을 누르세요. 백신이 오탐할 수 있으며, 파일 해시는 `SHA256SUMS.txt`로 확인할 수 있습니다.

### 2. 설치 — `setup.exe`

처음 한 번, 그리고 새 버전을 받았을 때 실행합니다. `Setup complete.`가 나오면 Enter로 닫습니다.

- Metamod와 CS2Fixes를 CS2의 `game/csgo`에 설치합니다. CS2 위치는 Steam 정보에서 자동으로 찾습니다.
- 기존 CS2Fixes 설정 파일은 유지합니다. 새 설정 파일은 공식 배포판의 기본값을 사용합니다.
- 교체되는 기존 파일은 exe 폴더의 `backups/<설치 시각(UTC)>/`에 백업합니다. 이전 버전으로 되돌리려면 그 안의 `addons` 폴더를 CS2의 `game/csgo`에 덮어쓰세요. 필요 없으면 지워도 됩니다.
- 다른 Metamod 플러그인, FGD, 파티클 편집기, CSM, `gameinfo.gi`는 건드리지 않습니다.

### 3. Hammer 실행 — `run-mapping.exe`

**매번 이 exe로 Workshop Tools를 여세요.** Steam에서 바로 열면 CS2Fixes가 로드되지 않습니다.

1. `run-mapping.exe`를 실행하고 관리자 권한 요청에 **예**를 누릅니다.
2. Workshop Tools 창에서 애드온을 고르고 **Launch Tools**를 누릅니다.
3. 로딩이 끝날 때까지 검은 창을 닫지 마세요. 다음이 나오면 Enter로 닫아도 됩니다. 게임과 Hammer는 계속 실행됩니다.

```text
CS2Fixes DLL detected. Confirm successful initialization with: meta list
Original gameinfo files restored.
```

런처는 CS2가 시작되는 동안만 `gameinfo.gi`에 Metamod 경로를 넣고, 로딩이 끝나면 원본으로 되돌립니다. `-insecure -gpuraytracing` 옵션으로 실행되므로 매치메이킹에는 사용할 수 없습니다.

### 4. 플러그인 확인

맵 실행 후 **게임 콘솔**에 입력합니다.

```text
meta version
meta list
```

Metamod가 `2.0.0-dev+1472`이고 CS2Fixes가 정상 로드되었는지 확인하세요. 런처의 DLL 감지는 플러그인 초기화 성공까지 보장하지 않습니다.

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

| 메시지 | 해결 |
| --- | --- |
| `Close CS2 and Workshop Tools...` | 작업 관리자에서 `cs2.exe`까지 종료한 뒤 다시 실행 |
| `Missing csgocfg.exe` | Workshop Tools DLC 설치 |
| `Missing cs2fixes.dll` | `setup.exe` 먼저 실행 |
| `CS2Fixes DLL was not detected` | 게임을 끄고 다시 시도. `gameinfo.gi`는 자동으로 복구됨 |
| `A gameinfo_cs2fixes_original.gi backup remains` | 이전 실행이 중간에 끊긴 경우. `game/csgo`, `game/csgo_core`의 `gameinfo_cs2fixes_original.gi`를 지우고 Steam에서 **게임 파일 무결성 확인** |

### CS2 경로를 찾지 못하는 경우

exe 폴더의 주소창에 `powershell`을 입력해 연 뒤, 설치 경로를 직접 지정합니다. 자리표시자는 실제 경로로 바꾸세요.

```powershell
.\setup.exe --cs2-path "<CS2 설치 폴더>"
.\run-mapping.exe --cs2-path "<CS2 설치 폴더>"
```

지정한 폴더 아래에 `game/bin/win64/cs2.exe`가 있어야 합니다.

<details>
<summary><strong>Python으로 직접 실행 (선택)</strong></summary>

exe 대신 소스를 실행하려면 Python 3.10 이상과 Git이 필요합니다. 저장소 폴더에서:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe setup.py
```

이후에는 `run-mapping.cmd`를 실행합니다. 관리자 권한으로 `run-mapping.py`를 실행해 줍니다. exe 사용법의 `--cs2-path` 옵션도 동일하게 쓸 수 있습니다.

`verify.py`는 일반 설치·실행에 필요하지 않습니다. 기존 `gameinfo.gi`를 백업 없이 덮어쓰므로 사용 전 백업하세요.

</details>

<details>
<summary><strong>새 버전 배포 (관리자용)</strong></summary>

`setup.py`의 `PACKAGES` URL·SHA-256과 이 문서의 버전을 수정해 커밋한 뒤, annotated 태그를 푸시하면 GitHub Actions가 exe를 빌드해 릴리즈를 만듭니다. 태그 메시지가 릴리즈 노트가 됩니다.

```powershell
git tag -a v1.0.1 -m "릴리즈 노트"
git push origin v1.0.1
```

</details>

</details>

<details>
<summary><strong>🇬🇧 English</strong></summary>

## Package versions

| Component | Version |
| --- | --- |
| Metamod:Source | `2.0.0-dev+1472` — Windows |
| CS2Fixes | `v2.0` — official Source2ZE Windows release (KHook-based) |

## Requirements

- Windows, Steam, CS2
- **CS2 Workshop Tools** DLC — in the Steam library, right-click CS2 → **Properties** → **DLC** → check **Counter-Strike 2 Workshop Tools**

**Close CS2 and Workshop Tools** before installation or launching.

## Usage

### 1. Download

Download `setup.exe` and `run-mapping.exe` from **Assets** on [Releases](https://github.com/sj58320/cs2fixes-mapping/releases/latest) into **the same folder**, preferably a dedicated folder outside the CS2 installation.

The executables are unsigned. If **Windows protected your PC** (SmartScreen) appears, click **More info** → **Run anyway**. Antivirus false positives may occur; verify hashes with `SHA256SUMS.txt`.

### 2. Install — `setup.exe`

Run it once, and again after downloading a new release. Press Enter to close after `Setup complete.`

- Installs Metamod and CS2Fixes into CS2's `game/csgo`. The CS2 installation is detected from Steam.
- Existing CS2Fixes configuration files are preserved. New configs use official package defaults.
- Replaced files are backed up to `backups/<install time (UTC)>/` next to the executables. To roll back, copy its `addons` folder over CS2's `game/csgo`. Delete it when no longer needed.
- Other Metamod plugins, FGD, particle editor, CSM, and `gameinfo.gi` are not modified.

### 3. Launch Hammer — `run-mapping.exe`

**Always open Workshop Tools through this executable.** Launching directly from Steam does not load CS2Fixes.

1. Run `run-mapping.exe` and accept the administrator prompt.
2. Select the addon in the Workshop Tools launcher and click **Launch Tools**.
3. Keep the console window open until loading finishes. Once the following appears, press Enter to close it; the game and Hammer keep running.

```text
CS2Fixes DLL detected. Confirm successful initialization with: meta list
Original gameinfo files restored.
```

The launcher adds the Metamod path to `gameinfo.gi` only while CS2 starts, then restores the original. It runs with `-insecure -gpuraytracing`, so it cannot be used for matchmaking.

### 4. Verify plugin loading

After running the map, enter these commands in the **game console**:

```text
meta version
meta list
```

Confirm Metamod reports `2.0.0-dev+1472` and CS2Fixes is loaded successfully. DLL detection by the launcher does not guarantee successful plugin initialization.

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

| Message | Fix |
| --- | --- |
| `Close CS2 and Workshop Tools...` | End `cs2.exe` in Task Manager, then retry |
| `Missing csgocfg.exe` | Install the Workshop Tools DLC |
| `Missing cs2fixes.dll` | Run `setup.exe` first |
| `CS2Fixes DLL was not detected` | Close the game and retry; `gameinfo.gi` is restored automatically |
| `A gameinfo_cs2fixes_original.gi backup remains` | A previous run was interrupted. Delete `gameinfo_cs2fixes_original.gi` in `game/csgo` and `game/csgo_core`, then **Verify integrity of game files** in Steam |

### CS2 installation not found

Type `powershell` into the address bar of the executables' folder, then specify the installation directory. Replace the placeholder with the actual path:

```powershell
.\setup.exe --cs2-path "<CS2 installation directory>"
.\run-mapping.exe --cs2-path "<CS2 installation directory>"
```

The selected directory must contain `game/bin/win64/cs2.exe`.

<details>
<summary><strong>Running from Python source (optional)</strong></summary>

Running the source instead of the executables requires Python 3.10+ and Git. In the repository folder:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe setup.py
```

Afterwards, run `run-mapping.cmd`, which launches `run-mapping.py` as Administrator. The `--cs2-path` option works the same way.

`verify.py` is not needed for normal setup or launching. It overwrites existing `gameinfo.gi` files without a backup, so back them up first.

</details>

<details>
<summary><strong>Publishing a new version (maintainers)</strong></summary>

Update the `PACKAGES` URLs and SHA-256 values in `setup.py` and the versions in this document, commit, then push an annotated tag. GitHub Actions builds the executables and creates the release; the tag message becomes the release notes.

```powershell
git tag -a v1.0.1 -m "Release notes"
git push origin v1.0.1
```

</details>

</details>

## Credits

- Original launcher / 원본 런처: [zer0k-z/cs2kz-mapping](https://github.com/zer0k-z/cs2kz-mapping)
- Plugin / 플러그인: [Source2ZE/CS2Fixes](https://github.com/Source2ZE/CS2Fixes)
- Plugin loader / 플러그인 로더: [AlliedModders Metamod:Source](https://github.com/alliedmodders/metamod-source)
