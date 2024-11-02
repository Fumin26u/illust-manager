import os
import shutil
import argparse

def collect_images(directory, destination):
    # ディレクトリ内を再帰的に探索
    for root, _, files in os.walk(directory):
        for file_name in files:
            # 対象のファイルが画像ファイルであるかを確認
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                old_path = os.path.join(root, file_name)
                new_path = os.path.join(destination, file_name)
                
                # 同名ファイルが集約フォルダに既に存在する場合の処理
                if os.path.exists(new_path):
                    base, ext = os.path.splitext(file_name)
                    counter = 1
                    while os.path.exists(new_path):
                        new_path = os.path.join(destination, f"{base}_{counter}{ext}")
                        counter += 1
                
                # ファイルをコピー
                shutil.copy2(old_path, new_path)
                print(f"Copied: {old_path} -> {new_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect images from directory into one folder.")
    parser.add_argument("directory", help="Path to the source directory")
    parser.add_argument("destination", help="Path to the destination directory")
    args = parser.parse_args()

    # 集約フォルダが存在しない場合は作成
    if not os.path.exists(args.destination):
        os.makedirs(args.destination)

    # 画像集約処理を実行
    collect_images(args.directory, args.destination)
