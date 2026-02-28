"""Python library to parse and format musical key notation and convert between Camelot key notation"""

import typing as t
import re
from dataclasses import dataclass


# Do not add type annotation here; hatch won't parse it then
__VERSION__ = '0.1.0'


CAMELOT_TO_MUSICAL = {
    (12, 'B'): 'EM',
    (1, 'B'): 'BM',
    (2, 'B'): 'F#M',
    (3, 'B'): 'DbM',
    (4, 'B'): 'AbM',
    (5, 'B'): 'EbM',
    (6, 'B'): 'BbM',
    (7, 'B'): 'FM',
    (8, 'B'): 'CM',
    (9, 'B'): 'GM',
    (10, 'B'): 'DM',
    (11, 'B'): 'AM',
    (12, 'A'): 'Dbm',
    (1, 'A'): 'Abm',
    (2, 'A'): 'Ebm',
    (3, 'A'): 'Bbm',
    (4, 'A'): 'Fm',
    (5, 'A'): 'Cm',
    (6, 'A'): 'Gm',
    (7, 'A'): 'Dm',
    (8, 'A'): 'Am',
    (9, 'A'): 'Em',
    (10, 'A'): 'Bm',
    (11, 'A'): 'F#m',
}
"""Mapping of camelot key number/letter pairs to musical key"""

MUSICAL_TO_CAMELOT = {v: k for k, v in CAMELOT_TO_MUSICAL.items()}
"""Mapping of musical key to camelot key number/letter pairs (inverse of `CAMELOT_TO_MUSICAL`)"""

MUSICAL_LONG = {
    'EM': {'letter': 'E', 'sharp': False, 'flat': False, 'type': 'major'},
    'BM': {'letter': 'B', 'sharp': False, 'flat': False, 'type': 'major'},
    'F#M': {'letter': 'F', 'sharp': True, 'flat': False, 'type': 'major'},
    'DbM': {'letter': 'D', 'sharp': False, 'flat': True, 'type': 'major'},
    'AbM': {'letter': 'A', 'sharp': False, 'flat': True, 'type': 'major'},
    'EbM': {'letter': 'E', 'sharp': False, 'flat': True, 'type': 'major'},
    'BbM': {'letter': 'B', 'sharp': False, 'flat': True, 'type': 'major'},
    'FM': {'letter': 'F', 'sharp': False, 'flat': False, 'type': 'major'},
    'CM': {'letter': 'C', 'sharp': False, 'flat': False, 'type': 'major'},
    'GM': {'letter': 'G', 'sharp': False, 'flat': False, 'type': 'major'},
    'DM': {'letter': 'D', 'sharp': False, 'flat': False, 'type': 'major'},
    'AM': {'letter': 'A', 'sharp': False, 'flat': False, 'type': 'major'},
    'Dbm': {'letter': 'D', 'sharp': False, 'flat': True, 'type': 'minor'},
    'Abm': {'letter': 'A', 'sharp': False, 'flat': True, 'type': 'minor'},
    'Ebm': {'letter': 'E', 'sharp': False, 'flat': True, 'type': 'minor'},
    'Bbm': {'letter': 'B', 'sharp': False, 'flat': True, 'type': 'minor'},
    'Fm': {'letter': 'F', 'sharp': False, 'flat': False, 'type': 'minor'},
    'Cm': {'letter': 'C', 'sharp': False, 'flat': False, 'type': 'minor'},
    'Gm': {'letter': 'G', 'sharp': False, 'flat': False, 'type': 'minor'},
    'Dm': {'letter': 'D', 'sharp': False, 'flat': False, 'type': 'minor'},
    'Am': {'letter': 'A', 'sharp': False, 'flat': False, 'type': 'minor'},
    'Em': {'letter': 'E', 'sharp': False, 'flat': False, 'type': 'minor'},
    'Bm': {'letter': 'B', 'sharp': False, 'flat': False, 'type': 'minor'},
    'F#m': {'letter': 'F', 'sharp': True, 'flat': False, 'type': 'minor'},
}
"""'Long' format for short musical key representations, can be passed to `Key()`"""

