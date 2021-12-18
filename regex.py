def match_symbol(regex, char):
    if regex in (".", "") or regex == char:
        return True
    return False

def match_strings_with_equal_lengths(regex, word, prev_symbol_matched=False):
    if not regex:
        return True

    if not word:
        if regex == ['$']:
            return True
        if len(regex) == 2 and regex[1] in ("*", "+"):
            return True
        else:
            return False

    first_regex, *rest_regex = regex
    first_char, *rest_chars = word

    if rest_regex == ['$'] and rest_chars == []:
        return True

    if first_regex == "\\":
        if len(rest_regex) > 0:
            if rest_regex[0] == first_char:
                return match_strings_with_equal_lengths(rest_regex[1:], rest_chars)

    if len(rest_regex) > 0 and rest_regex[0] == '?' and first_regex != "\\":
        if match_symbol(first_regex, first_char):
            return match_strings_with_equal_lengths(rest_regex[1:], rest_chars)
        elif len(rest_regex) >= 2 and match_symbol(rest_regex[1], first_char):
            return match_strings_with_equal_lengths(rest_regex[2:], rest_chars[1:])

    if len(rest_regex) > 0 and rest_regex[0] == '*' and first_regex != "\\":
        if match_symbol(first_regex, first_char):
            return match_strings_with_equal_lengths(regex, rest_chars)
        elif len(rest_regex) >= 2 and match_symbol(rest_regex[1], first_char):
            return match_strings_with_equal_lengths(rest_regex[2:], rest_chars[1:])

    if len(rest_regex) > 0 and rest_regex[0] == '+' and first_regex != "\\":
        if not prev_symbol_matched:
            if match_symbol(first_regex, first_char):
                return match_strings_with_equal_lengths(regex, rest_chars, True)
            else:
                return False
        elif prev_symbol_matched:
            if len(rest_regex) > 1 and rest_regex[1] == first_char:
                # time to leave
                return match_strings_with_equal_lengths(rest_regex[1:], word)
            elif match_symbol(first_regex, first_char):
                return match_strings_with_equal_lengths(regex, rest_chars, True)
            else:
                return match_strings_with_equal_lengths(rest_regex[1:], word)

    if match_symbol(first_regex, first_char):
        return match_strings_with_equal_lengths(rest_regex, rest_chars)
    else:
        return False

def match(regex, word):
    if not regex:
        return True
    if not word:
        return False

    if regex[0] == "^":
        return match_strings_with_equal_lengths(regex[1:], word)

    res = match_strings_with_equal_lengths(regex, word)

    if res:
        return True
    else:
        return match(regex, word[1:])

inputs = input().split("|")
print(match(inputs[0], inputs[1]))
