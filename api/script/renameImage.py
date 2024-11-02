import os
import shutil
import argparse

def rename_images_in_directory(directory, destination=None):
    # 指定されたディレクトリ内を再帰的に探索
    for root, _, files in os.walk(directory):
        relative_path = os.path.relpath(root, directory)  # ディレクトリ内での相対パスを取得
        folder_name = os.path.basename(root)

        for file_name in files:
            # 対象のファイルが画像ファイルであるかを確認
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                new_name = f"{folder_name}_{file_name}"
                
                if destination:
                    # コピー用のパスを設定
                    dest_dir = os.path.join(destination, relative_path)
                    os.makedirs(dest_dir, exist_ok=True)
                    old_path = os.path.join(root, file_name)
                    new_path = os.path.join(dest_dir, new_name)
                    shutil.copy2(old_path, new_path)
                    print(f"Copied and Renamed: {old_path} -> {new_path}")
                else:
                    # リネームのみ実行
                    old_path = os.path.join(root, file_name)
                    new_path = os.path.join(root, new_name)
                    if old_path != new_path:
                        os.rename(old_path, new_path)
                        print(f"Renamed: {old_path} -> {new_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename images or copy and rename images with folder structure.")
    parser.add_argument("directory", help="Path to the target directory")
    parser.add_argument("--copy", nargs='?', const=True, default=False, help="Copy files to a new directory with the same folder structure")
    args = parser.parse_args()

    if args.copy:
        # コピー先のディレクトリパスを元ディレクトリの同階層に設定
        destination_path = os.path.join(os.path.dirname(args.directory), f"{os.path.basename(args.directory)}_copy")
        os.makedirs(destination_path, exist_ok=True)
        rename_images_in_directory(args.directory, destination_path)
    else:
        rename_images_in_directory(args.directory)
