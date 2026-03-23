import os
import subprocess
import tkinter.simpledialog as tk_dialog
import tkinter.filedialog as tk_filedialog



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



project_name = ""
while project_name == "": project_name = tk_dialog.askstring("", "Project name (can be anything):")

project_path = tk_filedialog.askdirectory(title="Project path")


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
		pass # TODO: Implement for Linux
except Exception as e:
	if subprocess.run("winget list anatawa12.ALCOM").returncode != 0:
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
	else: # NOTE: untested on Linux
		subprocess.run("curl https://dot.net/v1/dotnet-install.sh | bash", check=True, shell=True)
except Exception as e:
	if subprocess.run("winget list Microsoft.Dotnet.SDK.8").returncode != 0:
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
	subprocess.run([
		"vpm",
		"install",
		"hub"
	], check=True)
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
	subprocess.run(f"vpm add repo {repo}")


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
		subprocess.run(f"vpm add package {package}")


print("Done!")


input("""
BASICS:

1) Find an avatar base on https://boothplorer.com/avatars (more items = better)
2) Drag and drop into project scene
3) Add a 'VRC Avatar Descriptor' component to it
4) ^ set 'View Position' to between avatar's eyes
5) 'VRChat SDK > Show Control Panel' (top-middle of window) -> build and upload
""")