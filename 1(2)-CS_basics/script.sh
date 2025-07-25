cd "$(dirname "$0")"

# anaconda(또는 miniconda)가 존재하지 않을 경우 설치해주세요!
## TODO

if ! command -v conda >/dev/null 2>&1; then
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
    bash /tmp/miniconda.sh -b -p $HOME/miniconda3
    rm /tmp/miniconda.sh
    export PATH="$HOME/miniconda3/bin:$PATH"
fi

CONDA_BASE=$(conda info --base)
source "$CONDA_BASE/etc/profile.d/conda.sh"

# Conda 환셩 생성 및 활성화
if ! conda info --envs | grep -q "^myenv"; then
    conda create --name myenv python=3.10.8 --yes
fi

conda activate myenv

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
cd "submission" || { echo "[INFO] submission 디렉토리로 이동 실패"; exit 1; }

for file in *.py; do
    if [ -f "$file" ]; then

        full_name="${file%%.*}"  
        problem_num="$full_name"

        input_file="../input/${problem_num}_input"
        output_file="../output/${problem_num}_output"

        if [ ! -f "$input_file" ]; then
            echo "[INFO] 입력 파일 $input_file 가 존재하지 않습니다."
            continue
        fi
        python "$file" < "$input_file" > "$output_file"
    fi
done

# mypy 테스트 실행 및 mypy_log.txt 저장
mypy . > ../mypy_log.txt 2>&1
if [ $? -eq 0 ]; then
fi

# conda.yml 파일 생성
conda env export > ../conda.yml

# 가상환경 비활성화
conda deactivate
