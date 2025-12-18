

print("---------------Get Account------------------")


# https://www.cnb.cz/export/sites/cnb/en/payments/.galleries/accounts_bank_codes/download/bank_codes_CR.pdf
d_bank_codes_to_bic = {
    "0100": ("Komerční banka, a.s.", "KOMBCZPP"),
    "0300": ("Československá obchodní banka, a. s.", "CEKOCZPP"),
    "0600": ("MONETA Money Bank, a.s.", "AGBACZPP"),
    "0710": ("ČESKÁ NÁRODNÍ BANKA", "CNBACZPP"),
    "0800": ("Česká spořitelna, a.s.", "GIBACZPX"),
    "2010": ("Fio banka, a.s.", "FIOBCZPP"),
    "2060": ("Citfin, spořitelní družstvo", "CITFCZPP"),
    "2070": ("TRINITY BANK a.s.", "MPUBCZPP"),
    "2100": ("ČSOB Hypoteční banka, a.s.", "-"),
    "2200": ("Peněžní dům, spořitelní družstvo", "-"),
    "2220": ("Artesa, spořitelní družstvo", "ARTTCZPP"),
    "2250": ("Banka CREDITAS a.s.", "CTASCZ22"),
    "2260": ("NEY spořitelní družstvo", "-"),
    "2600": ("Citibank Europe plc, organizační složka", "CITICZPX"),
    "2700": ("UniCredit Bank Czech Republic and Slovakia, a.s.", "BACXCZPP"),
    "3030": ("Air Bank a.s.", "AIRACZPP"),
    "3060": ("PKO BP S.A., Czech Branch", "BPKOCZPP"),
    "3500": ("ING Bank N.V.", "INGBCZPP"),
    "4300": ("Národní rozvojová banka, a.s.", "NROZCZPP"),
    "5500": ("Raiffeisenbank a.s.", "RZBCCZPP"),
    "5800": ("J&T BANKA, a.s.", "JTBPCZPP"),
    "6000": ("PPF banka a.s.", "PMBPCZPP"),
    "6200": ("COMMERZBANK Aktiengesellschaft, pobočka Praha", "COBACZPX"),
    "6210": ("mBank S.A., organizační složka", "BREXCZPP"),
    "6300": ("BNP Paribas S.A., pobočka Česká republika", "GEBACZPP"),
    "6363": ("Partners Banka, a.s.", "-"),
    "6700": ("Všeobecná úverová banka a.s., pobočka Praha", "SUBACZPP"),
    "6800": ("Sberbank CZ, a.s. v likvidaci", "VBOECZ2X"),
    "7910": ("Deutsche Bank Aktiengesellschaft Filiale Prag, organizační složka", "DEUTCZPX"),
    "7950": ("Raiffeisen stavební spořitelna a.s.", "-"),
    "7960": ("ČSOB Stavební spořitelna, a.s.", "-"),
    "7970": ("MONETA Stavební Spořitelna, a.s.", "-"),
    "7990": ("Modrá pyramida stavební spořitelna, a.s.", "-"),
    "8030": ("Volksbank Raiffeisenbank Nordoberpfalz eG pobočka Cheb", "GENOCZ21"),
    "8040": ("Oberbank AG pobočka Česká republika", "OBKLCZ2X"),
    "8060": ("Stavební spořitelna České spořitelny, a.s.", "-"),
    "8090": ("Česká exportní banka, a.s.", "CZEECZPP"),
    "8150": ("HSBC Continental Europe, Czech Republic", "MIDLCZPP"),
    "8190": ("Sparkasse Oberlausitz-Niederschlesien", "-"),
    "8198": ("FAS finance company s.r.o.", "FFCSCZP1"),
    "8220": ("Payment execution s.r.o.", "PAERCZP1"),
    "8250": ("Bank of China (CEE) Ltd. Prague Branch", "BKCHCZPP"),
    "8255": ("Bank of Communications Co., Ltd., Prague Branch odštěpný závod", "COMMCZPP"),
    "8265": ("Industrial and Commercial Bank of China Limited, Prague Branch, odštěpný závod", "ICBKCZPP"),
    "8500": ("Multitude Bank p.l.c.", "-")
}

