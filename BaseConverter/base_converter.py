def is_valid_input(num_to_convert, source_base, target_base):
    """Check whether the number and bases are valid"""
    if num_to_convert.count('.') != 1 or not (2 <= source_base <= 10 and 2 <= target_base <= 10):
        return False

    for part in num_to_convert.split('.'):
        if not part.isdigit():
            return False

        for char in part:
            if int(char) >= source_base:
                return False
    return True


def get_valid_input():
    """Request user input until valid values are entered"""
    while True:
        num_to_convert = str(input("Enter the number to convert "))
        source_base = int(input("Enter the source base "))
        target_base = int(input("Enter the target base "))

        if is_valid_input(num_to_convert, source_base, target_base):
            return num_to_convert, source_base, target_base

        print("Invalid input! Please try again.")


def remove_unnecessary_zeros(converted_num):
    """Remove unnecessary leading and trailing zeros"""
    if "." in converted_num:
        converted_num = converted_num.rstrip("0").rstrip(".")

    converted_num = converted_num.lstrip("0")

    if converted_num == "" or converted_num[0] == ".":
        converted_num = "0" + converted_num

    return converted_num


def add_carry_to_digits(reversed_digits, target_base):
    """Add a carry to reversed digits and return the updated digits and the remaining carry"""
    carry = 1
    rounded_digits = ""

    for digit in reversed_digits:
        result = int(digit) + carry
        carry = result // target_base
        rounded_digits += str(result % target_base)

    return rounded_digits, carry


def round_to_10_fraction_digits(converted_num, target_base):
    """Round the number to a maximum of 10 fractional digits"""
    if '.' not in converted_num:
        return remove_unnecessary_zeros(converted_num)

    converted_integer, converted_fraction = converted_num.split('.')

    if len(converted_fraction) >= 11:

        # Keep the first 10 fractional digits and use the 11th for rounding
        rounding_digit = int(converted_fraction[10])
        converted_fraction = converted_fraction[:10]

        # Round up if the rounding digit is at least half of the target base
        if rounding_digit * 2 >= target_base :
            converted_fraction, carry = add_carry_to_digits(converted_fraction[::-1], target_base)
            converted_fraction = converted_fraction[::-1]

            # Add the carry to the integer part
            if carry == 1:
                converted_integer, carry = add_carry_to_digits(converted_integer[::-1], target_base)
                converted_integer = converted_integer[::-1]

                # Add 1 to the beginning if there is still a carry
                if carry == 1:
                    converted_integer = "1" + converted_integer

    # Combine the integer and fractional parts
    converted_num = converted_integer + "." + converted_fraction

    return remove_unnecessary_zeros(converted_num)


def convert_to_decimal(reversed_integer_digits, fractional_digits, source_base):
    """Convert the source number to decimal using an integer part, numerator and denominator"""
    integer_part = 0
    final_numerator = 0

    # Calculate the common denominator
    common_denominator = source_base ** len(fractional_digits)

    # Convert the integer part to decimal
    for i in range(len(reversed_integer_digits)):
        integer_part += int(reversed_integer_digits[i]) * source_base ** i

    # Calculate the numerator of the fractional part
    # using the common denominator
    for j in range(len(fractional_digits)):
        denominator = source_base ** (j + 1)
        final_numerator += int(fractional_digits[j]) * (common_denominator // denominator)

    return integer_part, final_numerator, common_denominator


def convert_to_target_base(integer_part, numerator, denominator, target_base):
    """Convert the integer and fractional parts to the target base"""
    converted_integer = ""
    converted_fraction = ""

    # Convert the integer part using repeated division
    while integer_part > 0:
        converted_integer += str(integer_part % target_base)
        integer_part //= target_base

    converted_integer = converted_integer[::-1]
    if converted_integer == "":
        converted_integer = "0"

    # Convert up to 11 fractional digits, including one for rounding
    for _ in range(11):
        if numerator == 0:
            break

        result = numerator * target_base
        digit = result // denominator
        numerator = result % denominator
        converted_fraction += str(digit)

    if converted_fraction != "":
        converted_num = converted_integer + '.' + converted_fraction
        return round_to_10_fraction_digits(converted_num, target_base)

    converted_num = converted_integer
    return remove_unnecessary_zeros(converted_num)


def main():
    """Manage the number conversion process"""
    num_to_convert, source_base, target_base = get_valid_input()

    if source_base == target_base:
        result = round_to_10_fraction_digits(num_to_convert, target_base)
    else:
        number_parts = num_to_convert.split('.')
        reversed_integer_digits = number_parts[0][::-1]
        fractional_digits = number_parts[1]

        integer_part, numerator, denominator = convert_to_decimal(
            reversed_integer_digits, fractional_digits, source_base
        )

        result = convert_to_target_base(
            integer_part, numerator, denominator, target_base
        )

    print(f"Result: {result}")


main()
