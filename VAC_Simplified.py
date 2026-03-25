import os
import subprocess
import tkinter.simpledialog as tk_dialog
import tkinter.filedialog as tk_filedialog
from shutil import which
from pathlib import Path
import urllib.request
from bs4 import BeautifulSoup



# v format: "REPO": ["PACKAGE_1", "PACKAGE_2", ...]
PACKAGES = {
	# Packages from official SDK: Gesture Manager
	"": ["vrchat.blackstartx.gesture-manager"],

	# VRCFury
	"https://vcc.vrcfury.com/": ["com.vrcfury.vrcfury"],

	# lilToons shader
	"https://lilxyzw.github.io/vpm-repos/vpm.json": ["jp.lilxyzw.liltoon"],

	# Poiyomi Toon Shader
	"https://poiyomi.github.io/vpm/index.json": ["com.poiyomi.toon"],

	# Modular Avatar
	"https://vpm.nadena.dev/vpm.json": ["nadena.dev.modular-avatar"],

	# AAO: Avatar Optimizer
	"https://vpm.anatawa12.com/vpm.json": ["com.anatawa12.avatar-optimizer"],

	# d4rkAvatarOptimizer
	"https://d4rkc0d3r.github.io/vpm-repos/main.json": ["d4rkpl4y3r.d4rkavataroptimizer"],

	# Avatar Compressor
	"https://vpm.limitex.dev/index.json": ["dev.limitex.avatar-compressor"],

	# GoGo Loco
	"https://Spokeek.github.io/goloco/index.json": ["gogoloco"]
}

ALCOM_URL = "https://vrc-get.anatawa12.com/alcom/"
ALCOM_HTML_LINUX_DOWNLOAD_ELEM_ID = "btn-download-linux"



project_name = tk_dialog.askstring("", "Project name (can be anything):")
if project_name == "" or project_name == None: exit(0)

project_path = tk_filedialog.askdirectory(title="Project path")
if project_path == "": exit(0)


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
		alcom = Path.home() / "Applications" / "alcom.AppImage"
		urllib.request.urlretrieve(
			BeautifulSoup(
				urllib.request.urlopen(ALCOM_URL).read().decode('utf-8'),
				"html.parser"
			).find(id=ALCOM_HTML_LINUX_DOWNLOAD_ELEM_ID).get('href'),

			alcom
		)
		alcom.chmod(0o755)
except Exception as e:
	if (
		(os.name == "nt" and subprocess.run(["winget", "list", "anatawa12.ALCOM"]).returncode != 0)
		or
		(os.name != "nt")
	):
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
			subprocess.run(["sudo", "pacman", "-Sy", "--noconfirm", "dotnet-sdk-8.0"], check=True)
		else:
			subprocess.run("curl -fsSL https://dot.net/v1/dotnet-install.sh | bash -s -- --channel 8.0", check=True, shell=True)
			# ^ + add to path:
			path_export_cmd = f'export PATH="$PATH:{str(Path.home() / ".dotnet")}:{str(Path.home() / ".dotnet/tools")}"'
			subprocess.run(path_export_cmd, check=True, shell=True)
			bashrc = Path.home() / ".bashrc"
			if bashrc.exists(): open(bashrc, "a").write(f'\n{path_export_cmd}\n')
except Exception as e:
	os.reload_environ() # So that the following check can work
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
	os.reload_environ() # So that the following check can work
	if subprocess.run(["vpm", "--version"]).returncode != 0:
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

for repo in PACKAGES.keys():
	if repo == "": continue
	print(f"Adding repo: {repo}...")
	subprocess.run(["vpm", "add", "repo", repo])


print("Creating new avatar project...")

try:
	subprocess.run([
		"vpm",
		"new",
		project_name,
		"Avatar",
		"-p",
		project_path
	], check=True)
except Exception as e:
	input(f"ERROR: Failed to create new Avatar project\n{e}")
	exit(1)

os.chdir(os.path.join(project_path, project_name))

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

for packages in PACKAGES.values():
	for package in packages:
		print(f"Adding package: {package}...")
		subprocess.run(["vpm", "add", "package", package])


print("Done!")


input("""
BASICS:

1) Find an avatar base on https://boothplorer.com/avatars (more items = better)
2) Drag and drop into project scene
3) Add a 'VRC Avatar Descriptor' component to it
4) ^ set 'View Position' to between avatar's eyes
5) 'VRChat SDK > Show Control Panel' (top-middle of window) -> build and upload
""")