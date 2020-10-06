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
    0b01010 : [""],
}

number_layer = {
    
}

symbols_layer = {
    
}

function_layer = {
    
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
    0b1111111111 : "taplock"
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
