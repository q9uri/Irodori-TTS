from safetensors import safe_open
import torch

# チェックしたいファイル名
file_path = "./models/Irodori-TTS-36L-interleaved.safetensors"

def inspect_safetensors(path):
    try:
        with safe_open(path, framework="pt", device="cpu") as f:
            # メタデータの取得
            metadata = f.metadata()
            if metadata:
                print(f"--- Metadata ---")
                for k, v in metadata.items():
                    print(f"{k}: {v}")
                print("-" * 30)

            # キーの一覧を取得してソート（層の順番で並ぶように）
            keys = sorted(f.keys())
            
            print(f"{'Key Name':<60} | {'Shape':<20} | {'dtype'}")
            print("-" * 95)
            
            for key in keys:
                tensor_slice = f.get_slice(key)
                shape = tensor_slice.get_shape()
                # 実際のデータ型を取得するために1要素だけ取得するか、
                # もしくは単純にキー名と形状を表示
                print(f"{key:<60} | {str(shape):<20} | {f.get_tensor(key).dtype}")

            print("-" * 95)
            print(f"Total keys: {len(keys)}")

    except Exception as e:
        print(f"Error reading {path}: {e}")

if __name__ == "__main__":
    inspect_safetensors(file_path)
