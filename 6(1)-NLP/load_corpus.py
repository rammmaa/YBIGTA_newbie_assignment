# 구현하세요!

from datasets import load_dataset

def load_corpus() -> list[str]:
    corpus: list[str] = []
    # 구현하세요!
    
    # poem_sentiment 데이터셋 로드
    dataset = load_dataset("google-research-datasets/poem_sentiment")
    
    # 학습 데이터에서 텍스트 추출
    train_data = dataset["train"]
    corpus = [text for text in train_data["verse_text"] if text is not None]
    
    return corpus