from unittest import TestCase
from unittest.mock import MagicMock, patch, call, ANY

from src.camelot_key import Key


@patch('src.camelot_key.Key.__post_init__')
class TestKey_Init_PostInitParse(TestCase):
    def test_post_init_parse__no_letter_no_camelot(self, mock_post_init):
        k = Key()
        with self.assertRaisesRegex(ValueError, 'No key information'):
            k._Key__post_init__parse()

    def test_post_init_parse__no_letter_no_camelot_number(self, mock_post_init):
        k = Key(camelot_letter='B')
        with self.assertRaisesRegex(ValueError, 'No key information'):
            k._Key__post_init__parse()

    def test_post_init_parse__no_letter_no_camelot_letter(self, mock_post_init):
        k = Key(camelot_number=3)
        with self.assertRaisesRegex(ValueError, 'No key information'):
            k._Key__post_init__parse()

    def test_post_init_parse__no_letter_invalid_camelot_number(self, mock_post_init):
        k = Key(camelot_number=99, camelot_letter='B')
        with self.assertRaisesRegex(ValueError, 'No valid key information'):
            k._Key__post_init__parse()

    def test_post_init_parse__no_letter_invalid_camelot_letter(self, mock_post_init):
        k = Key(camelot_number=3, camelot_letter='X')
        with self.assertRaisesRegex(ValueError, 'No valid key information'):
            k._Key__post_init__parse()

    @patch('src.camelot_key.MUSICAL_LONG', {})
    def test_post_init_parse__no_letter_invalid_camelot_key(self, mock_post_init):
        k = Key(camelot_number=3, camelot_letter='B')
        with self.assertRaisesRegex(ValueError, 'No valid key information'):
            k._Key__post_init__parse()

    def test_post_init_parse__no_letter(self, mock_post_init):
        k = Key(camelot_number=3, camelot_letter='B')
        k._Key__post_init__parse()
        self.assertEqual(k.camelot_number, 3)
        self.assertEqual(k.camelot_letter, 'B')
        self.assertIsNone(k.camelot_color)
        self.assertIsNone(k.key)
        self.assertEqual(k.letter, 'D')
        self.assertFalse(k.sharp)
        self.assertTrue(k.flat)
        self.assertEqual(k.type, 'major')

    def test_post_init_parse__sharp_and_flat(self, mock_post_init):
        k = Key(letter='D', sharp=True, flat=True)
        k._Key__post_init__parse()
        self.assertTrue(k.sharp)
        self.assertFalse(k.flat)

    def test_post_init_parse__sharp(self, mock_post_init):
        k = Key(letter='D', sharp=True, flat=False)
        k._Key__post_init__parse()
        self.assertTrue(k.sharp)
        self.assertFalse(k.flat)

    def test_post_init_parse__flat(self, mock_post_init):
        k = Key(letter='D', sharp=False, flat=True)
        k._Key__post_init__parse()
        self.assertFalse(k.sharp)
        self.assertTrue(k.flat)

    def test_post_init_parse__normal(self, mock_post_init):
        k = Key(letter='D')
        k._Key__post_init__parse()
        self.assertFalse(k.sharp)
        self.assertFalse(k.flat)


@patch('src.camelot_key.Key.__post_init__')
class TestKey_Init_PostInitKey(TestCase):
    def test_post_init_key__letter(self, mock_post_init):
        k = Key(letter='D')
        k._Key__post_init__key()
        self.assertEqual(k.key, 'DM')

    def test_post_init_key__letter_maj(self, mock_post_init):
        k = Key(letter='D', type='major')
        k._Key__post_init__key()
        self.assertEqual(k.key, 'DM')

    def test_post_init_key__letter_min(self, mock_post_init):
        k = Key(letter='D', type='minor')
        k._Key__post_init__key()
        self.assertEqual(k.key, 'Dm')

    def test_post_init_key__letter_sharpflat(self, mock_post_init):
        k = Key(letter='D', sharp=True, flat=True)
        k._Key__post_init__key()
        self.assertEqual(k.key, 'D#M')

    def test_post_init_key__letter_sharp(self, mock_post_init):
        k = Key(letter='D', sharp=True)
        k._Key__post_init__key()
        self.assertEqual(k.key, 'D#M')

    def test_post_init_key__letter_flat(self, mock_post_init):
        k = Key(letter='D', flat=True)
        k._Key__post_init__key()
        self.assertEqual(k.key, 'DbM')

    def test_post_init_key__letter_min_sharp(self, mock_post_init):
        k = Key(letter='D', type='minor', sharp=True)
        k._Key__post_init__key()
        self.assertEqual(k.key, 'D#m')

    def test_post_init_key__letter_min_flat(self, mock_post_init):
        k = Key(letter='D', type='minor', flat=True)
        k._Key__post_init__key()
        self.assertEqual(k.key, 'Dbm')

    def test_post_init_key__exists(self, mock_post_init):
        k = Key(letter='D', key='Am')
        k._Key__post_init__key()
        self.assertEqual(k.key, 'Am')


@patch('src.camelot_key.Key.__post_init__')
class TestKey_Init_PostInitCamelot(TestCase):
    @patch('src.camelot_key.Key.alternate_keys', [MagicMock(key='foo'), MagicMock(key='bar')])
    def test_post_init_camelot__no_valid_alt_keys(self, mock_post_init):
        k = Key(letter='E', flat=True)
        k._Key__post_init__key()
        k._Key__post_init__camelot()
        self.assertIsNone(k.camelot_number)
        self.assertIsNone(k.camelot_letter)
        self.assertIsNone(k.camelot_color)

    @patch('src.camelot_key.CAMELOT_COLORS', {})
    def test_post_init_camelot__no_valid_color(self, mock_post_init):
        k = Key(letter='E', flat=True)
        k._Key__post_init__key()
        k._Key__post_init__camelot()
        self.assertEqual(k.camelot_number, 5)
        self.assertEqual(k.camelot_letter, 'B')
        self.assertIsNone(k.camelot_color)

    def test_post_init_camelot__valid(self, mock_post_init):
        k = Key(letter='E', flat=True)
        k._Key__post_init__key()
        # import pdb;pdb.set_trace()
        k._Key__post_init__camelot()
        self.assertEqual(k.camelot_number, 5)
        self.assertEqual(k.camelot_letter, 'B')
        self.assertIsNotNone(k.camelot_color)

    def test_post_init_camelot__already_set(self, mock_post_init):
        k = Key(letter='E', flat=True, camelot_number=5, camelot_letter='B')
        k._Key__post_init__key()
        k._Key__post_init__camelot()
        self.assertEqual(k.camelot_number, 5)
        self.assertEqual(k.camelot_letter, 'B')
        self.assertIsNotNone(k.camelot_color)

    def test_post_init_camelot__already_set_with_color(self, mock_post_init):
        k = Key(letter='E', flat=True, camelot_number=5, camelot_letter='B', camelot_color='foo')
        k._Key__post_init__key()
        k._Key__post_init__camelot()
        self.assertEqual(k.camelot_number, 5)
        self.assertEqual(k.camelot_letter, 'B')
        self.assertEqual(k.camelot_color, 'foo')


@patch('src.camelot_key.Key.__post_init__')
class TestKey_Init_PostInitValidate(TestCase):
    def test_post_init_validate__letter(self, mock_post_init):
        with self.assertRaisesRegex(TypeError, 'letter must be present'):
            k = Key()
            k._Key__post_init__validate()

        with self.assertRaisesRegex(TypeError, 'letter must be a string'):
            k = Key(letter=7)
            k._Key__post_init__validate()

        with self.assertRaisesRegex(ValueError, 'letter must be in'):
            k = Key(letter='X')
            k._Key__post_init__validate()

    def test_post_init_validate__sharp_flat(self, mock_post_init):
        with self.assertRaisesRegex(TypeError, 'sharp must be True'):
            k = Key(letter='G', sharp='foo')
            k._Key__post_init__validate()

        with self.assertRaisesRegex(TypeError, 'flat must be True'):
            k = Key(letter='G', flat='foo')
            k._Key__post_init__validate()

        with self.assertRaisesRegex(ValueError, 'one of'):
            k = Key(letter='G', sharp=True, flat=True)
            k._Key__post_init__validate()

    def test_post_init_validate__type(self, mock_post_init):
        with self.assertRaisesRegex(TypeError, 'type must be present'):
            k = Key(letter='G', type=None)
            k._Key__post_init__validate()

        with self.assertRaisesRegex(TypeError, 'type must be a string'):
            k = Key(letter='G', type=7)
            k._Key__post_init__validate()

        with self.assertRaisesRegex(ValueError, 'type must be major'):
            k = Key(letter='G', type='foo')
            k._Key__post_init__validate()

    def test_post_init_validate__key(self, mock_post_init):
        with self.assertRaisesRegex(TypeError, 'key must be present'):
            k = Key(letter='G')
            k._Key__post_init__validate()

        with self.assertRaisesRegex(TypeError, 'key must be a string'):
            k = Key(letter='G', key=7)
            k._Key__post_init__validate()

    def test_post_init_validate__camelot_presence(self, mock_post_init):
        with self.assertRaisesRegex(ValueError, 'provided together'):
            k = Key(letter='G', key='foo', camelot_number=3)
            k._Key__post_init__validate()

        with self.assertRaisesRegex(ValueError, 'provided together'):
            k = Key(letter='G', key='foo', camelot_letter='B')
            k._Key__post_init__validate()

    def test_post_init_validate__camelot_number(self, mock_post_init):
        with self.assertRaisesRegex(TypeError, 'must be an int'):
            k = Key(letter='G', key='foo', camelot_number='foo', camelot_letter='B')
            k._Key__post_init__validate()

        with self.assertRaisesRegex(ValueError, 'must be in'):
            k = Key(letter='G', key='foo', camelot_number=0, camelot_letter='B')
            k._Key__post_init__validate()

        with self.assertRaisesRegex(ValueError, 'must be in'):
            k = Key(letter='G', key='foo', camelot_number=13, camelot_letter='B')
            k._Key__post_init__validate()

    def test_post_init_validate__camelot_letter(self, mock_post_init):
        with self.assertRaisesRegex(TypeError, 'must be a str'):
            k = Key(letter='G', key='foo', camelot_number=3, camelot_letter=7)
            k._Key__post_init__validate()

        with self.assertRaisesRegex(ValueError, 'must be A'):
            k = Key(letter='G', key='foo', camelot_number=3, camelot_letter='X')
            k._Key__post_init__validate()

    def test_post_init_validate__success_maj(self, mock_post_init):
        k = Key(letter='G', key='foo', camelot_number=3, camelot_letter='B')
        self.assertEqual(k.letter, 'G')
        self.assertEqual(k.type, 'major')
        self.assertEqual(k.key, 'foo')
        self.assertEqual(k.camelot_number, 3)
        self.assertEqual(k.camelot_letter, 'B')

    def test_post_init_validate__success_min(self, mock_post_init):
        k = Key(letter='G', type='minor', key='foo', camelot_number=3, camelot_letter='B')
        self.assertEqual(k.letter, 'G')
        self.assertEqual(k.type, 'minor')
        self.assertEqual(k.key, 'foo')
        self.assertEqual(k.camelot_number, 3)
        self.assertEqual(k.camelot_letter, 'B')

    def test_post_init_validate__success_maj_sharp(self, mock_post_init):
        k = Key(letter='G', sharp=True, key='foo', camelot_number=3, camelot_letter='B')
        self.assertEqual(k.letter, 'G')
        self.assertEqual(k.type, 'major')
        self.assertTrue(k.sharp)
        self.assertFalse(k.flat)
        self.assertEqual(k.key, 'foo')
        self.assertEqual(k.camelot_number, 3)
        self.assertEqual(k.camelot_letter, 'B')

    def test_post_init_validate__success_min_flat(self, mock_post_init):
        k = Key(letter='G', type='minor', flat=True, key='foo', camelot_number=3, camelot_letter='B')
        self.assertEqual(k.letter, 'G')
        self.assertEqual(k.type, 'minor')
        self.assertFalse(k.sharp)
        self.assertTrue(k.flat)
        self.assertEqual(k.key, 'foo')
        self.assertEqual(k.camelot_number, 3)
        self.assertEqual(k.camelot_letter, 'B')