CAMELOT_COLORS = {
    12: {
        'B': '#1de9e6',
        'A': '#4befec',
    },
    1: {
        'B': '#1eedbe',
        'A': '#4cf1d2',
    },
    2: {
        'B': '#38f06e',
        'A': '#6ff49a',
    },
    3: {
        'B': '#78f53e',
        'A': '#a1f876',
    },
    4: {
        'B': '#d7c160',
        'A': '#e2d390',
    },
    5: {
        'B': '#fd8d69',
        'A': '#fbb197',
    },
    6: {
        'B': '#fd7082',
        'A': '#fb9da9',
    },
    7: {
        'B': '#fd67a5',
        'A': '#fb96c1',
    },
    8: {
        'B': '#e867d0',
        'A': '#ed96de',
    },
    9: {
        'B': '#c274ff',
        'A': '#d4a0fd',
    },
    10: {
        'B': '#8ea4ff',
        'A': '#b1c0fd',
    },
    11: {
        'B': '#4ad1f8',
        'A': '#7edff8',
    },
}
"""Colors representing camelot key pairs"""

ALTERNATE_KEYS = {
    ('C', False, True): {'letter': 'B', 'sharp': False, 'flat': False},
    ('C', True, False): {'letter': 'D', 'sharp': False, 'flat': True},
    ('D', False, True): {'letter': 'C', 'sharp': True, 'flat': False},
    ('D', True, False): {'letter': 'E', 'sharp': False, 'flat': True},
    ('E', False, True): {'letter': 'D', 'sharp': True, 'flat': False},
    ('E', True, False): {'letter': 'F', 'sharp': False, 'flat': False},
    ('F', False, True): {'letter': 'E', 'sharp': False, 'flat': False},
    ('F', True, False): {'letter': 'G', 'sharp': False, 'flat': True},
    ('G', False, True): {'letter': 'F', 'sharp': True, 'flat': False},
    ('G', True, False): {'letter': 'A', 'sharp': False, 'flat': True},
    ('A', False, True): {'letter': 'G', 'sharp': True, 'flat': False},
    ('A', True, False): {'letter': 'B', 'sharp': False, 'flat': True},
    ('B', False, True): {'letter': 'A', 'sharp': True, 'flat': False},
    ('B', True, False): {'letter': 'C', 'sharp': False, 'flat': False},
}
"""Alternate key mapping, keys that can be represented differently but are the same note"""