# source: https://www.swift.com/sites/default/files/files/iban-registry_1.txt
IBAN_LENGTHS = {
    'AD': 24, 'AE': 23, 'AL': 28, 'AT': 20, 'AZ': 28, 'BA': 20, 'BE': 16, 'BG': 22, 'BH': 22,
    'BI': 27, 'BR': 29, 'BY': 28, 'CH': 21, 'CR': 22, 'CY': 28, 'CZ': 24, 'DE': 22, 'DJ': 27,
    'DK': 18, 'DO': 28, 'EE': 20, 'EG': 29, 'ES': 24, 'FI': 18, 'FK': 18, 'FO': 18, 'FR': 27,
    'GB': 22, 'GE': 22, 'GI': 23, 'GL': 18, 'GR': 27, 'GT': 28, 'HN': 28, 'HR': 21, 'HU': 28,
    'IE': 22, 'IL': 23, 'IQ': 23, 'IS': 26, 'IT': 27, 'JO': 30, 'KW': 30, 'KZ': 20, 'LB': 28,
    'LC': 32, 'LI': 21, 'LT': 20, 'LU': 20, 'LV': 21, 'LY': 25, 'MC': 27, 'MD': 24, 'ME': 22,
    'MK': 19, 'MN': 20, 'MR': 27, 'MT': 31, 'MU': 30, 'NI': 28, 'NL': 18, 'NO': 15, 'OM': 23,
    'PK': 24, 'PL': 28, 'PS': 29, 'PT': 25, 'QA': 29, 'RO': 24, 'RS': 22, 'RU': 33, 'SA': 24,
    'SC': 31, 'SD': 18, 'SE': 24, 'SI': 19, 'SK': 24, 'SM': 27, 'SO': 23, 'ST': 25, 'SV': 28,
    'TL': 23, 'TN': 24, 'TR': 26, 'UA': 29, 'VA': 22, 'VG': 24, 'XK': 20, 'YE': 30
}


def validate_iban(acc: str) -> bool:
    acc = acc.replace(' ', '').upper()

    # Check basic format
    if not re.match(r'^[A-Z0-9]+$', acc):
        return False

    # Check country code and length
    country_code = acc[:2]
    if country_code not in IBAN_LENGTHS or len(acc) != IBAN_LENGTHS[country_code]:
        return False

    # Rearrange and convert letters to numbers
    rearranged = acc[4:] + acc[:4]
    numeric_iban = ''
    for char in rearranged:
        if char.isdigit():
            numeric_iban += char
        else:
            numeric_iban += str(ord(char) - 55)  # A=10, B=11, ..., Z=35

    # Perform mod-97 check
    remainder = int(numeric_iban[:9]) % 97
    for i in range(9, len(numeric_iban), 7):
        remainder = int(str(remainder) + numeric_iban[i:i + 7]) % 97

    return remainder == 1


def validate_mod11(number: str) -> bool:
    """Validate a number using the Czech Modulo 11 algorithm.
        https://www.penize.cz/osobni-ucty/424173-tajemstvi-cisla-uctu-klicem-pro-banky-je-11
        https://www.cnb.cz/export/sites/cnb/cs/platebni-styk/.galleries/pravni_predpisy/download/vyhl_169_2011.pdf
    """
    weights = [1, 2, 4, 8, 5, 10, 9, 7, 3, 6]
    total = sum(int(digit) * weight for digit, weight in zip(reversed(number), weights))
    return total % 11 == 0


def generate_czech_iban(bank_code, account_number):
    """
    Generate a Czech IBAN from bank code and account number.
    """
    country_code = "CZ"

    # Ensure the account number is properly formatted (prefix + main account number)
    # Czech account numbers can have up to 6 digits for the prefix and 10 digits for the main account number
    # If the account number is shorter, pad it with zeros
    account_number = account_number.zfill(16)  # Total length of prefix + account number is 16

    # Step 1: Create the basic IBAN structure without check digits
    bban = bank_code + account_number
    iban_without_checksum = country_code + "00" + bban

    # Step 2: Move the first 4 characters to the end
    iban_rearranged = iban_without_checksum[4:] + iban_without_checksum[:4]

    # Step 3: Convert letters to numbers (A=10, B=11, ..., Z=35)
    iban_numeric = ""
    for char in iban_rearranged:
        if char.isalpha():
            iban_numeric += str(ord(char.upper()) - 55)
        else:
            iban_numeric += char

    # Step 4: Calculate the check digits (98 - (iban_numeric % 97))
    check_digits = 98 - (int(iban_numeric) % 97)
    check_digits = f"{check_digits:02d}"  # Ensure it's 2 digits

    # Step 5: Construct the final IBAN
    iban = country_code + check_digits + bban
    return iban


def extract_czech_bank_and_account(iban):
    """
    Extract the bank code and account number from a Czech IBAN.
    """
    # Remove non-alphanumeric characters
    iban = re.sub(r"[^a-zA-Z0-9]", "", iban)

    # Validate length (Czech IBANs are 24 characters long)
    if len(iban) != 24:
        raise ValueError("Invalid Czech IBAN length. Expected 24 characters.")

    # Extract components
    bank_code = iban[4:8]  # Bank code is 4 digits
    account_number = iban[8:].lstrip('0')  # Account number is 16 digits (prefix + main account number)
    # if len(account_number) > 10:
    #     account_number = f"{account_number[:-10]}-{account_number[-10:]}"

    return bank_code, account_number
    
