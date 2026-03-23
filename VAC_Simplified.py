import os
import subprocess
from datetime import datetime
from shutil import which
from pathlib import Path
import urllib.request


VRCFURY_REPO_URL = "https://vcc.vrcfury.com/"
LILTOONSHADER_REPO_URL = "https://lilxyzw.github.io/vpm-repos/vpm.json"
POIYOMISHADER_REPO_URL = "https://poiyomi.github.io/vpm/index.json"
MODULARAVATAR_REPO_URL = "https://vpm.nadena.dev/vpm.json"
AAOAVATAROPTIMIZER_REPO_URL = "https://vpm.anatawa12.com/vpm.json"
D4RKAVATAROPTIMIZER_REPO_URL = "https://d4rkc0d3r.github.io/vpm-repos/main.json"
AVATARCOMPRESSOR_REPO_URL = "https://vpm.limitex.dev/index.json"
GOGOLOCO_REPO_URL = "https://Spokeek.github.io/goloco/index.json"


print("Installing/Updating ALCOM...")

try:
	if os.name == "nt":
		subprocess.run([
			"winget",
			"install",
			"anatawa12.ALCOM",
			"--accept-package-agreements",
			"--accept-source-agreements"
		], check=True)
	else:
		Path.home().joinpath("Applications").mkdir(parents=True, exist_ok=True)
		alcom = Path.home() / "Applications" / "alcom-1.1.5-x86_64.AppImage"
		urllib.request.urlretrieve("https://github.com/vrc-get/vrc-get/releases/download/gui-v1.1.5/alcom-1.1.5-x86_64.AppImage", alcom)
		alcom.chmod(0o755)
except Exception as e:
		input(f"ERROR: Failed to install ALCOM\n{e}")
		exit(1)


print("Installing/Updating dotnet...")

try:
	if os.name == "nt":
		subprocess.run([
			"winget",
			"install",
			"Microsoft.Dotnet.SDK.8",
			"--accept-package-agreements",
			"--accept-source-agreements"
		], check=True)
	else:
		if which("apt"):
			subprocess.run(["sudo", "apt", "update"], check=True)
			subprocess.run(["sudo", "apt", "install", "-y", "dotnet-sdk-8.0"], check=True)
		elif which("dnf"):
			subprocess.run(["sudo", "dnf", "install", "-y", "dotnet-sdk-8.0"], check=True)
		elif which("pacman"):
			subprocess.run(["sudo", "pacman", "-Sy", "--noconfirm", "dotnet-sdk"], check=True)
		else:
			# manual install if package manager isnt detected
			subprocess.run("curl -fsSL https://dot.net/v1/dotnet-install.sh | bash", check=True, shell=True)
			# add to path
			dotnet_path = str(Path.home() / ".dotnet")
			bashrc = Path.home() / ".bashrc"
			if bashrc.exists():
				with open(bashrc, "a") as f:
					f.write(f'\nexport PATH="$PATH:{dotnet_path}"\n')
except Exception as e:
	if subprocess.run(["dotnet", "--version"]).returncode != 0:
		input(f"ERROR: Failed to install dotnet\n{e}")
		exit(1)

os.reload_environ()


print("Installing/Updating VRChat Package Manager...")

try:
	subprocess.run([
		"dotnet",
		"tool",
		"install",
		"--global",
		"vrchat.vpm.cli"
	], check=True)
except Exception as e:
	input(f"ERROR: Failed to install VRChat Package Manager\n{e}")
	exit(1)

os.reload_environ()


print("Installing/Updating VPM templates...")

try:
	subprocess.run([
		"vpm",
		"install",
		"templates"
	], check=True)
except Exception as e:
	input(f"ERROR: Failed to install VPM templates\n{e}")
	exit(1)


print("Installing/Updating Unity Hub...")

try:
	if os.name == "nt":
		subprocess.run([
			"vpm",
			"install",
			"hub"
		], check=True)
	else:
		if which("paru"):
			subprocess.run(["sudo", "paru", "-Sy", "--noconfirm", "unityhub"], check=True)
		elif which("yay"):
			subprocess.run(["sudo", "yay", "-Sy", "--noconfirm", "unityhub"], check=True)
		else:
			Path.home().joinpath("Applications").mkdir(parents=True, exist_ok=True)
			unityhub = Path.home() / "Applications" / "UnityHub.AppImage"
			urllib.request.urlretrieve("https://public-cdn.cloud.unity3d.com/hub/prod/UnityHub.AppImage", unityhub)
			unityhub.chmod(0o755)
