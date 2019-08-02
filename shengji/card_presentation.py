'''
手写terminal输入法与内部表示法的转换
'''

_terminal_char = ['2','3','4','5','6','7','8','9','0','J','Q','K','A','V','W']

_bin_char = list(range(2,14)) + [16, 32]

_terminal_prefix = ['!','d','c','h','b']

_bin_prefix = [0, 0, 1, 2, 3]

def _one_bin_card_from(input):
    if input[0] ==

def bin_card_from_terminal_string(input):
    if len(input)%2:
