import os
import argparse

def rename_images_in_directory(directory):
    # 指定されたディレクトリ内を再帰的に探索
    for root, _, files in os.walk(directory):
        folder_name = os.path.basename(root)
        for file_name in files:
            # 対象のファイルが画像ファイルであるかを確認
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                # フォルダ名_ファイル名の形式で新しいファイル名を生成
                new_name = f"{folder_name}_{file_name}"
                old_path = os.path.join(root, file_name)
                new_path = os.path.join(root, new_name)
                
                # ファイルのリネームを実行
                if old_path != new_path:
                    os.rename(old_path, new_path)
                    print(f"Renamed: {old_path} -> {new_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename images to 'foldername_filename' format.")
    parser.add_argument("directory", help="Path to the target directory")
    args = parser.parse_args()

    # 指定されたディレクトリを使ってリネーム処理を実行
    rename_images_in_directory(args.directory)
