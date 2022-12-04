import random
from dataclasses import dataclass
from typing import Literal, Optional

import numpy as np
import torch as t

ModelName = Literal["bert-base-uncased"]
TokenizerName = Literal["bert-base-uncased"]


@dataclass
class Config:
    """
    Config for a BERT model. For applicable values of [model] and [tokenizer],
    see [bert/config.py].
    """

    model: ModelName

    layers: int
    heads: int
    hidden_size: int

    """
    used in [attention.py]. can be equal to [hidden_size // heads] or can be smaller to make the model work in parallel.
    """
    head_size: int

    vocab_size: int
    mlp_size: int

    max_length: int

    dropout: float = 0.1

    device: Optional[t.device] = None

    tokenizer: Optional[TokenizerName] = None

    seed: int = 42

    @classmethod
    def __set_seed_everywhere__(cls, seed: int):
        t.manual_seed(seed)
        random.seed(seed)
        np.random.seed(seed)

    def __post_init__(self):
        if self.device is None:
            self.device = t.device("cuda" if t.cuda.is_available() else "cpu")

        if self.tokenizer is None:
            self.tokenizer = self.model

        Config.__set_seed_everywhere__(self.seed)