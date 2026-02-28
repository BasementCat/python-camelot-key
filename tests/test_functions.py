from unittest import TestCase
from unittest.mock import MagicMock, patch, call, ANY

from src.camelot_key import (
    Key,
    _parse_beatport__musical,
    _parse_beatport__camelot,
    _parse_str__musical,
    _parse_str__camelot,
    parse,
)


class TestParseBeatportMusical(TestCase):
    def test_no_key(self):
        val = {'is_sharp': False, 'is_flat': False, 'chord_type': {'name': 'major'}}
        res = _parse_beatport__musical(val)
        self.assertIsNone(res)

    def test_no_sharp(self):
        val = {'letter': 'C', 'is_flat': False, 'chord_type': {'name': 'major'}}
        res = _parse_beatport__musical(val)
        self.assertIsNone(res)

    def test_no_flat(self):
        val = {'letter': 'C', 'is_sharp': False, 'chord_type': {'name': 'major'}}
        res = _parse_beatport__musical(val)
        self.assertIsNone(res)

    def test_no_type_outer(self):
        val = {'letter': 'C', 'is_sharp': False, 'is_flat': False}
        res = _parse_beatport__musical(val)
        self.assertIsNone(res)

    def test_no_type_name(self):
        val = {'letter': 'C', 'is_sharp': False, 'is_flat': False, 'chord_type': {}}
        res = _parse_beatport__musical(val)
        self.assertIsNone(res)

    def test_parse_ok(self):
        val = {'letter': 'C', 'is_sharp': False, 'is_flat': False, 'chord_type': {'name': 'major'}}
        res = _parse_beatport__musical(val)
        self.assertEqual(res, Key(letter='C'))


class TestParseBeatportCamelot(TestCase):
    def test_no_camelot_number(self):
        val = {'camelot_letter': 'B'}
        res = _parse_beatport__camelot(val)
        self.assertIsNone(res)

    def test_camelot_number_not_int(self):
        val = {'camelot_number': 'asdf', 'camelot_letter': 'B'}
        res = _parse_beatport__camelot(val)
        self.assertIsNone(res)

    def test_no_camelot_letter(self):
        val = {'camelot_number': 4}
        res = _parse_beatport__camelot(val)
        self.assertIsNone(res)

    def test_valid(self):
        val = {'camelot_number': 4, 'camelot_letter': 'B'}
        res = _parse_beatport__camelot(val)
        self.assertEqual(res, Key(letter='A', flat=True))