@dataclass(frozen=True)
class Key:
    """\
    Represents a musical/camelot key.  Keys are immutable and hashable, and can
    be compared and sorted.
    """

    letter: t.Literal['A', 'B', 'C', 'D', 'E', 'F', 'G'] = None
    """Musical key letter"""
    sharp: bool = False
    """Whether the key is sharp"""
    flat: bool = False
    """Whether the key is flat"""
    type: t.Literal['major', 'minor'] = 'major'
    """Chord type - major or minor"""
    key: str = None
    """'Short' representation of the musical key, like 'F#m'"""
    camelot_number: t.Optional[t.Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]] = None
    """Number for the camelot key"""
    camelot_letter: t.Optional[t.Literal['A', 'B']] = None
    """Letter for the camelot key"""
    camelot_color: t.Optional[str] = None
    """Color to use for displaying the camelot key"""

    def __post_init__parse(self):
        """\
        On init, ensure we have musical key information.  If it was provided
        then we're fine; otherwise attempt to get it from the camelot key.  If
        no camelot key was provided in that case, it's an error.
        """

        if self.letter is None:
            if self.camelot_number is None or self.camelot_letter is None:
                raise ValueError("No key information provided")
            short_key = CAMELOT_TO_MUSICAL.get((self.camelot_number, self.camelot_letter))
            if not short_key:
                raise ValueError("No valid key information provided")
            long_key = MUSICAL_LONG.get(short_key)
            if not long_key:
                raise ValueError("No valid key information provided")
            for k, v in long_key.items():
                super().__setattr__(k, v)

        if self.sharp and self.flat:
            super().__setattr__('flat', False)

    def __post_init__key(self):
        """\
        On init, generate the short key representation/string representation
        from the musical key information.
        """

        if self.key is None:
            parts = [self.letter]

            if self.sharp:
                parts.append('#')
            elif self.flat:
                parts.append('b')

            if self.type == 'major' or not self.type:
                parts.append('M')
            elif self.type == 'minor':
                parts.append('m')

            super().__setattr__('key', ''.join(parts))

    def __post_init__camelot(self):
        """\
        On init, generate the camelot key information from the musical key
        information if possible.
        """

        if self.camelot_number is None or self.camelot_letter is None:
            for alt_key in self.alternate_keys:
                res = MUSICAL_TO_CAMELOT.get(alt_key.key)
                if res:
                    n, l = res
                    super().__setattr__('camelot_number', n)
                    super().__setattr__('camelot_letter', l)
                    break
        if self.camelot_color is None and self.camelot_number and self.camelot_letter:
            c = CAMELOT_COLORS.get(self.camelot_number, {}).get(self.camelot_letter)
            super().__setattr__('camelot_color', c)

    def __post_init__validate(self):
        """\
        On init, validate that the data in the class instance is actually valid.
        In some cases an exception might have been thrown earlier.
        """

        if self.letter is None:
            raise TypeError("letter must be present")
        if not isinstance(self.letter, str):
            raise TypeError("letter must be a string")
        if self.letter not in ('A', 'B', 'C', 'D', 'E', 'F', 'G'):
            raise ValueError("letter must be in A-G")

        if self.sharp not in (True, False):
            raise TypeError("sharp must be True or False")
        if self.flat not in (True, False):
            raise TypeError("flat must be True or False")
        if self.sharp and self.flat:
            raise ValueError("Only one of sharp or flat may be True")

        if self.type is None:
            raise TypeError("type must be present")
        if not isinstance(self.type, str):
            raise TypeError("type must be a string")
        if self.type not in ('major', 'minor'):
            raise ValueError("type must be major or minor")

        if self.key is None:
            raise TypeError("key must be present")
        if not isinstance(self.key, str):
            raise TypeError("key must be a string")

        if self.camelot_number or self.camelot_letter:
            if self.camelot_number is None or self.camelot_letter is None:
                raise ValueError("Both camelot_number and camelot_letter must be provided together")
            if not isinstance(self.camelot_number, int):
                raise TypeError("camelot_number must be an int")
            if self.camelot_number < 1 or self.camelot_number > 12:
                raise ValueError("camelot_number must be in 1-12")
            if not isinstance(self.camelot_letter, str):
                raise TypeError("camelot_letter must be a string")
            if self.camelot_letter not in ('A', 'B'):
                raise ValueError("camelot_letter must be A or B")

    def __post_init__(self):
        """\
        Run all post init tasks.  This ensures the resulting object has all of
        the data that we can determine from the given arguments, or raises an
        error if (somewhat) invalid data was provided.
        """

        self.__post_init__parse()
        self.__post_init__key()
        self.__post_init__camelot()
        self.__post_init__validate()

    @property
    def camelot_key(self) -> t.Optional[str]:
        """\
        Convert the camelot number and letter to a string representation, if
        both the number and letter are present.  If either are not present,
        returns None
        """

        if self.camelot_number and self.camelot_letter:
            return f'{self.camelot_number}{self.camelot_letter}'

    def __str__(self) -> str:
        """\
        String representation of the key, returns the short key and the camelot
        key if available.
        """

        out = self.key
        ck = self.camelot_key
        if ck:
            out = f'{out} ({ck})'
        return out

    def __hash__(self):
        """\
        Hash that is used to compare/uniquely identify a key.

        Note that two different keys representing the same note (i.e. F#/Gb) do
        not produce the same hash value; the properties must be the same
        """

        return hash((self.letter, self.sharp, self.flat, self.type))

    def __eq__(self, other: t.Self) -> bool:
        """\
        Compare two keys to see if they are the same.  Generally, two keys are
        the same if the musical key properties (letter, sharp/flat, type) are
        the same, however two keys representing the same note (i.e. F#/Gb) are
        also considered to be the same if the chord type is the same.
        """

        if isinstance(other, Key):
            for other_alt in other.alternate_keys:
                if hash(self) == hash(other_alt):
                    return True
        return False

    def __ne__(self, other: t.Self) -> bool:
        return not self.__eq__(other)

    @property
    def _camelot_key_number_repr(self) -> float:
        """\
        Return a numerical representation of the camelot key, for internal
        usage.  This numerical representation is sortable, in particular
        ensuring that the numbers sort in order, as do the letters (ex. 1A < 1B,
        1B < 2A, etc).

        For keys that do not have a camelot key, they are sorted first.

        The use case here is primarily implementing comparison outside of'
        equality, for sorting.
        """

        out = -1.0
        if self.camelot_number and self.camelot_letter:
            out = float(self.camelot_number)
            if self.camelot_letter == 'B':
                out += 0.5
        return out
    

    def __lt__(self, other: t.Self) -> bool:
        if not isinstance(other, Key):
            raise ValueError("Uncomparable types")
        return self._camelot_key_number_repr < other._camelot_key_number_repr

    def __le__(self, other: t.Self) -> bool:
        if not isinstance(other, Key):
            raise ValueError("Uncomparable types")
        return self._camelot_key_number_repr <= other._camelot_key_number_repr

    def __gt__(self, other: t.Self) -> bool:
        if not isinstance(other, Key):
            raise ValueError("Uncomparable types")
        return self._camelot_key_number_repr > other._camelot_key_number_repr

    def __ge__(self, other: t.Self) -> bool:
        if not isinstance(other, Key):
            raise ValueError("Uncomparable types")
        return self._camelot_key_number_repr >= other._camelot_key_number_repr

    @property
    def alternate_keys(self) -> t.Generator[t.Self, None, None]:
        """\
        Produce alternate keys that are technically the same key as this one.
        The current object is always produced as it is always the same, and if
        another key that is the same exists it is also produced.

        Examples:
          * F# is also Gb
          * C# is also Db
          * E# is also F (uncommon but not technically wrong...)
        """

        yield self
        alt = ALTERNATE_KEYS.get((self.letter, self.sharp, self.flat))
        if alt:
            yield self.__class__(**alt, type=self.type)

    def _copy(self, **kwargs) -> t.Self:
        """\
        Create a copy of the current object with updated properties from kwargs.
        If kwargs contains camelot key information, the musical key information
        is discarded and only camelot key is used to construct the new instance,
        and vice versa - if musical key information is provided, camelot key
        information is discarded.

        If no kwargs are given, the musical key information is used.
        """

        camelot_args = ('camelot_number', 'camelot_letter')
        musical_args = ('letter', 'sharp', 'flat', 'type')

        new_args = {
            'letter': self.letter,
            'sharp': self.sharp,
            'flat': self.flat,
            'type': self.type,
            'camelot_number': self.camelot_number,
            'camelot_letter': self.camelot_letter,
        }

        if any(((k in kwargs) for k in camelot_args)):
            for k in musical_args:
                del new_args[k]
        else:
            for k in camelot_args:
                del new_args[k]
        new_args.update(kwargs)
        return Key(**new_args)

    def shift(self, n: int):
        """\
        Shift the key by N steps on the camelot wheel/circle of fifths,
        returning a new Key object.  If the current instance does not have
        camelot key information, raises an error.

        .. important:: Note that this is NOT equivalent to a key shift such as you may find in DJ software - where key shifting is done by note (for example shifing CM up by 1 results in C#M), but rather by the adjacent key on the circle of fifths (shifting CM up by 1 results in FM).

        .. tip:: To shift by adjacent notes, use a factor of 5.
        """

        if not (self.camelot_number and self.camelot_letter):
            raise ValueError("Missing camelot key information")

        return self._copy(camelot_number=((self.camelot_number + n) % 12) or 12)

    def get_adjacent_keys(self, n: int=1) -> t.Generator[t.Tuple[int, t.Self], None, None]:
        """\
        Get keys adjacent to this key on the circle of fifths, along with the
        number of steps by which that key must be shifted to be adjacent.  When
        n>1 is passed, consider keys that are not immediately adjacent.  If n=1,
        only immediately adjacent keys are considered and the number of steps to
        shift is always 0.

        In terms of the camelot wheel, for example:
        Given a key 3A, adjacent keys are 3A (same), 3B (same, but major instead
        of minor scale), 2A, and 4A.  For all of these the shift value is 0.
        With n=2, additional adjacent keys would include:

          * 3A +/- 5: (-1, 8A), (+1, 10A)
          * 3B +/- 5: (-1, 8B), (+1, 10B)
          * 4A +/- 5: (-1, 9A), (+1, 11A)
          * 2A +/- 5: (-1, 7A), (+1, 9A)

        Generated values are a tuple of (shift, key)

        .. note:: Nothing is generated if this instance does not have camelot key information
        .. note:: The results are not in any particular order (there is a deterministic order but it does not have any meaning) but are sortable; sorting without any key results in a list sorted by shift distance, then camelot number & letter
        """

        if self.camelot_number and self.camelot_letter:
            this_key = self
            this_alt_key = self._copy(camelot_letter='B' if self.camelot_letter == 'A' else 'A')
            this_adj_prev = self.shift(-1)
            this_adj_next = self.shift(1)
            # This key
            yield 0, this_key
            # Alternate key - major vs. minor
            yield 0, this_alt_key
            # Previous # on the camelot wheel, same scale
            yield 0, this_adj_prev
            # Next # on the camelot wheel, same scale
            yield 0, this_adj_next

            for i in range(2, n + 1):
                diff = i - 1
                shift = diff * 5
                # Produce the alternate key first - when shifted by N these keys will be exactly the alternate key
                yield -diff, this_alt_key.shift(shift)
                yield diff, this_alt_key.shift(-shift)
                # Then keys that when shifted become the current key, or an ajacent key
                yield -diff, this_key.shift(shift)
                yield diff, this_key.shift(-shift)
                yield -diff, this_adj_prev.shift(shift)
                yield diff, this_adj_prev.shift(-shift)
                yield -diff, this_adj_next.shift(shift)
                yield diff, this_adj_next.shift(-shift)


def _parse_beatport__musical(value: t.Dict[str, t.Any]) -> t.Optional[Key]:
    """\
    Return a Key instance for a key dictionary as returned by Beatport's API, if
    possible.
    """

    try:
        return Key(
            letter=value['letter'],
            sharp=value['is_sharp'],
            flat=value['is_flat'],
            type=value['chord_type']['name'].lower(),
        )
    except KeyError:
        pass


def _parse_beatport__camelot(value: t.Dict[str, t.Any]) -> t.Optional[Key]:
    """\
    Return a Key instance for a camelot key dictionary as returned by Beatport's
    API, if possible.
    """

    try:
        number = int(value['camelot_number'])
        letter = value['camelot_letter'].upper()
    except (TypeError, ValueError, KeyError):
        pass
    else:
        return Key(camelot_number=number, camelot_letter=letter)


def _parse_str__musical(value: str) -> t.Optional[Key]:
    """\
    Return a Key instance for a musical key as a string, if possible.
    """

    match = re.match(r'''
        ^
        # Letter key - should be uppercase, but check lowercase too
        ([A-Ga-g])\s*
        # Sharp/flat, optional
        ([#b])?\s*
        # Major/minor spec
        (
            # Full words
            (?:[mM](?:ajor|inor))
            # Short form
            |(?:[mM](?:aj|in))
            # Very short form
            |(?:[mM])
        )?
        $
    ''', str(value).strip(), re.X)
    if match:
        letter, sharpflat, type_ = match.groups()
        if not letter:
            return

        if type_:
            if type_ == 'M':
                type_ = 'major'
            elif type_ == 'm' or type_.lower().startswith('min'):
                type_ = 'minor'
            else:
                type_ = 'major'
        else:
            type_ = 'major'

        return Key(
            letter=letter.upper(),
            sharp=sharpflat == '#',
            flat=sharpflat == 'b',
            type=type_,
        )