@patch('src.camelot_key.Key._Key__post_init__parse')
@patch('src.camelot_key.Key._Key__post_init__key')
@patch('src.camelot_key.Key._Key__post_init__camelot')
@patch('src.camelot_key.Key._Key__post_init__validate')
class TestKey_Init_PostInit(TestCase):
    def test_post_init(self, mock_v, mock_c, mock_k, mock_p):
        k = Key()
        mock_p.assert_called_once_with()
        mock_k.assert_called_once_with()
        mock_c.assert_called_once_with()
        mock_v.assert_called_once_with()


class TestKey_CamelotKey(TestCase):
    def test_camelot_key_not_present(self):
        k = Key(letter='A', flat=True, type='minor', key='foo')
        self.assertIsNone(k.camelot_key)

    def test_camelot_key(self):
        k = Key(letter='A', flat=True, type='minor')
        self.assertEqual(k.camelot_key, '1A')


class TestKey_Str(TestCase):
    def test_str_no_camelot_key(self):
        k = Key(letter='A', flat=True, type='minor', key='foo')
        self.assertEqual(str(k), 'foo')

    def test_str(self):
        k = Key(letter='A', flat=True, type='minor')
        self.assertEqual(str(k), 'Abm (1A)')


class TestKey_Hash(TestCase):
    def test_hash(self):
        k1 = Key(letter='A', flat=True, type='minor')
        k2 = Key(letter='A', flat=True, type='minor')
        k3 = Key(letter='A', type='minor')
        self.assertEqual(hash(k1), hash(k2))
        self.assertNotEqual(hash(k1), hash(k3))
        self.assertNotEqual(hash(k2), hash(k3))


