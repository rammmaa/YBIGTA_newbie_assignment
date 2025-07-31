import torch
from torch import nn, Tensor, LongTensor
from torch.optim import Adam

from transformers import PreTrainedTokenizer

from typing import Literal

# 구현하세요!


class Word2Vec(nn.Module):
    def __init__(
        self,
        vocab_size: int,
        d_model: int,
        window_size: int,
        method: Literal["cbow", "skipgram"]
    ) -> None:
        super().__init__()
        self.embeddings = nn.Embedding(vocab_size, d_model)
        self.weight = nn.Linear(d_model, vocab_size, bias=False)
        self.window_size = window_size
        self.method = method
        # 구현하세요!
        self.vocab_size = vocab_size
        self.d_model = d_model

    def embeddings_weight(self) -> Tensor:
        return self.embeddings.weight.detach()

    def fit(
        self,
        corpus: list[str],
        tokenizer: PreTrainedTokenizer,
        lr: float,
        num_epochs: int
    ) -> None:
        criterion = nn.CrossEntropyLoss()
        optimizer = Adam(self.parameters(), lr=lr)
        # 구현하세요!
        
        # 코퍼스를 토큰화
        tokenized_corpus = []
        for text in corpus:
            tokens = tokenizer.tokenize(text)
            token_ids = tokenizer.convert_tokens_to_ids(tokens)
            if isinstance(token_ids, list):
                tokenized_corpus.append(token_ids)
        
        # 학습
        for epoch in range(num_epochs):
            total_loss = 0
            num_batches = 0
            
            for token_ids in tokenized_corpus:
                if len(token_ids) < 2 * self.window_size + 1:
                    continue
                
                if self.method == "cbow":
                    loss = self._train_cbow(token_ids, criterion, optimizer)
                else:  # skipgram
                    loss = self._train_skipgram(token_ids, criterion, optimizer)
                
                total_loss += loss
                num_batches += 1
            
            if num_batches > 0:
                avg_loss = total_loss / num_batches
                if epoch % 10 == 0:
                    print(f"Epoch {epoch}, Loss: {avg_loss:.6f}")

    def _train_cbow(
        self,
        token_ids: list[int],
        criterion: nn.CrossEntropyLoss,
        optimizer: Adam
    ) -> float:
        # 구현하세요!
        total_loss = 0
        num_samples = 0
        
        # 더 많은 샘플링을 위해 윈도우 크기를 조정
        effective_window = min(self.window_size, len(token_ids) // 4)
        
        for i in range(effective_window, len(token_ids) - effective_window):
            # 중심 단어
            target = token_ids[i]
            
            # 주변 단어들 (context) - 더 많은 샘플링
            context = []
            for j in range(i - effective_window, i + effective_window + 1):
                if j != i and 0 <= j < len(token_ids):
                    context.append(token_ids[j])
            
            if len(context) == 0:
                continue
                
            # 입력과 타겟 준비
            context_tensor = torch.tensor(context, dtype=torch.long)
            target_tensor = torch.tensor([target], dtype=torch.long)
            
            # 순전파
            context_embeddings = self.embeddings(context_tensor)
            context_mean = context_embeddings.mean(dim=0, keepdim=True)
            output = self.weight(context_mean)
            
            # 손실 계산 및 역전파
            loss = criterion(output, target_tensor)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            num_samples += 1
        
        return total_loss / max(num_samples, 1)

    def _train_skipgram(
        self,
        token_ids: list[int],
        criterion: nn.CrossEntropyLoss,
        optimizer: Adam
    ) -> float:
        # 구현하세요!
        total_loss = 0
        num_samples = 0
        
        # 더 많은 샘플링을 위해 윈도우 크기를 조정
        effective_window = min(self.window_size, len(token_ids) // 4)
        
        for i in range(effective_window, len(token_ids) - effective_window):
            # 중심 단어
            center_word = token_ids[i]
            
            # 주변 단어들 (target) - 더 많은 샘플링
            for j in range(i - effective_window, i + effective_window + 1):
                if j != i and 0 <= j < len(token_ids):
                    target_word = token_ids[j]
                    
                    # 입력과 타겟 준비
                    center_tensor = torch.tensor([center_word], dtype=torch.long)
                    target_tensor = torch.tensor([target_word], dtype=torch.long)
                    
                    # 순전파
                    center_embedding = self.embeddings(center_tensor)
                    output = self.weight(center_embedding)
                    
                    # 손실 계산 및 역전파
                    loss = criterion(output, target_tensor)
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
                    
                    total_loss += loss.item()
                    num_samples += 1
        
        return total_loss / max(num_samples, 1)

    # 구현하세요!
    pass