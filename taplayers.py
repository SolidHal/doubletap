# Copyright Hal Emmerich <SolidHal> 2020

### tap functions
taplock_key = "taplock"


# All internal layers should be integers
#layers on left hand
LEFT_PREFIX = 0 #left_prefix_layer
LEFT_CMD = 1 #"left_blank_cmd_layer"
SYMS = 2 #"symbols_layer"

#layers accessed by left hand prefix
RIGHT_PREFIX = 0 #right_prefix_layer
RIGHT_CMD = 1 #"right_blank_cmd_layer"
NUMS = 2 #"number_layer" # also includes the arrow keys
FN = 3 #"function_layer"

#layers on right hand
RIGHT_CMD = 1 #"right_blank_cmd_layer"
NUMS = 2 #"number_layer" # also includes the arrow keys
FN = 3 #"function_layer"

#layers accessed by right hand prefix
LEFT_CMD = 1 #"left_blank_cmd_layer"
SYMS = 2 #"symbols_layer"

#TODO
TFUNS = "tap_function_layer"




# All keys should be strings
left_prefix_layer = {
    #blank_tap
    0b00000 : [RIGHT_CMD],
    # modifiers/layers
    0b00001 : ['shift', 'win'],
    0b00010 : ['win'],
    0b00100 : ['shift'],
    0b01000 : [NUMS],
    0b10000 : ['ctrl'],
    0b10011 : [FN],
    # modifier combos
    0b01100 : ['shift', NUMS],
    0b01001 : ['shift', NUMS, 'win'],
    0b11000 : ['ctrl', NUMS], # since arrows are on the NUMS layer, we get ctrl + arrows here
    0b01010 : ['win', NUMS],
}
left_cmd_layer = {
    #blank_tap
    0b00000 : [],
    # specials
    0b11111 : ['space'],
    # letters
    0b00011 : ['a'],
    0b00110 : ['t'],
    0b00101 : ['e'],
    0b10001 : ['f'],
    0b10010 : ['x'], # mapped easily for cut
    0b00111 : ['d'],
    0b01110 : ['s'],
    0b11100 : ['z'],
    0b11001 : ['r'],
    0b01111 : ['w'],
    0b11110 : ['c'],
    0b11101 : ['g'],
    0b11011 : ['v'],
    0b01011 : ['b'],
    0b10100 : ['q'],
}

#order matters here, the blank_tap from cmd_layer wipes out the blank_tap from prefix_layer to avoid recursive circles
#we merge the base prefix layer and base cmd layer for each hand to form the default layer
left_blank_cmd_layer = {**left_prefix_layer, **left_cmd_layer}

right_prefix_layer = {
    #blank_tap
    0b00000 : [LEFT_CMD],
    # modifiers/layers
    0b10000 : ['shift', 'win'],
    0b01000 : ['win'],
    0b00100 : ['shift'],
    0b00010 : [SYMS],
    0b00001 : ['ctrl'],
    # modifier combos
    0b00110 : ['shift', SYMS],
    0b00101 : ['ctrl', 'shift'], # for c, v copy/paste in terminals
}

right_cmd_layer = {
    #blank_tap
    0b00000 : [],
    # specials
    0b11111 : ['backspace'],
    0b00011 : ['tab'],
    0b10011 : ['esc'],
    # punctuation
    0b10010 : ['?'],
    0b10001 : [';'],
    0b01001 : ['.'],
    0b01110 : [','],
    # letters
    0b11000 : ['o'],
    0b01100 : ['i'],
    0b10100 : ['u'],
    0b11100 : ['n'],
    0b00111 : ['h'],
    0b11001 : ['p'],
    0b11110 : ['m'],
    0b01111 : ['y'],
    0b10111 : ['l'],
    0b11011 : ['j'],
    0b11010 : ['k'],
}

#order matters here, the blank_tap from cmd_layer wipes out the blank_tap from prefix_layer to avoid recursive circles
right_blank_cmd_layer = {**right_prefix_layer, **right_cmd_layer}

right_empty_map = {
    # empty - not exhaustive, but limited to "easier" taps
}

