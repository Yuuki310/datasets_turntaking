for file in /data/group1/z40351r/datasets_turntaking/data/Callhome/jpn/original/*/*.wav; do
    
    session_name="${file: -8:-4}"
    echo "${session_name}"
    
    input="${file}"
    up_data_path="${file: :-21}up16k_data/${session_name}.wav"

    echo "${input}"
    echo "${up_data_path}"
    sox -G --buffer 32768 "${input}" -r 16000 -b 16 -S "${up_data_path}"
    
done