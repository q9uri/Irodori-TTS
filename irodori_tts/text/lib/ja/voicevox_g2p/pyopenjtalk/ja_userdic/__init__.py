from pathlib import Path
import os
import re

import jpreprocess

dict_folder = Path(__file__).parent
tmp_csv_path = Path(__file__).parent / "tmp.csv"
tmp_usr_dict_path = Path(__file__).parent / "tmp_user.csv"
tmp_dict_path = Path(__file__).parent / "tmp.bin"

def create_csv():

    dict_folder = Path(__file__).parent
    tmp_csv_path = Path(__file__).parent / "tmp.csv"
    tmp_dict_path = Path(__file__).parent / "tmp.bin"

    if not os.path.exists(str(tmp_csv_path)):
        dict_files = [
            "ja-jtalkdic-ud-edict2-noacc.txt",
            "ja-jtalkdic-ud-jawiki-noacc-00.txt",
            "ja-jtalkdic-ud-jawiki-noacc-01.txt",
            "ja-jtalkdic-ud-jawiki-noacc-02.txt",
            "ja-jtalkdic-ud-jawiki-noacc-03.txt",
            "ja-jtalkdic-ud-personal-names-noacc.txt",
            "ja-jtalkdic-ud-place-names-noacc.txt",
            "ja-jtalkdic-ud-thdic-character-noacc.txt",
            "ja-jtalkdic-ud-thdic-music-noacc.txt",
            "ja-jtalkdic-ud-thdic-sakuhin-noacc.txt",
            "ja-jtalkdic-ud-thdic-spelcard-noacc.txt",
            "ja-jtalkdic-ud-thdic-word-noacc.txt",
        ]

        data = ""
        for file in dict_files:
            file_path = dict_folder / file
            data += file_path.read_text(encoding="utf-8")

        new_data_list = []
        data_list = data.split("\n")
        for line in data_list:
            match_list = re.findall(',', line)
            if len(match_list) == 14:
                new_data_list.append(line)

        data = "\n".join(new_data_list)
        tmp_csv_path.write_text(data, encoding="utf-8")

        jpreprocess.build_dictionary(input=str(tmp_csv_path), output=str(tmp_dict_path), user=True)