def _parse_str__camelot(value: str) -> t.Optional[Key]:
    """\
    Return a Key instance for a camelot key as a string, if possible.
    """

    letter = number = None
    try:
        value = value.upper().strip().replace(' ', '')
        if len(value) > 1 and len(value) < 4:
            letter = value[-1:]
            number = int(value[:-1])
    except (TypeError, ValueError, AttributeError):
        pass
    else:
        if letter and number:
            return Key(camelot_number=number, camelot_letter=letter)



def parse(value: t.Union[str, t.Dict[str, t.Any]]) -> t.Optional[Key]:
    """\
    Parse a value representing a musical key into a Key instance, if possible.
    Automatically determines the format and parses the data, returning None if a
    key could not be determined.  Input formats may include:

    **Beatport API - musical key**
    ```
    {
        'letter': 'C',
        'is_sharp': True,
        'is_flat': False,
        'chord_type': {'name': 'minor'},
    }
    ```

    **Beatport API - camelot key**
    ```
    {
        'camelot_number': 12,
        'camelot_letter': 'B',
    }
    ```

    **Musical Key - string:** `C#m`, `C # Minor`, etc

    **Camelot Key - string:** `12B`
    """

    if isinstance(value, str):
        res = _parse_str__musical(value)
        if res is not None:
            return res

        res = _parse_str__camelot(value)
        if res is not None:
            return res
    else:
        res = _parse_beatport__musical(value)
        if res is not None:
            return res

        res = _parse_beatport__camelot(value)
        if res is not None:
            return res
