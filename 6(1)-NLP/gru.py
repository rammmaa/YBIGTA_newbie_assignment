import torch
from torch import nn, Tensor


class GRUCell(nn.Module):
    def __init__(self, input_size: int, hidden_size: int) -> None:
        super().__init__()
        # 구현하세요!
        self.hidden_size = hidden_size
        
        # GRU 게이트들을 위한 선형 레이어들
        self.r_gate = nn.Linear(input_size + hidden_size, hidden_size)
        self.z_gate = nn.Linear(input_size + hidden_size, hidden_size)
        self.h_gate = nn.Linear(input_size + hidden_size, hidden_size)

    def forward(self, x: Tensor, h: Tensor) -> Tensor:
        # 구현하세요!
        # x: (batch_size, input_size), h: (batch_size, hidden_size)
        batch_size = x.size(0)
        
        # 입력과 이전 hidden state 결합
        combined = torch.cat([x, h], dim=1)  # (batch_size, input_size + hidden_size)
        
        # 게이트 계산
        r = torch.sigmoid(self.r_gate(combined))  # reset gate
        z = torch.sigmoid(self.z_gate(combined))  # update gate
        
        # candidate hidden state 계산
        h_candidate = torch.cat([x, r * h], dim=1)
        h_tilde = torch.tanh(self.h_gate(h_candidate))
        
        # 새로운 hidden state 계산
        new_h = (1 - z) * h + z * h_tilde
        
        return new_h


class GRU(nn.Module):
    def __init__(self, input_size: int, hidden_size: int) -> None:
        super().__init__()
        self.hidden_size = hidden_size
        self.cell = GRUCell(input_size, hidden_size)
        # 구현하세요!

    def forward(self, inputs: Tensor) -> Tensor:
        # 구현하세요!
        # inputs: (batch_size, sequence_length, input_size)
        batch_size, seq_len, input_size = inputs.size()
        
        # 초기 hidden state
        h = torch.zeros(batch_size, self.hidden_size, device=inputs.device)
        
        # 시퀀스를 순차적으로 처리
        for t in range(seq_len):
            x_t = inputs[:, t, :]  # (batch_size, input_size)
            h = self.cell(x_t, h)
        
        # 마지막 hidden state 반환
        return h