class TestKey_Compare(TestCase):
    def test_equality(self):
        k1 = Key(letter='A', flat=True, type='minor')
        k2 = Key(letter='A', flat=True, type='minor')
        k3 = Key(letter='G', sharp=True, type='minor')
        k4 = Key(letter='F', sharp=True, type='minor')
        self.assertEqual(k1, k2)
        self.assertEqual(k1, k3)
        self.assertEqual(k2, k3)
        self.assertNotEqual(k1, k4)
        self.assertNotEqual(k2, k4)
        self.assertNotEqual(k3, k4)

    def test_number_repr(self):
        k = Key(letter='F', key='foo')
        self.assertEqual(k._camelot_key_number_repr, -1.0)

        k = Key(camelot_number=3, camelot_letter='A')
        self.assertEqual(k._camelot_key_number_repr, 3.0)

        k = Key(camelot_number=3, camelot_letter='B')
        self.assertEqual(k._camelot_key_number_repr, 3.5)

    def test_compare(self):
        k1 = Key(camelot_number=1, camelot_letter='A')
        k2 = Key(camelot_number=1, camelot_letter='A')
        k3 = Key(camelot_number=1, camelot_letter='B')
        k4 = Key(camelot_number=2, camelot_letter='A')

        self.assertTrue(k1 <= k2)
        self.assertTrue(k1 >= k2)
        self.assertTrue(k1 < k3)
        self.assertTrue(k1 < k4)
        self.assertTrue(k3 < k4)
        self.assertTrue(k4 > k3)
        self.assertTrue(k4 > k1)
        self.assertTrue(k3 > k1)

    def test_sortable(self):
        keys = [
            Key(camelot_number=7, camelot_letter='B'),
            Key(camelot_number=9, camelot_letter='B'),
            Key(camelot_number=4, camelot_letter='A'),
            Key(camelot_number=9, camelot_letter='A'),
            Key(camelot_number=6, camelot_letter='B'),
            Key(camelot_number=3, camelot_letter='A'),
            Key(camelot_number=1, camelot_letter='A'),
            Key(camelot_number=8, camelot_letter='A'),
            Key(camelot_number=6, camelot_letter='A'),
            Key(camelot_number=3, camelot_letter='B'),
            Key(camelot_number=2, camelot_letter='B'),
            Key(camelot_number=12, camelot_letter='A'),
            Key(camelot_number=8, camelot_letter='B'),
            Key(letter='F', key='foo'),
            Key(camelot_number=4, camelot_letter='B'),
            Key(camelot_number=10, camelot_letter='A'),
            Key(camelot_number=10, camelot_letter='B'),
            Key(camelot_number=11, camelot_letter='A'),
            Key(camelot_number=7, camelot_letter='A'),
            Key(camelot_number=2, camelot_letter='A'),
            Key(camelot_number=11, camelot_letter='B'),
            Key(camelot_number=1, camelot_letter='B'),
            Key(camelot_number=5, camelot_letter='B'),
            Key(camelot_number=5, camelot_letter='A'),
            Key(camelot_number=12, camelot_letter='B'),
        ]
        keys = list(sorted(keys))
        self.assertEqual(keys, [
            Key(letter='F', key='foo'),
            Key(camelot_number=1, camelot_letter='A'),
            Key(camelot_number=1, camelot_letter='B'),
            Key(camelot_number=2, camelot_letter='A'),
            Key(camelot_number=2, camelot_letter='B'),
            Key(camelot_number=3, camelot_letter='A'),
            Key(camelot_number=3, camelot_letter='B'),
            Key(camelot_number=4, camelot_letter='A'),
            Key(camelot_number=4, camelot_letter='B'),
            Key(camelot_number=5, camelot_letter='A'),
            Key(camelot_number=5, camelot_letter='B'),
            Key(camelot_number=6, camelot_letter='A'),
            Key(camelot_number=6, camelot_letter='B'),
            Key(camelot_number=7, camelot_letter='A'),
            Key(camelot_number=7, camelot_letter='B'),
            Key(camelot_number=8, camelot_letter='A'),
            Key(camelot_number=8, camelot_letter='B'),
            Key(camelot_number=9, camelot_letter='A'),
            Key(camelot_number=9, camelot_letter='B'),
            Key(camelot_number=10, camelot_letter='A'),
            Key(camelot_number=10, camelot_letter='B'),
            Key(camelot_number=11, camelot_letter='A'),
            Key(camelot_number=11, camelot_letter='B'),
            Key(camelot_number=12, camelot_letter='A'),
            Key(camelot_number=12, camelot_letter='B'),
        ])


class TestKey_AltKeys(TestCase):
    def test_alt_keys(self):
        k = Key(letter='C', sharp=True)
        self.assertEqual(list(k.alternate_keys), [k, Key(letter='D', flat=True)])
        k = Key(letter='E', sharp=True)
        self.assertEqual(list(k.alternate_keys), [k, Key(letter='F')])


class TestKey_Copy(TestCase):
    def test_copy_no_args(self):
        k = Key(letter='C', type='minor')
        self.assertEqual(k, k._copy())

    def test_copy_musical_args(self):
        k = Key(letter='C', type='minor')
        self.assertEqual(k._copy(sharp=True), Key(letter='C', type='minor', sharp=True))

    def test_copy_camelot_args(self):
        k = Key(camelot_number=3, camelot_letter='B')
        self.assertEqual(k._copy(sharp=True, camelot_letter='A'), Key(camelot_number=3, camelot_letter='A'))


class TestKey_Shift(TestCase):
    def test_shift_no_camelot_key(self):
        k = Key(letter='C', key='foo')
        with self.assertRaises(ValueError):
            k.shift(1)

    def test_shift_down(self):
        k = Key(camelot_number=3, camelot_letter='B')
        nk = k.shift(-1)
        self.assertEqual(nk, Key(camelot_number=2, camelot_letter='B'))

    def test_shift_up(self):
        k = Key(camelot_number=3, camelot_letter='B')
        nk = k.shift(1)
        self.assertEqual(nk, Key(camelot_number=4, camelot_letter='B'))

    def test_shift_down_out_of_range(self):
        k = Key(camelot_number=3, camelot_letter='B')
        nk = k.shift(-4)
        self.assertEqual(nk, Key(camelot_number=11, camelot_letter='B'))

    def test_shift_up_out_of_range(self):
        k = Key(camelot_number=3, camelot_letter='B')
        nk = k.shift(11)
        self.assertEqual(nk, Key(camelot_number=2, camelot_letter='B'))


