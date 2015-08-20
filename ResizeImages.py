#coding:utf-8

import ConfigParser
import Image
import os

# リサイズ処理
def Resize(file_path, save_path, pixel):
	img = Image.open(file_path)
	
	# サイズをチェックしてリサイズ
	if img.size[0] > pixel or img.size[1] > pixel:
		if img.size[0] > img.size[1]:
			img.thumbnail((pixel, 2000), Image.ANTIALIAS)
		elif img.size[0] < img.size[1]:
			img.thumbnail((2000, pixel), Image.ANTIALIAS)
	
	#　カラーモードを変換する
	img = img.convert("RGBA")
	
	#　クオリティを設定して保存
	img.save(save_path, quality = 100)

# 対象フォルダを処理
def FolderProcess(org_dir, target_dir, pixel):
	# ターゲットディレクトリの作成
	if not os.path.exists(target_dir):
		os.mkdir(target_dir)

	for root, dirs, files in os.walk(unicode(org_dir)):
		# ディレクトリの作成
		for name in dirs:
			dir_path = os.path.join(target_dir, name)
			if not os.path.exists(dir_path):
			 	os.makedirs(dir_path)

		# リサイズ処理
		for name in files:
			for ext in [".jpg",".jpeg",".Jpg",".Jpeg",".JPG",".JPEG",".png",".PNG",".bmp",".BMP"]:
				if name.find(ext) > -1:
					file_path = os.path.join(root, name)
					save_path = file_path.replace(org_dir, target_dir)
					if not os.path.exists(save_path):
						Resize(file_path, save_path, pixel)
					break

def Main():
	# 設定の読み込み
	config = ConfigParser.SafeConfigParser()
	if os.path.exists("config.ini"):
		config.read("config.ini")
	else:
		return;

	ORG_DIR = config.get("SETTINGS", "ORG_DIR")
	TARGET_DIRS = config.get("SETTINGS", "TARGET_DIRS").split(",")
	TARGET_PIXELS = config.get("SETTINGS", "TARGET_PIXELS").split(",")

	for (target_dir, target_pixel) in zip(TARGET_DIRS, TARGET_PIXELS):
		FolderProcess(ORG_DIR, target_dir, int(target_pixel))

if __name__ == "__main__":
	Main()