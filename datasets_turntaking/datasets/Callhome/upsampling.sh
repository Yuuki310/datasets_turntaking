for file in /data/group1/z40351r/datasets_turntaking/data/Callhome/jpn/data_origin/*.wav; do
    
    session_name="${file: -8:-4}"
    echo "${session_name}"
    
    input="${file}"
    data_full_path="${file: :-20}data_full/${session_name}.wav"

    echo "${input}"
    echo "${data_full_path}"
    sox -G --buffer 32768 "${input}" -r 16000 -b 16 -S "${data_full_path}"
    
done