number_layer = {
    0b10000 : ["1"],
    0b01000 : ["2"],
    0b11000 : ["3"],
    0b00100 : ["4"],
    0b10100 : ["5"],
    0b01100 : ["6"],
    0b11100 : ["7"],
    0b00010 : ["8"],
    0b10010 : ["9"],
    0b00111 : ["0"],
    0b11111 : ["up"],
    0b01111 : ["down"],
    0b10111 : ["left"],
    0b10011 : ["right"],
}

symbols_layer = {
    0b00001 : ["`"],
    0b00010 : ["-"],
    0b00011 : ["="],
    0b00100 : ["["],
    0b00101 : ["]"],
    0b00110 : ["\\"],
    0b00111 : ["'"],
}

function_layer = {
    0b10000 : ["f1"],
    0b01000 : ["f2"],
    0b11000 : ["f3"],
    0b00100 : ["f4"],
    0b10100 : ["f5"],
    0b01100 : ["f6"],
    0b11100 : ["f7"],
    0b00010 : ["f8"],
    0b10010 : ["f9"],
    0b00111 : ["f10"],
}

tap_function_layer = {
    
}

left_prefix_layers = {
    RIGHT_CMD : right_blank_cmd_layer,
    NUMS : number_layer,
    FN : function_layer,

}

right_prefix_layers = {
    LEFT_CMD : left_blank_cmd_layer,
    SYMS : symbols_layer,
}


# special dual tap macros
doublelayer = {
    0b0000000000 : "Zeros-- an impossible tap",
    0b1000000001 : "Pinkeys",
    0b0100000010 : "Rings",
    0b0010000100 : "Middles",
    0b0001001000 : "Pointers",
    0b0000110000 : "Thumbs",
    0b1111111111 : taplock_key
}

# hand = [ [layers_on_hand_list], [other_hand_layers_list] ]

left = [
    left_prefix_layer,
    left_cmd_layer,
    [left_blank_cmd_layer, symbols_layer],
    left_prefix_layers
]

right = [
    right_prefix_layer,
    right_cmd_layer,
    [right_blank_cmd_layer, number_layer, function_layer],
    right_prefix_layers
]

















### reference

full_left_hand_map = {
    0b00000 : [],
    0b00001 : [],
    0b00010 : [],
    0b00011 : [],
    0b00100 : [],
    0b00101 : [],
    0b00110 : [],
    0b00111 : [],
    0b01000 : [],
    0b01001 : [],
    0b01010 : [],
    0b01011 : [],
    0b01100 : [],
    0b01101 : [],
    0b01110 : [],
    0b01111 : [],
    0b10000 : [],
    0b10001 : [],
    0b10010 : [],
    0b10011 : [],
    0b10100 : [],
    0b10101 : [],
    0b10110 : [],
    0b10111 : [],
    0b11000 : [],
    0b11001 : [],
    0b11010 : [],
    0b11011 : [],
    0b11100 : [],
    0b11101 : [],
    0b11110 : [],
    0b11111 : [],
}

full_right_hand_map = {
    0b00000 : [],
    0b10000 : [],
    0b01000 : [],
    0b11000 : [],
    0b00100 : [],
    0b10100 : [],
    0b01100 : [],
    0b11100 : [],
    0b00010 : [],
    0b10010 : [],
    0b01010 : [],
    0b11010 : [],
    0b00110 : [],
    0b10110 : [],
    0b01110 : [],
    0b11110 : [],
    0b00001 : [],
    0b10001 : [],
    0b01001 : [],
    0b11001 : [],
    0b00101 : [],
    0b10101 : [],
    0b01101 : [],
    0b11101 : [],
    0b00011 : [],
    0b10011 : [],
    0b01011 : [],
    0b11011 : [],
    0b00111 : [],
    0b10111 : [],
    0b01111 : [],
    0b11111 : [],

}

def _reverseBits(code):
    return int('{:05b}'.format(code)[::-1], 2)

def generate_hand_map():
    print("left_hand_map")
    for i in range(0,32):
        print("    0b{:05b} : [],".format(i))
    print("right_hand_map")
    for i in range(0,32):
        j = _reverseBits(i)
        print("    0b{:05b} : [],".format(j))
