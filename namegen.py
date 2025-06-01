import random
from name_components import themes

def main():
    '''print_planet_name_examples()
    print("Systems: ", end ="")
    for i in range(10):
        print(f"{generate_system_name()}, ", end="")'''
    print(generate_name("Abundant"))
        

def starts_with_vowel(s):
    return s[0].lower() in ['a', 'e', 'i', 'o', 'u']

def ends_with_vowel(s):
    return s[-1].lower() in ['a', 'e', 'i', 'o', 'u']

def is_duplicate_vowel_boundary(a: str, b: str):
    return a[-1].lower() == b[0].lower() and a[-1].lower() in ['a', 'e', 'i', 'o', 'u']

def generate_name(world_type: str, count: int = 1):
    if world_type not in themes:
        raise ValueError(f"Unknown world type: {world_type}")

    theme = themes[world_type]
    names = []

    for _ in range(count):
        prefix = random.choice(theme["prefixes"])
        suffix = random.choice(theme["suffixes"])

        if random.random() < 0.25:
            middle = random.choice(theme["middle_parts"])

            if is_duplicate_vowel_boundary(prefix, middle):
                middle = middle[1:]
            vowel1 = '' if ends_with_vowel(prefix) or starts_with_vowel(middle) else random.choice(['a', 'e', 'i', 'o', 'u'])

            if is_duplicate_vowel_boundary(middle, suffix):
                suffix = suffix[1:]
            vowel2 = '' if ends_with_vowel(middle) or starts_with_vowel(suffix) else random.choice(['a', 'e', 'i', 'o', 'u'])

            name = prefix + vowel1 + middle + vowel2 + suffix
        else:
            if is_duplicate_vowel_boundary(prefix, suffix):
                suffix = suffix[1:]
            vowel = '' if ends_with_vowel(prefix) or starts_with_vowel(suffix) else random.choice(['a', 'e', 'i', 'o', 'u'])

            name = prefix + vowel + suffix

        names.append(name)

    return names[0] if count == 1 else names

def generate_system_name():
    prefix = random.choice(themes["System"]["prefixes"])
    
    if random.random() < 0.5:
        # 2-digit number with constellation
        number = str(random.randint(0, 99)).zfill(2)
        constellation = random.choice(themes["System"]["constellation"])
        name = f"{prefix} {number} {constellation}"
    else:
        # 3-digit number, no constellation
        number = random.randint(100, 999)
        name = f"{prefix}-{number}"
    
    return name

def print_planet_name_examples():
    planet_types = [
        "Abundant",
        "Fertile",
        "Mountain",
        "Desert",
        "Volcanic",
        "Highlands",
        "Swamp",
        "Barren",
        "Radiant"
    ]
    
    for planet in planet_types:
        try:
            names = generate_name(planet, 8)
            print(f"{planet}: {', '.join(names)}")
        except Exception as e:
            print(f"{planet}: Error generating names - {e}")

if __name__ == "__main__":
    main()
