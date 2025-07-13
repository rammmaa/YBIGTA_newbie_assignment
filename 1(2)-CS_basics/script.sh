# anaconda(또는 miniconda)가 존재하지 않을 경우 설치해주세요!
## TODO


if ! command -v conda >/dev/null 2>&1; then
    echo "[INFO] conda 없어서 miniconda 설치함..."
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
    bash /tmp/miniconda.sh -b -p $HOME/miniconda3
    rm /tmp/miniconda.sh
    export PATH="$HOME/miniconda3/bin:$PATH"
    echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc
else
    echo "[INFO] conda 이미 있음"
fi

# Conda 환셩 생성 및 활성화
## TODO

conda init
conda create --name myenv python=3.10.8 --yes
conda activate myenv

echo "[DEBUG] python path: $(which python)"
echo "[DEBUG] python sys.prefix: $(python -c 'import sys; print(sys.prefix)')"


## 건드리지 마세요! ##
python_env=$(python -c "import sys; print(sys.prefix)")
if [[ "$python_env" == *"/envs/myenv"* ]]; then
    echo "[INFO] 가상환경 활성화: 성공"
else
    echo "[INFO] 가상환경 활성화: 실패"
    exit 1 
fi

# 필요한 패키지 설치
conda install mypy -y --quiet

# Submission 폴더 파일 실행
cd "/Users/yoons/Desktop/1(2)-CS_basics/submission" || { echo "[INFO] submission 디렉토리로 이동 실패"; exit 1; }

for file in *.py; do
    if [ -f "$file" ]; then
        # 문제번호 추출 (ex: 2243.py -> 2243)
        full_name="${file%%.*}"   # 1_1260
        problem_num="${full_name#*_}"  # 접두사 제거, 1260만 남음

        input_file="../input/${problem_num}_input"
        output_file="../output/${problem_num}_output"

        if [ ! -f "$input_file" ]; then
            echo "[INFO] 입력 파일 $input_file 가 존재하지 않습니다."
            continue
        fi

        # 파이썬 파일 실행 (input redirect, output redirect)
        python "$file" < "$input_file" > "$output_file"
        if [ $? -ne 0 ]; then
            echo "[INFO] $file 실행 실패"
        else
            echo "[INFO] $file 실행 성공, 결과 저장: $output_file"
        fi
    else
        echo "[INFO] 실행할 .py 파일이 없습니다."
        break
    fi
done

# mypy 테스트 실행 및 mypy_log.txt 저장
mypy . > ../mypy_log.txt 2>&1
if [ $? -eq 0 ]; then
    echo "[INFO] mypy 테스트 성공"
else
    echo "[INFO] mypy 테스트 실패 (로그: mypy_log.txt)"
fi

# conda.yml 파일 생성
conda env export > ../conda.yml

# 가상환경 비활성화
conda deactivate