@patch('src.camelot_key.Key.__repr__', Key.__str__)
class TestKey_AdjacentKeys(TestCase):
    maxDiff = None

    def test_adjacent_1(self):
        k = Key(camelot_number=3, camelot_letter='B')
        res = list(sorted(k.get_adjacent_keys()))
        self.assertEqual(res, list(sorted([
            # Immediately adjacent; no shifting
            (0, Key(camelot_number=3, camelot_letter='B')),
            (0, Key(camelot_number=3, camelot_letter='A')),
            (0, Key(camelot_number=2, camelot_letter='B')),
            (0, Key(camelot_number=4, camelot_letter='B')),
        ])))

    def test_adjacent_2(self):
        k = Key(camelot_number=3, camelot_letter='B')
        res = list(sorted(k.get_adjacent_keys(2)))
        self.assertEqual(res, list(sorted([
            # Immediately adjacent; no shifting
            (0, Key(camelot_number=3, camelot_letter='B')),
            (0, Key(camelot_number=3, camelot_letter='A')),
            (0, Key(camelot_number=2, camelot_letter='B')),
            (0, Key(camelot_number=4, camelot_letter='B')),

            # first shift - becomes base key
            (-1, Key(camelot_number=8, camelot_letter='B')),
            (1, Key(camelot_number=10, camelot_letter='B')),
            # first shift - becomes alt key
            (-1, Key(camelot_number=8, camelot_letter='A')),
            (1, Key(camelot_number=10, camelot_letter='A')),
            # first shift - becomes adjacent key (+/- 1)
            (-1, Key(camelot_number=7, camelot_letter='B')),
            (1, Key(camelot_number=9, camelot_letter='B')),
            (-1, Key(camelot_number=9, camelot_letter='B')),
            (1, Key(camelot_number=11, camelot_letter='B')),
        ])))

    def test_adjacent_3(self):
        k = Key(camelot_number=3, camelot_letter='B')
        res = list(sorted(k.get_adjacent_keys(3)))
        self.assertEqual(res, list(sorted([
            # Immediately adjacent; no shifting
            (0, Key(camelot_number=3, camelot_letter='B')),
            (0, Key(camelot_number=3, camelot_letter='A')),
            (0, Key(camelot_number=2, camelot_letter='B')),
            (0, Key(camelot_number=4, camelot_letter='B')),

            # first shift - becomes base key
            (-1, Key(camelot_number=8, camelot_letter='B')),
            (1, Key(camelot_number=10, camelot_letter='B')),
            # first shift - becomes alt key
            (-1, Key(camelot_number=8, camelot_letter='A')),
            (1, Key(camelot_number=10, camelot_letter='A')),
            # first shift - becomes adjacent key (+/- 1)
            (-1, Key(camelot_number=7, camelot_letter='B')),
            (1, Key(camelot_number=9, camelot_letter='B')),
            (-1, Key(camelot_number=9, camelot_letter='B')),
            (1, Key(camelot_number=11, camelot_letter='B')),

            # second shift - becomes base key
            (-2, Key(camelot_number=1, camelot_letter='B')),
            (2, Key(camelot_number=5, camelot_letter='B')),
            # second shift - becomes alt key
            (-2, Key(camelot_number=1, camelot_letter='A')),
            (2, Key(camelot_number=5, camelot_letter='A')),
            # second shift - becomes adjacent key (+/- 1)
            (-2, Key(camelot_number=12, camelot_letter='B')),
            (2, Key(camelot_number=4, camelot_letter='B')),
            (-2, Key(camelot_number=2, camelot_letter='B')),
            (2, Key(camelot_number=6, camelot_letter='B')),
        ])))
