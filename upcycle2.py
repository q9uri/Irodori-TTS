import torch
from safetensors.torch import load_file, save_file
import re

def upcycle_interleaved_24_layers(input_path, output_path):
    state_dict = load_file(input_path)
    new_state_dict = {}
    
    # メインブロックの層数を 12 -> 24 に拡張
    # 既存の i 層目を、新しいモデルの 2i 層目と 2i+1 層目に割り当てる
    for key, value in state_dict.items():
        if key.startswith("blocks."):
            # keyの形式: "blocks.N.attention..."
            split_key = key.split(".")
            index = int( split_key[1] )
            
            key_a_split = [split_key[0], str(index *2)] + split_key[2:]
            key_b_split = [split_key[0], str(index *2 + 1)] + split_key[2:]

            
            new_key_a = ".".join(key_a_split)
            new_key_b = ".".join(key_b_split)
                
            new_state_dict[new_key_a] = value.clone()
            new_state_dict[new_key_b] = value.clone()
        else:
            # text_encoder や speaker_encoder などはそのままコピー
            new_state_dict[key] = value

    # メタデータの更新（任意）
    metadata = {
        "num_layers": "24",
        "upcycled_by": "Gemini-Stacking-Script",
        "method": "interleaved_2_layer_copy",
        "config_json": '{ \
            "latent_dim":32, \
            "latent_patch_size":1, \
            "model_dim":1280, \
            "num_layers":24, \
            "num_heads":20, \
            "mlp_ratio":2.875, \
            "text_mlp_ratio":2.6, \
            "speaker_mlp_ratio":2.6, \
            "dropout":0.0, \
            "text_vocab_size":99574, \
            "text_tokenizer_repo":"llm-jp/llm-jp-3-150m", \
            "text_add_bos":true, \
            "text_dim":512, \
            "text_layers":10, \
            "text_heads":8, \
            "speaker_dim":768, \
            "speaker_layers":8, \
            "speaker_heads":12, \
            "speaker_patch_size":1, \
            "timestep_embed_dim":512, \
            "adaln_rank":192, \
            "norm_eps":1e-05, \
            "max_text_len":256, \
            "fixed_target_latent_steps":750}' 
    }
    
    save_file(new_state_dict, output_path, metadata=metadata)
    print(f"Done! 24層モデルを保存しました: {output_path}")

# 実行例
upcycle_interleaved_24_layers("./models/Irodori-TTS-500M-v2.safetensors", "./models/Irodori-TTS-24L-interleaved.safetensors")