class TestParseStrMusical(TestCase):
    def test_parse(self):
        test_cases = {
            'X':        None,
            'x':        None,
            'C7':       None,
            'C^m':      None,
            'A':        Key(letter='A', sharp=False, flat=False, type='major'),
            'A#M':      Key(letter='A', sharp=True,  flat=False, type='major'),
            'A#m':      Key(letter='A', sharp=True,  flat=False, type='minor'),
            'Ab':       Key(letter='A', sharp=False, flat=True,  type='major'),
            'Ab Major': Key(letter='A', sharp=False, flat=True,  type='major'),
            'Ab Minor': Key(letter='A', sharp=False, flat=True,  type='minor'),
            'Abm':      Key(letter='A', sharp=False, flat=True,  type='minor'),
            'AbM':      Key(letter='A', sharp=False, flat=True,  type='major'),
            'Abmaj':    Key(letter='A', sharp=False, flat=True,  type='major'),
            'Abmin':    Key(letter='A', sharp=False, flat=True,  type='minor'),
            'Am':       Key(letter='A', sharp=False, flat=False, type='minor'),
            'AM':       Key(letter='A', sharp=False, flat=False, type='major'),
            'Amaj':     Key(letter='A', sharp=False, flat=False, type='major'),
            'Amin':     Key(letter='A', sharp=False, flat=False, type='minor'),
            'B':        Key(letter='B', sharp=False, flat=False, type='major'),
            'B Major':  Key(letter='B', sharp=False, flat=False, type='major'),
            'Bb':       Key(letter='B', sharp=False, flat=True,  type='major'),
            'Bb Major': Key(letter='B', sharp=False, flat=True,  type='major'),
            'BbM':      Key(letter='B', sharp=False, flat=True,  type='major'),
            'Bbm':      Key(letter='B', sharp=False, flat=True,  type='minor'),
            'Bbmaj':    Key(letter='B', sharp=False, flat=True,  type='major'),
            'Bbmin':    Key(letter='B', sharp=False, flat=True,  type='minor'),
            'Bm':       Key(letter='B', sharp=False, flat=False, type='minor'),
            'BM':       Key(letter='B', sharp=False, flat=False, type='major'),
            'Bmaj':     Key(letter='B', sharp=False, flat=False, type='major'),
            'Bmin':     Key(letter='B', sharp=False, flat=False, type='minor'),
            'C':        Key(letter='C', sharp=False, flat=False, type='major'),
            'C Major':  Key(letter='C', sharp=False, flat=False, type='major'),
            'C Minor':  Key(letter='C', sharp=False, flat=False, type='minor'),
            'C#M':      Key(letter='C', sharp=True,  flat=False, type='major'),
            'C#m':      Key(letter='C', sharp=True,  flat=False, type='minor'),
            'Cm':       Key(letter='C', sharp=False, flat=False, type='minor'),
            'CM':       Key(letter='C', sharp=False, flat=False, type='major'),
            'Cmaj':     Key(letter='C', sharp=False, flat=False, type='major'),
            'Cmin':     Key(letter='C', sharp=False, flat=False, type='minor'),
            'D#M':      Key(letter='D', sharp=True,  flat=False, type='major'),
            'D#m':      Key(letter='D', sharp=True,  flat=False, type='minor'),
            'D#maj':    Key(letter='D', sharp=True,  flat=False, type='major'),
            'Db':       Key(letter='D', sharp=False, flat=True,  type='major'),
            'Db Major': Key(letter='D', sharp=False, flat=True,  type='major'),
            'Dbm':      Key(letter='D', sharp=False, flat=True,  type='minor'),
            'DbM':      Key(letter='D', sharp=False, flat=True,  type='major'),
            'Dbmin':    Key(letter='D', sharp=False, flat=True,  type='minor'),
            'Dm':       Key(letter='D', sharp=False, flat=False, type='minor'),
            'DM':       Key(letter='D', sharp=False, flat=False, type='major'),
            'Dmaj':     Key(letter='D', sharp=False, flat=False, type='major'),
            'Dmin':     Key(letter='D', sharp=False, flat=False, type='minor'),
            'E':        Key(letter='E', sharp=False, flat=False, type='major'),
            'E Minor':  Key(letter='E', sharp=False, flat=False, type='minor'),
            'Eb':       Key(letter='E', sharp=False, flat=True,  type='major'),
            'Eb Major': Key(letter='E', sharp=False, flat=True,  type='major'),
            'EbM':      Key(letter='E', sharp=False, flat=True,  type='major'),
            'Ebm':      Key(letter='E', sharp=False, flat=True,  type='minor'),
            'Ebmaj':    Key(letter='E', sharp=False, flat=True,  type='major'),
            'Ebmin':    Key(letter='E', sharp=False, flat=True,  type='minor'),
            'Em':       Key(letter='E', sharp=False, flat=False, type='minor'),
            'EM':       Key(letter='E', sharp=False, flat=False, type='major'),
            'Emaj':     Key(letter='E', sharp=False, flat=False, type='major'),
            'Emin':     Key(letter='E', sharp=False, flat=False, type='minor'),
            'F':        Key(letter='F', sharp=False, flat=False, type='major'),
            'F#M':      Key(letter='F', sharp=True,  flat=False, type='major'),
            'F#m':      Key(letter='F', sharp=True,  flat=False, type='minor'),
            'F#min':    Key(letter='F', sharp=True,  flat=False, type='minor'),
            'Fm':       Key(letter='F', sharp=False, flat=False, type='minor'),
            'FM':       Key(letter='F', sharp=False, flat=False, type='major'),
            'Fmaj':     Key(letter='F', sharp=False, flat=False, type='major'),
            'Fmin':     Key(letter='F', sharp=False, flat=False, type='minor'),
            'G':        Key(letter='G', sharp=False, flat=False, type='major'),
            'G Minor':  Key(letter='G', sharp=False, flat=False, type='minor'),
            'G#m':      Key(letter='G', sharp=True,  flat=False, type='minor'),
            'G#M':      Key(letter='G', sharp=True,  flat=False, type='major'),
            'Gb':       Key(letter='G', sharp=False, flat=True,  type='major'),
            'Gb Minor': Key(letter='G', sharp=False, flat=True,  type='minor'),
            'Gbm':      Key(letter='G', sharp=False, flat=True,  type='minor'),
            'GbM':      Key(letter='G', sharp=False, flat=True,  type='major'),
            'Gbmaj':    Key(letter='G', sharp=False, flat=True,  type='major'),
            'Gbmin':    Key(letter='G', sharp=False, flat=True,  type='minor'),
            'Gm':       Key(letter='G', sharp=False, flat=False, type='minor'),
            'GM':       Key(letter='G', sharp=False, flat=False, type='major'),
            'Gmaj':     Key(letter='G', sharp=False, flat=False, type='major'),
            'Gmin':     Key(letter='G', sharp=False, flat=False, type='minor'),
        }
        count = 0
        for raw, val in test_cases.items():
            res = _parse_str__musical(raw)
            self.assertEqual(res, val)
            count += 1
        self.assertEqual(count, len(test_cases))