except Exception as e:
	input(f"ERROR: Failed to install Unity Hub (try running as admin/root?)\n{e}")
	exit(1)

os.reload_environ()


print("Installing/Updating Unity...")

try:
	subprocess.run([
		"vpm",
		"install",
		"unity"
	], check=True)
except Exception as e:
	input(f"ERROR: Failed to install Unity\n{e}")
	exit(1)

os.reload_environ()


print("Adding VPM repositories...")

print("Adding VRCFury repo...")
subprocess.run(["vpm", "add", "repo", VRCFURY_REPO_URL], check=True)

print("Adding lilToon shader repo...")
subprocess.run(["vpm", "add", "repo", LILTOONSHADER_REPO_URL], check=True)

print("Adding Poiyomi Toon Shader repo...")
subprocess.run(["vpm", "add", "repo", POIYOMISHADER_REPO_URL], check=True)

print("Adding Modular Avatar repo...")
subprocess.run(["vpm", "add", "repo", MODULARAVATAR_REPO_URL], check=True)

print("Adding AAO: Avatar Optimizer repo...")
subprocess.run(["vpm", "add", "repo", AAOAVATAROPTIMIZER_REPO_URL], check=True)

print("Adding d4rkAvatarOptimizer repo...")
subprocess.run(["vpm", "add", "repo", D4RKAVATAROPTIMIZER_REPO_URL], check=True)

print("Adding Avatar Compressor repo...")
subprocess.run(["vpm", "add", "repo", AVATARCOMPRESSOR_REPO_URL], check=True)

print("Adding GoGo Loco repo...")
subprocess.run(["vpm", "add", "repo", GOGOLOCO_REPO_URL], check=True)


print("Creating new avatar project...")

project_dir_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

try:
	subprocess.run([
		"vpm",
		"new",
		project_dir_name,
		"Avatar",
		"-p",
		"."
	], check=True)
except Exception as e:
	input(f"ERROR: Failed to create new Avatar project\n{e}")
	exit(1)

os.chdir(project_dir_name)

try:
	subprocess.run([
		"vpm",
		"add",
		"project",
		os.getcwd()
	], check=True)
except Exception as e:
	input(f"ERROR: Failed to add newly-created project to list of VCC projects\n{e}")
	exit(1)


print("Adding packages to avatar project...")

print("Adding package: VRCFury...")
subprocess.run(["vpm", "add", "package", "com.vrcfury.vrcfury"], check=True)

print("Adding package: lilToon...")
subprocess.run(["vpm", "add", "package", "jp.lilxyzw.liltoon"], check=True)

print("Adding package: Poiyomi Toon Shader...")
subprocess.run(["vpm", "add", "package", "com.poiyomi.toon"], check=True)

print("Adding package: Modular Avatar...")
subprocess.run(["vpm", "add", "package", "nadena.dev.modular-avatar"], check=True)

print("Adding package: AAO: Avatar Optimizer...")
subprocess.run(["vpm", "add", "package", "com.anatawa12.avatar-optimizer"], check=True)

print("Adding package: d4rkAvatarOptimizer...")
subprocess.run(["vpm", "add", "package", "d4rkpl4y3r.d4rkavataroptimizer"], check=True)

print("Adding package: Avatar Compressor...")
subprocess.run(["vpm", "add", "package", "dev.limitex.avatar-compressor"], check=True)

print("Adding package: GoGoLoco...")
subprocess.run(["vpm", "add", "package", "gogoloco"], check=True)

print("Adding package: Gesture Manager...")
subprocess.run(["vpm", "add", "package", "vrchat.blackstartx.gesture-manager"], check=True)


print("Done!")


input("""
BASICS:

1) Find an avatar base on https://boothplorer.com/avatars (more items = better)
2) Drag and drop into project scene
3) Add a 'VRC Avatar Descriptor' component to it
4) ^ set 'View Position' to between avatar's eyes
5) 'VRChat SDK > Show Control Panel' (top-middle of window) -> build and upload
""")
