import configparser
from typing import Dict, List

class Args:
    """
    A class hold all the configurable arguments. they are being read from a config file (config.ini)
    """

    _instance = None

    dataset_path: str = ''
    models_dir: str = ''
    batch_size: int = 0
    learning_rate: float = 0.0
    max_iters: int = 0
    eval_iters: int = 0
    eval_interval: int = 0
    model_save_interval: int = 0
    load_checkpoint: bool = False
    test_size: float = 0.0
    n_head: int = 0
    n_embd: int = 0
    block_size: int = 0
    ff_hidden_dim: int = 0
    num_experts: int = 0
    num_experts_per_tok: int = 0
    norm_eps: float = 0.0
    vocab_size: int = 0
    device: str = ''
    n_layers: int = 0

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        args = dict(config['Core'])

        for k, v in args.items():
            if not v:
                continue
            # default type is string
            conversion = lambda x : x
            # if needed, convert argument to corresponding datatype
            if isinstance(getattr(Args, k), bool):
                conversion = lambda x : bool(x)

            elif isinstance(getattr(Args, k), int):
                conversion = lambda x : int(x)

            elif isinstance(getattr(Args, k), float):
                conversion = lambda x : float(x)
            
            setattr(Args, k, conversion(v))

        # vocab size has to be infered from the data (when using of character level tokenizer)
        with open(Args.dataset_path, 'r') as f:
            text = f.read()
            setattr(Args, 'vocab_size', len(list(set(text))))

    @classmethod
    def get_default_args(cls):
        if not cls._instance:
            cls._instance = cls() 
        return cls._instance


class Tokenizer:
    """
    A wrapper class providing interface for 
    character level tokenization.
    """
    vocab_size: int
    stoi: Dict[str, int]
    itos: Dict[int, str]

    def __init__(self) -> None:
        args = Args.get_default_args()
        self.vocab_size = args.vocab_size

        with open(args.dataset_path, encoding='utf-8') as f:
            s = f.read()

        chars = sorted(list(set(s)))

        self.stoi = { ch:i for i,ch in enumerate(chars) }
        self.itos = { i:ch for i,ch in enumerate(chars) }

    def encode(self, input_str: str) -> List[int]:
        """
        Encodes an input string in a list of tokens.
        """
        return [self.stoi[c] for c in input_str]
    
    def decode(self, tokens: List[int]) -> str:
        """
        Decodes a list of tokens back to the string format.
        """
        return ''.join([self.itos[i] for i in tokens]) 


if __name__ == "__main__":
    
    tokenizer = Tokenizer()

    print(tokenizer.decode(tokenizer.encode('Mixture of experts')))