class TestParseStrCamelot(TestCase):
    def test_value_is_none(self):
        val = None
        res = _parse_str__camelot(val)
        self.assertIsNone(res)

    def test_value_is_empty(self):
        val = ''
        res = _parse_str__camelot(val)
        self.assertIsNone(res)

    def test_value_is_not_str(self):
        val = 5
        res = _parse_str__camelot(val)
        self.assertIsNone(res)

    def test_invalid_length__long(self):
        val = '44BB'
        res = _parse_str__camelot(val)
        self.assertIsNone(res)

    def test_invalid_length__short(self):
        val = '4'
        res = _parse_str__camelot(val)
        self.assertIsNone(res)

    def test_valid(self):
        val = '4B'
        res = _parse_str__camelot(val)
        self.assertEqual(res, Key(camelot_number=4, camelot_letter='B'))


@patch('src.camelot_key._parse_str__musical')
@patch('src.camelot_key._parse_str__camelot')
@patch('src.camelot_key._parse_beatport__musical')
@patch('src.camelot_key._parse_beatport__camelot')
class TestParse(TestCase):
    def test_value_is_str__not_musical_or_camelot(self, mock_parse_bp_camelot, mock_parse_bp_musical, mock_parse_str_camelot, mock_parse_str_musical):
        mock_parse_str_musical.return_value = None
        mock_parse_str_camelot.return_value = None
        val = 'foo'
        res = parse(val)
        self.assertIsNone(res)
        mock_parse_bp_camelot.assert_not_called()
        mock_parse_bp_musical.assert_not_called()
        mock_parse_str_camelot.assert_called_once_with(val)
        mock_parse_str_musical.assert_called_once_with(val)

    def test_value_is_str__is_camelot(self, mock_parse_bp_camelot, mock_parse_bp_musical, mock_parse_str_camelot, mock_parse_str_musical):
        mock_parse_str_musical.return_value = None
        val = 'foo'
        res = parse(val)
        self.assertEqual(res, mock_parse_str_camelot.return_value)
        mock_parse_bp_camelot.assert_not_called()
        mock_parse_bp_musical.assert_not_called()
        mock_parse_str_camelot.assert_called_once_with(val)
        mock_parse_str_musical.assert_called_once_with(val)

    def test_value_is_str__is_musical(self, mock_parse_bp_camelot, mock_parse_bp_musical, mock_parse_str_camelot, mock_parse_str_musical):
        val = 'foo'
        res = parse(val)
        self.assertEqual(res, mock_parse_str_musical.return_value)
        mock_parse_bp_camelot.assert_not_called()
        mock_parse_bp_musical.assert_not_called()
        mock_parse_str_camelot.assert_not_called()
        mock_parse_str_musical.assert_called_once_with(val)

    def test_value_not_str__not_musical_or_camelot(self, mock_parse_bp_camelot, mock_parse_bp_musical, mock_parse_str_camelot, mock_parse_str_musical):
        mock_parse_bp_musical.return_value = None
        mock_parse_bp_camelot.return_value = None
        val = {'foo': 'bar'}
        res = parse(val)
        self.assertIsNone(res)
        mock_parse_bp_camelot.assert_called_once_with(val)
        mock_parse_bp_musical.assert_called_once_with(val)
        mock_parse_str_camelot.assert_not_called()
        mock_parse_str_musical.assert_not_called()

    def test_value_not_str__is_camelot(self, mock_parse_bp_camelot, mock_parse_bp_musical, mock_parse_str_camelot, mock_parse_str_musical):
        mock_parse_bp_musical.return_value = None
        val = {'foo': 'bar'}
        res = parse(val)
        self.assertEqual(res, mock_parse_bp_camelot.return_value)
        mock_parse_bp_camelot.assert_called_once_with(val)
        mock_parse_bp_musical.assert_called_once_with(val)
        mock_parse_str_camelot.assert_not_called()
        mock_parse_str_musical.assert_not_called()

    def test_value_not_str__is_musical(self, mock_parse_bp_camelot, mock_parse_bp_musical, mock_parse_str_camelot, mock_parse_str_musical):
        val = {'foo': 'bar'}
        res = parse(val)
        self.assertEqual(res, mock_parse_bp_musical.return_value)
        mock_parse_bp_camelot.assert_not_called()
        mock_parse_bp_musical.assert_called_once_with(val)
        mock_parse_str_camelot.assert_not_called()
        mock_parse_str_musical.assert_not_called()
