import os
import shutil


def cleanup_folders(folder_paths):
    """
    지정된 폴더들의 모든 파일을 삭제합니다.

    Args:
        folder_paths (list): 파일을 삭제할 폴더 경로 리스트
    """
    for folder_path in folder_paths:
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # 파일 삭제
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # 디렉토리 삭제
                except Exception as e:
                    print(f"파일 {file_path}를 삭제하는데 실패했습니다: {e}")
        else:
            print(f"폴더를 찾을 수 없습니다: {folder_path}")
